# 🚀 Guia de Instalação - AETHER Dashboard

> **Sistema de dashboard automotivo via OBD-II com interface Web (Streamlit) e Terminal (TUI)**

---

## 📋 Pré-requisitos

### Sistema Operacional
- **Linux** (Ubuntu 20.04+, Fedora 35+, Debian 11+)
- **Windows** 10/11 (com WSL2 recomendado)
- **macOS** 11+ (Big Sur ou superior)

### Software Necessário
- **Python 3.10+** (recomendado: Python 3.11 ou 3.12)
- **Git** (para clonar o repositório)
- **pip** (gerenciador de pacotes Python)

### Hardware (Opcional)
- **Adaptador OBD-II** (ELM327 Bluetooth/USB) para dados reais
- **Dispositivo móvel** com Bluetooth (para pareamento OBD)

---

## 🔧 Instalação

### 1. Clonar o Repositório
```bash
git clone https://github.com/OeGiaretta/Aether.git
cd Aether
```

### 2. Criar Ambiente Virtual
```bash
# Criar ambiente virtual
python -m venv venv

# Ativar ambiente virtual
# Linux/macOS:
source venv/bin/activate
# Windows:
# venv\Scripts\activate
```

### 3. Instalar Dependências
```bash
pip install -r requirements.txt
```

### 4. Verificar Instalação
```bash
python -c "import streamlit, plotly, pandas; print('✅ Dependências instaladas com sucesso!')"
```

---

## 🚀 Execução

### Modo Web (Streamlit) - **Recomendado**
```bash
# Ativar ambiente virtual
source venv/bin/activate

# Executar dashboard
streamlit run ui/streamlit_dashboard.py
```

**Acesse:** http://localhost:8501

### Modo Desenvolvimento
```bash
# Executar com dados mock
python dev_run.py
```

---

## ⚙️ Configuração

### Variáveis de Ambiente (Opcional)
Crie um arquivo `.env` na raiz do projeto:
```env
# Configurações do OBD-II
OBD_DEVICE=/dev/ttyUSB0
OBD_BAUDRATE=38400
OBD_TIMEOUT=5

# Configurações do Dashboard
REFRESH_INTERVAL=5
LOG_LEVEL=INFO
DATA_RETENTION_DAYS=30
```

### Configuração OBD-II (Linux)
```bash
# Adicionar usuário ao grupo dialout (para acesso serial)
sudo usermod -a -G dialout $USER

# Verificar dispositivos OBD disponíveis
ls /dev/ttyUSB* /dev/ttyACM*

# Logout e login novamente para aplicar mudanças
```

---

## 🔍 Solução de Problemas

### Erro: "Permission denied" (Linux)
```bash
sudo chmod 666 /dev/ttyUSB0
# ou
sudo usermod -a -G dialout $USER
```

### Erro: "Module not found"
```bash
# Verificar se o ambiente virtual está ativo
which python
# Deve apontar para: /caminho/para/Aether/venv/bin/python

# Reinstalar dependências
pip install -r requirements.txt --force-reinstall
```

### Erro: "Port already in use"
```bash
# Usar porta diferente
streamlit run ui/streamlit_dashboard.py --server.port 8502
```

### OBD-II não conecta
1. **Verificar pareamento Bluetooth:**
   ```bash
   bluetoothctl
   scan on
   pair [MAC_ADDRESS]
   connect [MAC_ADDRESS]
   ```

2. **Testar conexão serial:**
   ```bash
   python -c "import serial; print(serial.Serial('/dev/ttyUSB0', 38400))"
   ```

---

## 📁 Estrutura de Arquivos

```
Aether/
├── core/                    # Núcleo do sistema
│   ├── obd_reader.py       # Leitor OBD-II (mock e real)
│   ├── data_manager.py     # Gerenciamento de dados
│   ├── logger.py           # Sistema de logs
│   └── storage.py          # Armazenamento de dados
├── ui/                     # Interfaces de usuário
│   ├── streamlit_dashboard.py
│   └── widgets/            # Componentes visuais
├── utils/                  # Utilitários
│   └── types.py           # Definições de tipos
├── data/                   # Dados armazenados
│   └── telemetry_data.csv
├── logs/                   # Arquivos de log
├── assets/                 # Recursos (imagens, etc.)
├── docs/                   # Documentação
└── requirements.txt        # Dependências Python
```

---

## 🎯 Próximos Passos

1. **Executar o dashboard** e explorar as funcionalidades
2. **Configurar OBD-II** para dados reais (opcional)
3. **Personalizar alertas** e configurações
4. **Explorar dados históricos** e estatísticas

---

## 📞 Suporte

- **Issues:** [GitHub Issues](https://github.com/OeGiaretta/Aether/issues)
- **Documentação:** [docs/](docs/)
- **Código:** [GitHub Repository](https://github.com/OeGiaretta/Aether)

---

**🎉 Instalação concluída! Aproveite o AETHER Dashboard!**
