"""
Ponto de entrada principal do AETHER.
Coordena execução entre diferentes interfaces e fontes de dados.
"""

import subprocess
import sys
import os
from pathlib import Path

from cli import parse_args, load_env_config, merge_config, print_config
from core.logger import setup_logger


def run_streamlit(port: int = 8501) -> None:
    """Executa interface Streamlit.
    
    Args:
        port: Porta do Streamlit
    """
    dashboard_path = Path("ui") / "streamlit_dashboard.py"
    
    if not dashboard_path.exists():
        print("❌ Erro: streamlit_dashboard.py não encontrado!")
        sys.exit(1)
    
    print(f"🌐 Iniciando Streamlit na porta {port}...")
    print(f"📱 Acesse: http://localhost:{port}")
    print("⏹️  Para parar: Ctrl+C")
    print()
    
    try:
        subprocess.run([
            sys.executable, "-m", "streamlit", "run",
            str(dashboard_path),
            "--server.port", str(port),
            "--server.headless", "true"
        ], check=True)
    except KeyboardInterrupt:
        print("\n⏹️  Streamlit interrompido pelo usuário")
    except subprocess.CalledProcessError as e:
        print(f"❌ Erro ao executar Streamlit: {e}")
        sys.exit(1)


def run_terminal() -> None:
    """Executa interface Terminal (TUI).
    
    Nota: Implementação futura com rich/textual
    """
    print("💻 Interface Terminal ainda não implementada")
    print("🔄 Use --ui streamlit por enquanto")
    sys.exit(1)


def setup_reader(source: str, device: str = None, logger=None):
    """Configura leitor de dados baseado na fonte.
    
    Args:
        source: Fonte de dados ("mock" ou "obd")
        device: Dispositivo OBD (opcional)
        logger: Logger para mensagens
    
    Returns:
        Instância do leitor configurado
    """
    if source == "mock":
        from core.obd_reader import MockObdReader
        reader = MockObdReader()
        if logger:
            logger.info("Usando MockObdReader para desenvolvimento")
        return reader
    
    elif source == "obd":
        try:
            from core.obd_reader import RealObdReader
            reader = RealObdReader()
            if logger:
                logger.info(f"Tentando conectar OBD real no dispositivo: {device or 'padrão'}")
            return reader
        except ImportError:
            if logger:
                logger.warning("RealObdReader não implementado, usando MockObdReader")
            from core.obd_reader import MockObdReader
            return MockObdReader()
    
    else:
        raise ValueError(f"Fonte inválida: {source}")


def main():
    """Função principal do AETHER."""
    print("🌌 AETHER - Dashboard Automotivo Inteligente")
    print("=" * 50)
    
    # Parse argumentos e configurações
    args = parse_args()
    env_config = load_env_config()
    config = merge_config(args, env_config)
    
    # Configurar logger
    log_level = "DEBUG" if config["debug"] else "INFO"
    logger = setup_logger("aether", log_level)
    
    # Mostrar configuração
    print_config(config)
    
    # Configurar leitor
    try:
        reader = setup_reader(config["source"], config["device"], logger)
        logger.info(f"Leitor configurado: {reader.source}")
    except Exception as e:
        logger.error(f"Erro ao configurar leitor: {e}")
        print(f"❌ Erro: {e}")
        sys.exit(1)
    
    # Executar interface escolhida
    try:
        if config["ui"] == "streamlit":
            run_streamlit(config["port"])
        elif config["ui"] == "terminal":
            run_terminal()
        else:
            print(f"❌ Interface inválida: {config['ui']}")
            sys.exit(1)
            
    except KeyboardInterrupt:
        print("\n⏹️  AETHER interrompido pelo usuário")
        logger.info("Aplicação interrompida pelo usuário")
    except Exception as e:
        logger.error(f"Erro durante execução: {e}")
        print(f"❌ Erro: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
