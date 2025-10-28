# 🌌 AETHER – Estrutura do Projeto

## 🧠 1. Visão Geral
- Dashboard automotivo via OBD-II Bluetooth  
- Exibição de dados da ECU em tempo real  
- Dois modos de visualização:  
  - 🖥️ Interface Web (Streamlit)  
  - 💻 Interface Terminal (TUI estilo htop)  
- Modular, expansível e multiplataforma  

---

## ⚙️ 2. Núcleo (`core/`)

### 📡 `obd_reader.py`
- Responsável pela conexão com o adaptador OBD-II via Bluetooth  
- Leitura dos dados do veículo em tempo real  
- Funções principais:  
  - `connect()` → estabelece a comunicação  
  - `read_data()` → coleta dados de RPM, temperatura, etc.

### 📊 `data_manager.py`
- Formata, limpa e normaliza os dados recebidos da ECU  
- Prepara as informações para exibição  
- Funções: `format_data()`, `sanitize()`

### 🧭 `sensor_map.py`
- Mapeia os sensores OBD-II e seus respectivos PIDs  
- Armazena descrições e unidades de medida  
- Facilita a adição de novos sensores  

### 🪶 `logger.py`
- Gera logs e histórico de leituras  
- Armazena dados com timestamp  
- Pode exportar relatórios  

### 💾 `storage.py`
- Gerencia o armazenamento persistente (CSV, SQLite, etc.)  
- Facilita o backup e análise posterior  

---

## 🖥️ 3. Interface (`ui/`)

### 🌐 `streamlit_dashboard.py`
- Dashboard interativo em **Streamlit**  
- Atualização em tempo real e visualização gráfica dos dados  
- Contém funções para exibir gauges, gráficos e indicadores  

### 💻 `terminal_dashboard.py`
- Interface **TUI** estilo *htop*, voltada para Linux  
- Atualização dinâmica via `rich` ou `textual`  
- Exibe dados básicos do veículo em modo texto  

### 🧱 `widgets/`
- Contém componentes customizados do dashboard (ex: velocímetro, barras de status)

### 📈 `charts/`
- Gráficos e visualizações customizadas (usando `matplotlib` ou `plotly`)  

---

## 🧰 4. Utilitários (`utils/`)

### ⚙️ `config.py`
- Define configurações gerais do projeto  
- Lê variáveis do `.env`  

### 🧾 `constants.py`
- Contém constantes globais (nome, versão, unidades de medida, etc.)

### 🔧 `helpers.py`
- Funções auxiliares, como formatadores de valores e validações  

---

## 🧪 5. Testes (`tests/`)

### 🧩 `test_obd_reader.py`
- Testa conexão com o adaptador OBD-II  
- Verifica leitura e parsing de dados  

### 🧩 `test_data_manager.py`
- Testa integridade e formatação de dados  

---

## 💼 6. Interface de Linha de Comando

### 🧠 `cli.py`
- Controla a inicialização do sistema  
- Aceita argumentos como:  
  - `--ui streamlit`  
  - `--ui terminal`  

### 🚀 `main.py`
- Ponto de entrada principal  
- Inicia o modo de exibição conforme parâmetro  

---

## 🧩 7. Recursos e Mídia (`assets/`)

### 🖼️ `preview.png`
- Imagem de demonstração do dashboard (para README)

### 🧃 `images/`
- Logos, ícones e recursos visuais do projeto  
- Exemplo: `aether_logo.png`

---

## 🔒 8. Configurações

### ⚙️ `.env`
- Contém variáveis de ambiente:
  - `OBD_DEVICE=rfcomm0`
  - `REFRESH_RATE=1.0`  
- Protege informações sensíveis e facilita personalização  

---

## 📄 9. Documentação e Dependências

### 📘 `README.md`
- Descrição geral do projeto  
- Instruções de uso e instalação  
- Licença MIT  

### 📦 `requirements.txt`
- Lista de dependências:  
  - `python-obd`  
  - `streamlit`  
  - `rich`  
  - `textual`  
  - `dotenv`  

---

## 🌟 10. Licença
Distribuído sob a **Licença MIT** © 2025 Eduh Giaretta.  
Livre para uso, modificação e distribuição, desde que mantidos os créditos originais.

---

## 🧭 11. Objetivo
O **AETHER** busca unir tecnologia e clareza, tornando visível o que acontece sob o capô.  
Um projeto para compreender, visualizar e sentir o fluxo de dados automotivos de forma intuitiva e moderna.
