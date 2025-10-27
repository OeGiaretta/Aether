# ✅ TODO – AETHER Project Roadmap

> **Versão:** 1.0  
> **Licença:** MIT  
> **Descrição:** Sistema de dashboard automotivo via OBD-II Bluetooth com modos Web (Streamlit) e Terminal (TUI).

---

## 🧩 Visão Geral

AETHER é um projeto modular que conecta-se à ECU do carro via OBD-II Bluetooth, processa e exibe dados do veículo em tempo real.  
O objetivo é oferecer duas interfaces:  
- **Streamlit Dashboard:** visual moderno e interativo.  
- **Terminal Dashboard (TUI):** estilo *htop* para uso em Linux ou sistemas embarcados.  

---

## 🧠 Estrutura do Desenvolvimento

### 📦 Etapa 1 — Núcleo do Sistema (Core)
- [ ] Criar módulo `obd_reader.py`  
	- [ ] Configurar conexão Bluetooth com adaptador OBD-II  
	- [ ] Ler PIDs e traduzir dados crus da ECU  
	- [ ] Enviar dados para `data_manager`  
	- [ ] Implementar tratamento de exceções de conexão  

- [ ] Desenvolver `data_manager.py`  
	- [ ] Converter dados crus em informações utilizáveis  
	- [ ] Normalizar unidades (°C, km/h, RPM, etc.)  
	- [ ] Integrar com `sensor_map.py`  

- [ ] Implementar `sensor_map.py`  
	- [ ] Criar mapeamento de sensores e PIDs  
	- [ ] Adicionar unidades e descrições  

- [ ] Criar `logger.py`  
	- [ ] Registrar eventos e erros em arquivo de log  
	- [ ] Implementar opção de exportação para CSV  

- [ ] Implementar `storage.py`  
	- [ ] Armazenar histórico local de medições (JSON/CSV)  
	- [ ] Estrutura para futuras integrações SQLite  

---

### 🖥️ Etapa 2 — Interface de Usuário (UI)

#### 🌐 Modo Web – Streamlit
- [ ] Criar `streamlit_dashboard.py`  
	- [ ] Interface com gauges, gráficos e cards  
	- [ ] Atualização em tempo real dos valores  
	- [ ] Tema dark e responsivo  

- [ ] Criar componentes reutilizáveis (`widgets/`)  
	- [ ] Gauge de RPM  
	- [ ] Indicadores de temperatura e velocidade  
	- [ ] Cards de status  

- [ ] Criar `charts/`  
	- [ ] Gráficos de linha para histórico  
	- [ ] Suporte a múltiplos sensores  

#### 💻 Modo Terminal – TUI
- [ ] Criar `terminal_dashboard.py`  
	- [ ] Layout estilo *htop*  
	- [ ] Atualização automática a cada 0.5s  
	- [ ] Uso de cores ANSI ou `rich`  

---

### 🧰 Etapa 3 — Utilitários e Suporte (Utils)
- [ ] Criar `config.py`  
	- [ ] Parâmetros do Bluetooth e tempo de atualização  

- [ ] Criar `constants.py`  
	- [ ] Definir constantes e nomes de sensores  

- [ ] Criar `helpers.py`  
	- [ ] Funções auxiliares de conversão e formatação  

---

### 🧪 Etapa 4 — Testes
- [ ] Criar `test_obd_reader.py`  
	- [ ] Mock de conexão OBD-II  
	- [ ] Testes de leitura e falhas  

- [ ] Criar `test_data_manager.py`  
	- [ ] Validação das conversões e unidades  

---

### 🖼️ Etapa 5 — Recursos (Assets)
- [ ] Adicionar logo e ícones do projeto  
- [ ] Inserir `preview.png` no README  
- [ ] Criar diretório `assets/images/`  

---

### 🚀 Etapa 6 — Execução e CLI
- [ ] Criar `cli.py`  
	- [ ] Permitir escolher modo (`--web` ou `--tui`)  
	- [ ] Exibir ajuda e versão  

- [ ] Criar `main.py`  
	- [ ] Integrar todos os módulos  
	- [ ] Inicializar de acordo com modo selecionado  

---

### 🧩 Etapa 7 — Documentação
- [x] Criar `README.md` inicial  
- [x] Definir arquitetura do projeto (`AETHER_Arquitetura.md`)  
- [ ] Criar documentação de API e fluxo de dados  
- [ ] Adicionar instruções de instalação e uso  

---

### 🔮 Etapa 8 — Melhorias Futuras
- [ ] Suporte a Wi-Fi OBD-II  
- [ ] Registro de trajetos e consumo médio  
- [ ] Dashboard mobile responsivo  
- [ ] Alertas configuráveis (ex: temperatura alta)  
- [ ] Exportação de logs via interface  

---

## 📊 Status Geral

| Módulo | Progresso | Prioridade |
|--------|------------|-------------|
| Core | 🔧 Em planejamento | 🔴 Alta |
| UI Streamlit | ⚙️ Estrutura inicial | 🟠 Média |
| UI Terminal | 💤 Pendente | 🟡 Média |
| Utils | 🚧 Em definição | 🟢 Baixa |
| Testes | ❌ Não iniciado | 🟢 Baixa |
| Documentação | ✅ Em andamento | 🟢 Alta |

---

## 📅 Próximos Passos
1. Implementar `obd_reader` e `data_manager` com leitura real via ELM327.  
2. Criar dashboard Streamlit mínimo funcional.  
3. Adicionar TUI básico usando `rich` ou `textual`.  
4. Registrar logs e histórico.  
5. Testar comunicação em diferentes plataformas.  

---

## 🧾 Observações
- O projeto segue licença **MIT**.  
- Todos os módulos devem ser documentados com **docstrings** e tipagem Python.  
- Manter compatibilidade com **Python 3.10+**.  
- Recomendado uso de **venv** e **requirements.txt** para dependências.  

---
