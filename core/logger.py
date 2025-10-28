"""
Sistema de logging para AETHER.
Configura logging básico com rotação e diferentes níveis.
"""

import logging
import os
from datetime import datetime
from pathlib import Path


def setup_logger(name: str = "aether", level: str = "INFO") -> logging.Logger:
    """Configura e retorna um logger para o AETHER.
    
    Args:
        name: Nome do logger
        level: Nível de log (DEBUG, INFO, WARNING, ERROR, CRITICAL)
    
    Returns:
        Logger configurado
    """
    # Criar diretório de logs se não existir
    log_dir = Path("logs")
    log_dir.mkdir(exist_ok=True)
    
    # Configurar logger
    logger = logging.getLogger(name)
    logger.setLevel(getattr(logging, level.upper()))
    
    # Evitar duplicar handlers
    if logger.handlers:
        return logger
    
    # Formato das mensagens
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    # Handler para arquivo (com rotação)
    log_file = log_dir / f"aether_{datetime.now().strftime('%Y%m%d')}.log"
    file_handler = logging.FileHandler(log_file, encoding='utf-8')
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)
    
    # Handler para console
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)
    
    # Adicionar handlers
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    
    return logger


def log_telemetry(logger: logging.Logger, payload: dict) -> None:
    """Log de telemetria de forma estruturada.
    
    Args:
        logger: Logger configurado
        payload: TelemetryPayload do sistema
    """
    sensors_data = {}
    for name, sensor in payload.get("sensors", {}).items():
        sensors_data[name] = {
            "value": sensor.get("value"),
            "unit": sensor.get("unit"),
            "ok": sensor.get("ok")
        }
    
    logger.info(f"Telemetry - Source: {payload.get('source')} - "
                f"Sensors: {len(sensors_data)} - "
                f"Errors: {len(payload.get('errors', []))}")
    
    if payload.get("errors"):
        logger.warning(f"Telemetry errors: {payload['errors']}")


# Logger padrão do sistema
default_logger = setup_logger()
