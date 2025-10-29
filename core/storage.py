"""
Sistema de armazenamento para o AETHER Dashboard Automotivo.

Este módulo fornece funcionalidades de armazenamento de dados de telemetria,
incluindo persistência em CSV e preparação para futuras implementações em SQLite.
"""

import csv
import os
import sqlite3
from datetime import datetime, timedelta
from pathlib import Path
from typing import List, Dict, Any, Optional, Union
import pandas as pd

from utils.types import TelemetryPayload
from core.logger import get_logger

logger = get_logger("storage")


class DataStorage:
    """
    Classe para gerenciar armazenamento de dados de telemetria.
    
    Suporta armazenamento em CSV e preparação para SQLite.
    """
    
    def __init__(self, 
                 data_dir: str = "data",
                 csv_filename: str = "telemetry_data.csv",
                 sqlite_filename: str = "aether.db"):
        """
        Inicializa o sistema de armazenamento.
        
        Args:
            data_dir: Diretório para armazenar dados
            csv_filename: Nome do arquivo CSV
            sqlite_filename: Nome do arquivo SQLite
        """
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(exist_ok=True)
        
        self.csv_file = self.data_dir / csv_filename
        self.sqlite_file = self.data_dir / sqlite_filename
        
        # Inicializar CSV se não existir
        self._init_csv()
        
        logger.info(f"Data storage initialized", 
                   data_dir=str(self.data_dir),
                   csv_file=str(self.csv_file))
    
    def _init_csv(self) -> None:
        """Inicializa o arquivo CSV com cabeçalhos."""
        if not self.csv_file.exists():
            headers = [
                'timestamp', 'source', 'rpm', 'speed', 'coolant_temp',
                'throttle', 'engine_load', 'intake_temp', 'map',
                'fuel_pressure', 'fuel_level', 'fuel_consumption',
                'fuel_consumption_rate', 'errors'
            ]
            
            with open(self.csv_file, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(headers)
            
            logger.info("CSV file initialized", file=str(self.csv_file))
    
    def save_telemetry(self, payload: TelemetryPayload) -> bool:
        """
        Salva dados de telemetria no CSV.
        
        Args:
            payload: Dados de telemetria para salvar
            
        Returns:
            True se salvou com sucesso, False caso contrário
        """
        try:
            # Preparar dados para CSV
            row_data = {
                'timestamp': datetime.fromtimestamp(payload["timestamp"]).isoformat(),
                'source': payload["source"],
                'errors': '; '.join(payload["errors"]) if payload["errors"] else ''
            }
            
            # Adicionar dados dos sensores
            for sensor_name, sensor_data in payload["sensors"].items():
                row_data[sensor_name] = sensor_data["value"]
            
            # Escrever no CSV
            with open(self.csv_file, 'a', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=row_data.keys())
                writer.writerow(row_data)
            
            logger.debug("Telemetry data saved to CSV", 
                        timestamp=row_data['timestamp'],
                        source=payload["source"])
            
            return True
            
        except Exception as e:
            logger.error(f"Failed to save telemetry data: {e}")
            return False
    
    def load_telemetry(self, 
                      start_date: Optional[datetime] = None,
                      end_date: Optional[datetime] = None,
                      source: Optional[str] = None,
                      limit: Optional[int] = None) -> pd.DataFrame:
        """
        Carrega dados de telemetria do CSV.
        
        Args:
            start_date: Data de início (opcional)
            end_date: Data de fim (opcional)
            source: Fonte de dados (opcional)
            limit: Limite de registros (opcional)
            
        Returns:
            DataFrame com os dados carregados
        """
        try:
            if not self.csv_file.exists():
                logger.warning("CSV file does not exist")
                return pd.DataFrame()
            
            # Carregar dados
            df = pd.read_csv(self.csv_file)
            df['timestamp'] = pd.to_datetime(df['timestamp'])
            
            # Filtrar por data
            if start_date:
                df = df[df['timestamp'] >= start_date]
            if end_date:
                df = df[df['timestamp'] <= end_date]
            
            # Filtrar por fonte
            if source:
                df = df[df['source'] == source]
            
            # Ordenar por timestamp
            df = df.sort_values('timestamp')
            
            # Limitar registros
            if limit:
                df = df.tail(limit)
            
            logger.info(f"Loaded {len(df)} telemetry records",
                       start_date=start_date.isoformat() if start_date else None,
                       end_date=end_date.isoformat() if end_date else None,
                       source=source)
            
            return df
            
        except Exception as e:
            logger.error(f"Failed to load telemetry data: {e}")
            return pd.DataFrame()
    
    def get_statistics(self, 
                      days: int = 7,
                      source: Optional[str] = None) -> Dict[str, Any]:
        """
        Calcula estatísticas dos dados armazenados.
        
        Args:
            days: Número de dias para análise
            source: Fonte de dados (opcional)
            
        Returns:
            Dicionário com estatísticas
        """
        try:
            end_date = datetime.now()
            start_date = end_date - timedelta(days=days)
            
            df = self.load_telemetry(start_date, end_date, source)
            
            if df.empty:
                return {"error": "No data available"}
            
            # Calcular estatísticas
            stats = {
                "total_records": len(df),
                "date_range": {
                    "start": df['timestamp'].min().isoformat(),
                    "end": df['timestamp'].max().isoformat()
                },
                "sources": df['source'].value_counts().to_dict(),
                "sensor_stats": {}
            }
            
            # Estatísticas por sensor
            sensor_columns = [col for col in df.columns 
                            if col not in ['timestamp', 'source', 'errors']]
            
            for sensor in sensor_columns:
                if sensor in df.columns:
                    sensor_data = df[sensor].dropna()
                    if not sensor_data.empty:
                        stats["sensor_stats"][sensor] = {
                            "count": len(sensor_data),
                            "mean": float(sensor_data.mean()),
                            "min": float(sensor_data.min()),
                            "max": float(sensor_data.max()),
                            "std": float(sensor_data.std())
                        }
            
            logger.info(f"Statistics calculated for {days} days",
                       total_records=stats["total_records"])
            
            return stats
            
        except Exception as e:
            logger.error(f"Failed to calculate statistics: {e}")
            return {"error": str(e)}
    
    def cleanup_old_data(self, days_to_keep: int = 30) -> int:
        """
        Remove dados antigos do CSV.
        
        Args:
            days_to_keep: Número de dias para manter
            
        Returns:
            Número de registros removidos
        """
        try:
            if not self.csv_file.exists():
                return 0
            
            # Carregar todos os dados
            df = pd.read_csv(self.csv_file)
            df['timestamp'] = pd.to_datetime(df['timestamp'])
            
            # Calcular data de corte
            cutoff_date = datetime.now() - timedelta(days=days_to_keep)
            
            # Filtrar dados recentes
            recent_data = df[df['timestamp'] >= cutoff_date]
            
            # Salvar dados filtrados
            recent_data.to_csv(self.csv_file, index=False)
            
            removed_count = len(df) - len(recent_data)
            
            logger.info(f"Cleaned up old data",
                       removed_records=removed_count,
                       kept_records=len(recent_data),
                       cutoff_date=cutoff_date.isoformat())
            
            return removed_count
            
        except Exception as e:
            logger.error(f"Failed to cleanup old data: {e}")
            return 0
    
    def export_data(self, 
                   output_file: str,
                   start_date: Optional[datetime] = None,
                   end_date: Optional[datetime] = None,
                   source: Optional[str] = None) -> bool:
        """
        Exporta dados para um arquivo.
        
        Args:
            output_file: Arquivo de saída
            start_date: Data de início (opcional)
            end_date: Data de fim (opcional)
            source: Fonte de dados (opcional)
            
        Returns:
            True se exportou com sucesso, False caso contrário
        """
        try:
            df = self.load_telemetry(start_date, end_date, source)
            
            if df.empty:
                logger.warning("No data to export")
                return False
            
            # Determinar formato baseado na extensão
            output_path = Path(output_file)
            if output_path.suffix.lower() == '.json':
                df.to_json(output_file, orient='records', date_format='iso')
            elif output_path.suffix.lower() == '.xlsx':
                df.to_excel(output_file, index=False)
            else:
                df.to_csv(output_file, index=False)
            
            logger.info(f"Data exported successfully",
                       output_file=output_file,
                       records=len(df))
            
            return True
            
        except Exception as e:
            logger.error(f"Failed to export data: {e}")
            return False
    
    def get_file_size(self) -> Dict[str, int]:
        """
        Retorna informações sobre o tamanho dos arquivos de dados.
        
        Returns:
            Dicionário com tamanhos dos arquivos
        """
        sizes = {}
        
        if self.csv_file.exists():
            sizes['csv'] = self.csv_file.stat().st_size
        
        if self.sqlite_file.exists():
            sizes['sqlite'] = self.sqlite_file.stat().st_size
        
        return sizes


# Instância global do storage
storage = DataStorage()


def save_telemetry(payload: TelemetryPayload) -> bool:
    """Salva dados de telemetria usando o storage global."""
    return storage.save_telemetry(payload)


def load_telemetry(**kwargs) -> pd.DataFrame:
    """Carrega dados de telemetria usando o storage global."""
    return storage.load_telemetry(**kwargs)


def get_statistics(**kwargs) -> Dict[str, Any]:
    """Obtém estatísticas usando o storage global."""
    return storage.get_statistics(**kwargs)