"""
Sistema de armazenamento para AETHER.
Salva dados de telemetria em CSV e prepara para SQLite futuro.
"""

import csv
import os
from datetime import datetime
from pathlib import Path
from typing import Dict, Any

from utils.types import TelemetryPayload


def ensure_data_dir() -> Path:
    """Garante que o diretório de dados existe.
    
    Returns:
        Path do diretório de dados
    """
    data_dir = Path("data")
    data_dir.mkdir(exist_ok=True)
    return data_dir


def append_csv(payload: TelemetryPayload, filename: str = "telemetry.csv") -> None:
    """Salva payload de telemetria em CSV.
    
    Args:
        payload: TelemetryPayload para salvar
        filename: Nome do arquivo CSV
    """
    data_dir = ensure_data_dir()
    filepath = data_dir / filename
    
    # Verificar se arquivo existe para escrever cabeçalho
    file_exists = filepath.exists()
    
    # Preparar dados para CSV
    row_data = {
        "timestamp": payload["timestamp"],
        "datetime": datetime.fromtimestamp(payload["timestamp"]).isoformat(),
        "source": payload["source"],
        "errors": "; ".join(payload["errors"]) if payload["errors"] else ""
    }
    
    # Adicionar dados dos sensores
    for name, sensor in payload["sensors"].items():
        row_data[f"{name}_value"] = sensor["value"]
        row_data[f"{name}_unit"] = sensor["unit"]
        row_data[f"{name}_ok"] = sensor["ok"]
    
    # Escrever no CSV
    with open(filepath, "a", newline="", encoding="utf-8") as csvfile:
        fieldnames = list(row_data.keys())
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
        # Escrever cabeçalho se arquivo não existe
        if not file_exists:
            writer.writeheader()
        
        writer.writerow(row_data)


def read_recent_data(filename: str = "telemetry.csv", limit: int = 100) -> list:
    """Lê dados recentes do CSV.
    
    Args:
        filename: Nome do arquivo CSV
        limit: Número máximo de registros a retornar
    
    Returns:
        Lista de dicionários com os dados
    """
    data_dir = ensure_data_dir()
    filepath = data_dir / filename
    
    if not filepath.exists():
        return []
    
    data = []
    with open(filepath, "r", encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile)
        rows = list(reader)
        
        # Retornar últimos N registros
        data = rows[-limit:] if len(rows) > limit else rows
    
    return data


def get_file_stats(filename: str = "telemetry.csv") -> Dict[str, Any]:
    """Retorna estatísticas do arquivo de dados.
    
    Args:
        filename: Nome do arquivo CSV
    
    Returns:
        Dicionário com estatísticas
    """
    data_dir = ensure_data_dir()
    filepath = data_dir / filename
    
    if not filepath.exists():
        return {"exists": False, "size": 0, "records": 0}
    
    # Contar linhas (menos o cabeçalho)
    with open(filepath, "r", encoding="utf-8") as csvfile:
        reader = csv.reader(csvfile)
        records = sum(1 for row in reader) - 1  # -1 para cabeçalho
    
    return {
        "exists": True,
        "size": filepath.stat().st_size,
        "records": max(0, records),
        "filepath": str(filepath)
    }
