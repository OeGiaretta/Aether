#!/usr/bin/env python3
"""
Teste rápido do fluxo mock → data_manager → saída JSON.
Execute: python dev_run.py
"""

import json
import time
from core.obd_reader import MockObdReader
from core.data_manager import normalize


def main():
    print("🚗 AETHER - Teste do Mock Reader")
    print("=" * 40)
    
    # Inicializar leitor mock
    reader = MockObdReader()
    reader.connect()
    
    print(f"✅ Conectado: {reader.connected}")
    print(f"📡 Fonte: {reader.source}")
    print()
    
    try:
        # Loop de leitura
        for i in range(5):
            print(f"📊 Leitura {i+1}/5:")
            
            # Ler dados brutos
            raw_payload = reader.read()
            print(f"  Timestamp: {raw_payload['timestamp']:.2f}")
            print(f"  Sensores: {len(raw_payload['sensors'])}")
            
            # Normalizar dados
            normalized_payload = normalize(raw_payload)
            
            # Mostrar valores dos sensores
            print("  Valores:")
            for name, sensor in normalized_payload['sensors'].items():
                value = sensor['value']
                unit = sensor['unit']
                ok = sensor['ok']
                status = "✅" if ok else "❌"
                print(f"    {name:12}: {value:8.2f} {unit:6} {status}")
            
            # Mostrar erros se houver
            if normalized_payload['errors']:
                print("  ⚠️  Erros:")
                for error in normalized_payload['errors']:
                    print(f"    - {error}")
            
            print()
            time.sleep(1.0)
            
    except KeyboardInterrupt:
        print("\n⏹️  Interrompido pelo usuário")
    except Exception as e:
        print(f"\n❌ Erro: {e}")
    finally:
        reader.close()
        print("🔌 Conexão fechada")


if __name__ == "__main__":
    main()
