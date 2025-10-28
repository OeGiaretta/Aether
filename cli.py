"""
Interface de linha de comando para AETHER.
Define argumentos e configurações para execução.
"""

import argparse
import os
from typing import Dict, Any


def parse_args() -> argparse.Namespace:
    """Parse argumentos da linha de comando.
    
    Returns:
        Namespace com argumentos parseados
    """
    parser = argparse.ArgumentParser(
        description="AETHER - Dashboard Automotivo Inteligente",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemplos:
  python main.py --ui streamlit --source mock
  python main.py --ui terminal --source obd
  python main.py  # usa padrões: streamlit + mock
        """
    )
    
    # Interface de usuário
    parser.add_argument(
        "--ui",
        choices=["streamlit", "terminal"],
        default="streamlit",
        help="Interface de usuário (padrão: streamlit)"
    )
    
    # Fonte de dados
    parser.add_argument(
        "--source",
        choices=["mock", "obd"],
        default="mock",
        help="Fonte de dados (padrão: mock)"
    )
    
    # Configurações de dispositivo
    parser.add_argument(
        "--device",
        type=str,
        help="Dispositivo OBD (ex: COM3, /dev/rfcomm0)"
    )
    
    # Taxa de atualização
    parser.add_argument(
        "--refresh-rate",
        type=float,
        default=1.0,
        help="Taxa de atualização em segundos (padrão: 1.0)"
    )
    
    # Modo debug
    parser.add_argument(
        "--debug",
        action="store_true",
        help="Ativar modo debug com logs detalhados"
    )
    
    # Porta do Streamlit
    parser.add_argument(
        "--port",
        type=int,
        default=8501,
        help="Porta do Streamlit (padrão: 8501)"
    )
    
    return parser.parse_args()


def load_env_config() -> Dict[str, Any]:
    """Carrega configurações do arquivo .env se existir.
    
    Returns:
        Dicionário com configurações
    """
    config = {}
    
    try:
        from dotenv import load_dotenv
        load_dotenv()
        
        config = {
            "source": os.getenv("SOURCE", "mock"),
            "device": os.getenv("OBD_DEVICE"),
            "refresh_rate": float(os.getenv("REFRESH_RATE", "1.0")),
            "debug": os.getenv("DEBUG", "false").lower() == "true"
        }
    except ImportError:
        # python-dotenv não instalado, usar padrões
        pass
    
    return config


def merge_config(args: argparse.Namespace, env_config: Dict[str, Any]) -> Dict[str, Any]:
    """Mescla argumentos CLI com configurações do .env.
    
    Args:
        args: Argumentos da CLI
        env_config: Configurações do .env
    
    Returns:
        Configuração final mesclada
    """
    config = {
        "ui": args.ui,
        "source": args.source or env_config.get("source", "mock"),
        "device": args.device or env_config.get("device"),
        "refresh_rate": args.refresh_rate or env_config.get("refresh_rate", 1.0),
        "debug": args.debug or env_config.get("debug", False),
        "port": args.port
    }
    
    return config


def print_config(config: Dict[str, Any]) -> None:
    """Imprime configuração atual.
    
    Args:
        config: Configuração a ser exibida
    """
    print("🔧 Configuração AETHER:")
    print(f"  Interface: {config['ui']}")
    print(f"  Fonte: {config['source']}")
    if config['device']:
        print(f"  Dispositivo: {config['device']}")
    print(f"  Refresh Rate: {config['refresh_rate']}s")
    print(f"  Debug: {config['debug']}")
    if config['ui'] == "streamlit":
        print(f"  Porta: {config['port']}")
    print()


if __name__ == "__main__":
    # Teste da CLI
    args = parse_args()
    env_config = load_env_config()
    config = merge_config(args, env_config)
    print_config(config)
