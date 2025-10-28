# ✅ TODO – AETHER Project Roadmap

> **Versão:** 1.0  
> **Licença:** MIT  
> **Descrição:** Sistema de dashboard automotivo via OBD-II Bluetooth com modos Web (Streamlit) e Terminal (TUI).

---

## 📊 Progresso Geral

| Etapa | Progresso | Barra |
|:------|:-----------:|:------|
| Core | 20% | ███░░░░░░░░ |
| UI Streamlit | 10% | ██░░░░░░░░░ |
| UI Terminal (TUI) | 0% | ░░░░░░░░░░░ |
| Utils | 15% | ███░░░░░░░░ |
| Testes | 0% | ░░░░░░░░░░░ |
| Documentação | 60% | ███████░░░░ |
| Assets | 40% | █████░░░░░░ |
| CLI / Main | 25% | ████░░░░░░░ |

**Progresso total estimado:**  
🟣 **32% concluído** — o projeto está em fase inicial, com documentação sólida e arquitetura definida.

---

## 🧠 Estrutura do Desenvolvimento

### 📦 Etapa 1 — Núcleo do Sistema (Core)
- [ ] `obd_reader.py` — leitura dos dados via OBD-II Bluetooth  
- [ ] `data_manager.py` — processamento e normalização dos dados  
- [ ] `sensor_map.py` — mapeamento de PIDs e unidades  
- [ ] `logger.py` — registro de logs e erros  
- [ ] `storage.py` — armazenamento local e histórico  

> ⏳ **Progresso:** 20% — arquitetura pronta, leitura OBD em planejamento  

---

### 🖥️ Etapa 2 — Interface de Usuário (UI)

#### 🌐 Modo Web – Streamlit
- [ ] `streamlit_dashboard.py` — layout e gauges  
- [ ] `widgets/` — componentes visuais (cards, indicadores, gauges)  
- [ ] `charts/` — gráficos de histórico  

> ⏳ **Progresso:** 10% — estrutura base em criação  

#### 💻 Modo Terminal – TUI
- [ ] `terminal_dashboard.py` — interface estilo *htop*  
> ⏳ **Progresso:** 0% — aguardando definição da biblioteca (`rich` ou `textual`)  

---

### 🧰 Etapa 3 — Utilitários e Suporte (Utils)
- [x] `config.py` — parâmetros de conexão e refresh  
- [ ] `constants.py` — definição de PIDs e nomes de sensores  
- [ ] `helpers.py` — funções auxiliares  

> ⚙️ **Progresso:** 15%  

---

### 🧪 Etapa 4 — Testes
- [ ] `test_obd_reader.py` — simulação de leitura e falhas  
- [ ] `test_data_manager.py` — validação de conversões  

> 🧱 **Progresso:** 0% — aguardando núcleo estável  

---

### 🖼️ Etapa 5 — Recursos (Assets)
- [x] `logo.png` — logo oficial  
- [x] `preview.png` — prévia do dashboard  
- [ ] `assets/images/` — ícones e gráficos adicionais  

> 🎨 **Progresso:** 40%  

---

### 🚀 Etapa 6 — Execução e CLI
- [ ] `cli.py` — interface de linha de comando (`--web`, `--tui`)  
- [ ] `main.py` — inicialização central  

> ⚡ **Progresso:** 25%  

---

### 🧩 Etapa 7 — Documentação
- [x] `README.md` — descrição geral  
- [x] `AETHER_Arquitetura.md` — mapa do sistema  
- [ ] Documentação de API  
- [ ] Guia de instalação e uso  

> 📚 **Progresso:** 60%  

---

### 🔮 Etapa 8 — Melhorias Futuras
- [ ] Suporte Wi-Fi OBD-II  
- [ ] Registro de trajetos  
- [ ] Dashboard mobile  
- [ ] Alertas configuráveis  
- [ ] Exportação de logs via interface  

---

## 📅 Próximos Passos
1. Implementar `obd_reader` e `data_manager` com leitura real via ELM327  
2. Criar dashboard Streamlit mínimo funcional  
3. Adicionar TUI básico  
4. Registrar logs e histórico  
5. Testar comunicação multiplataforma  

---

## 🧾 Observações
- O projeto segue licença **MIT**  
- Documentação com **docstrings** e **tipagem Python**  
- Compatível com **Python 3.10+**  
- Recomendado uso de **venv** e **requirements.txt**  

---

### 🏁 Status Final
> 🔵 **AETHER está em fase de fundação** — a estrutura foi consolidada, o design de arquitetura finalizado e a fase de integração OBD-II está prestes a começar.  

---
