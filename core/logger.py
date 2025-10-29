"""
Sistema de logging para o AETHER Dashboard Automotivo.

Este módulo fornece funcionalidades de logging centralizadas para o sistema,
incluindo diferentes níveis de log, formatação personalizada e rotação de arquivos.
"""

import logging
import os
import sys
from datetime import datetime
from pathlib import Path
from typing import Optional, Dict, Any
from logging.handlers import RotatingFileHandler

from utils.types import TelemetryPayload


class AetherLogger:
    """
    Logger personalizado para o sistema AETHER.
    
    Fornece logging estruturado com diferentes níveis e formatação específica
    para dados automotivos e telemetria.
    """
    
    def __init__(self, 
                 name: str = "aether",
                 log_dir: str = "logs",
                 max_file_size: int = 10 * 1024 * 1024,  # 10MB
                 backup_count: int = 5,
                 level: int = logging.INFO):
        """
        Inicializa o logger do AETHER.
        
        Args:
            name: Nome do logger
            log_dir: Diretório para armazenar logs
            max_file_size: Tamanho máximo do arquivo de log em bytes
            backup_count: Número de arquivos de backup
            level: Nível de logging
        """
        self.name = name
        self.log_dir = Path(log_dir)
        self.log_dir.mkdir(exist_ok=True)
        
        # Configurar logger
        self.logger = logging.getLogger(name)
        self.logger.setLevel(level)
        
        # Evitar duplicação de handlers
        if not self.logger.handlers:
            self._setup_handlers(max_file_size, backup_count)
    
    def _setup_handlers(self, max_file_size: int, backup_count: int) -> None:
        """Configura os handlers de logging."""
        
        # Formatter personalizado
        formatter = logging.Formatter(
            '%(asctime)s | %(levelname)-8s | %(name)s | %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        
        # Handler para arquivo principal
        log_file = self.log_dir / f"{self.name}.log"
        file_handler = RotatingFileHandler(
            log_file,
            maxBytes=max_file_size,
            backupCount=backup_count,
            encoding='utf-8'
        )
        file_handler.setFormatter(formatter)
        file_handler.setLevel(logging.DEBUG)
        
        # Handler para console
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(formatter)
        console_handler.setLevel(logging.INFO)
        
        # Handler para erros
        error_file = self.log_dir / f"{self.name}_errors.log"
        error_handler = RotatingFileHandler(
            error_file,
            maxBytes=max_file_size,
            backupCount=backup_count,
            encoding='utf-8'
        )
        error_handler.setFormatter(formatter)
        error_handler.setLevel(logging.ERROR)
        
        # Adicionar handlers
        self.logger.addHandler(file_handler)
        self.logger.addHandler(console_handler)
        self.logger.addHandler(error_handler)
    
    def debug(self, message: str, **kwargs) -> None:
        """Log de debug."""
        self.logger.debug(self._format_message(message, **kwargs))
    
    def info(self, message: str, **kwargs) -> None:
        """Log de informação."""
        self.logger.info(self._format_message(message, **kwargs))
    
    def warning(self, message: str, **kwargs) -> None:
        """Log de aviso."""
        self.logger.warning(self._format_message(message, **kwargs))
    
    def error(self, message: str, **kwargs) -> None:
        """Log de erro."""
        self.logger.error(self._format_message(message, **kwargs))
    
    def critical(self, message: str, **kwargs) -> None:
        """Log crítico."""
        self.logger.critical(self._format_message(message, **kwargs))
    
    def _format_message(self, message: str, **kwargs) -> str:
        """Formata a mensagem com contexto adicional."""
        if kwargs:
            context = " | ".join([f"{k}={v}" for k, v in kwargs.items()])
            return f"{message} | {context}"
        return message
    
    def log_telemetry(self, payload: TelemetryPayload) -> None:
        """
        Log específico para dados de telemetria.
        
        Args:
            payload: Dados de telemetria para log
        """
        timestamp = datetime.fromtimestamp(payload["timestamp"])
        
        # Log básico da telemetria
        self.info(
            f"Telemetry data received",
            source=payload["source"],
            timestamp=timestamp.isoformat(),
            sensor_count=len(payload["sensors"]),
            error_count=len(payload["errors"])
        )
        
        # Log de erros se houver
        if payload["errors"]:
            for error in payload["errors"]:
                self.warning(f"Sensor error: {error}")
        
        # Log de valores críticos
        critical_sensors = ["rpm", "speed", "coolant_temp"]
        for sensor in critical_sensors:
            if sensor in payload["sensors"]:
                value = payload["sensors"][sensor]["value"]
                unit = payload["sensors"][sensor]["unit"]
                ok = payload["sensors"][sensor]["ok"]
                
                if not ok:
                    self.warning(f"Critical sensor out of range: {sensor}={value}{unit}")
                elif sensor == "rpm" and value > 6000:
                    self.warning(f"High RPM detected: {value}{unit}")
                elif sensor == "coolant_temp" and value > 100:
                    self.warning(f"High coolant temperature: {value}{unit}")
    
    def log_connection(self, source: str, status: str, details: Optional[str] = None) -> None:
        """
        Log de eventos de conexão.
        
        Args:
            source: Fonte de dados (mock, obd)
            status: Status da conexão (connected, disconnected, error)
            details: Detalhes adicionais
        """
        message = f"Connection {status}: {source}"
        if details:
            message += f" | {details}"
        
        if status == "connected":
            self.info(message)
        elif status == "disconnected":
            self.warning(message)
        else:
            self.error(message)
    
    def log_performance(self, operation: str, duration: float, **kwargs) -> None:
        """
        Log de performance de operações.
        
        Args:
            operation: Nome da operação
            duration: Duração em segundos
            **kwargs: Contexto adicional
        """
        self.info(
            f"Performance: {operation}",
            duration=f"{duration:.3f}s",
            **kwargs
        )
    
    def get_log_files(self) -> Dict[str, str]:
        """Retorna lista de arquivos de log."""
        log_files = {}
        for log_file in self.log_dir.glob("*.log"):
            log_files[log_file.stem] = str(log_file)
        return log_files


# Instância global do logger
logger = AetherLogger()


def get_logger(name: Optional[str] = None) -> AetherLogger:
    """
    Obtém uma instância do logger.
    
    Args:
        name: Nome do logger (opcional)
        
    Returns:
        Instância do AetherLogger
    """
    if name:
        return AetherLogger(name)
    return logger


# Funções de conveniência
def log_telemetry(payload: TelemetryPayload) -> None:
    """Log de telemetria usando o logger global."""
    logger.log_telemetry(payload)


def log_connection(source: str, status: str, details: Optional[str] = None) -> None:
    """Log de conexão usando o logger global."""
    logger.log_connection(source, status, details)


def log_performance(operation: str, duration: float, **kwargs) -> None:
    """Log de performance usando o logger global."""
    logger.log_performance(operation, duration, **kwargs)