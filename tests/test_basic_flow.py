"""
Teste básico do fluxo AETHER.
Valida integração entre mock reader, data manager e storage.
"""

import sys
import os
from pathlib import Path

# Adicionar diretório raiz ao path
sys.path.append(str(Path(__file__).parent.parent))

from core.obd_reader import MockObdReader
from core.data_manager import normalize
from core.storage import append_csv, get_file_stats
from core.logger import setup_logger


def test_mock_reader():
    """Testa MockObdReader."""
    print("🧪 Testando MockObdReader...")
    
    reader = MockObdReader()
    reader.connect()
    
    # Testar leitura
    payload = reader.read()
    
    # Validar estrutura
    assert "timestamp" in payload
    assert "sensors" in payload
    assert "source" in payload
    assert payload["source"] == "mock"
    
    # Validar sensores
    expected_sensors = ["rpm", "speed", "coolant_temp", "throttle", "engine_load", "intake_temp", "map"]
    for sensor in expected_sensors:
        assert sensor in payload["sensors"]
        sensor_data = payload["sensors"][sensor]
        assert "value" in sensor_data
        assert "unit" in sensor_data
        assert "ok" in sensor_data
    
    reader.close()
    print("✅ MockObdReader OK")


def test_data_manager():
    """Testa normalização de dados."""
    print("🧪 Testando data_manager...")
    
    reader = MockObdReader()
    reader.connect()
    
    raw_payload = reader.read()
    normalized_payload = normalize(raw_payload)
    
    # Validar que normalização mantém estrutura
    assert "timestamp" in normalized_payload
    assert "sensors" in normalized_payload
    assert "source" in normalized_payload
    assert "errors" in normalized_payload
    
    # Validar que sensores têm valores válidos
    for name, sensor in normalized_payload["sensors"].items():
        assert sensor["value"] is not None
        assert isinstance(sensor["value"], (int, float))
        assert isinstance(sensor["ok"], bool)
    
    reader.close()
    print("✅ data_manager OK")


def test_storage():
    """Testa sistema de armazenamento."""
    print("🧪 Testando storage...")
    
    reader = MockObdReader()
    reader.connect()
    
    payload = normalize(reader.read())
    
    # Testar salvamento
    append_csv(payload, "test_telemetry.csv")
    
    # Testar leitura
    stats = get_file_stats("test_telemetry.csv")
    assert stats["exists"]
    assert stats["records"] > 0
    
    reader.close()
    print("✅ storage OK")


def test_logger():
    """Testa sistema de logging."""
    print("🧪 Testando logger...")
    
    logger = setup_logger("test", "INFO")
    logger.info("Teste de logging")
    
    print("✅ logger OK")


def main():
    """Executa todos os testes."""
    print("🚀 AETHER - Teste de Integração Básica")
    print("=" * 40)
    
    try:
        test_mock_reader()
        test_data_manager()
        test_storage()
        test_logger()
        
        print("\n🎉 Todos os testes passaram!")
        print("✅ Sistema pronto para uso")
        
    except Exception as e:
        print(f"\n❌ Teste falhou: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
