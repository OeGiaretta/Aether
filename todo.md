# ✅ TODO – AETHER Project Roadmap

> **Versão:** 1.0  
> **Licença:** MIT  
> **Descrição:** Sistema de dashboard automotivo via OBD-II Bluetooth com modos Web (Streamlit) e Terminal (TUI).

---

## 📊 Progresso Geral

| Etapa | Progresso | Barra |
|:------|:-----------:|:------|
| Core | 90% | █████████░ |
| UI Streamlit | 95% | ██████████░ |
| UI Terminal (TUI) | 0% | ░░░░░░░░░░░ |
| Utils | 60% | ██████░░░░░ |
| Testes | 0% | ░░░░░░░░░░░ |
| Documentação | 70% | ███████░░░░ |
| Assets | 50% | █████░░░░░░ |
| CLI / Main | 40% | ████░░░░░░░ |

**Progresso total estimado:**  
🟢 **75% concluído** — dashboard Streamlit completo com gauges, gráficos, logs, storage e componentes visuais implementados.

---

## 🎉 Conquistas Recentes

### ✅ **Sessão Atual - Dashboard Completo**
- **Dashboard Streamlit profissional** com layout responsivo e sidebar
- **6 gauges visuais interativos** para dados automotivos críticos
- **Sistema de logs centralizado** com rotação automática de arquivos
- **Sistema de armazenamento CSV** com estatísticas e exportação
- **Gráficos de histórico** e matriz de correlação com Plotly
- **Sistema de alertas** em tempo real para condições críticas
- **Componentes visuais personalizados** (cards, indicadores, barras de progresso)
- **Integração completa** entre todos os módulos do sistema

### 📊 **Métricas de Progresso**
- **Core:** 60% → 90% (+30%)
- **UI Streamlit:** 10% → 95% (+85%)
- **Utils:** 40% → 60% (+20%)
- **Documentação:** 60% → 70% (+10%)
- **CLI/Main:** 30% → 40% (+10%)

---

## 🧠 Estrutura do Desenvolvimento

### 📦 Etapa 1 — Núcleo do Sistema (Core)
- [X] Definir contrato de dados (payload padrão, unidades, flags `ok`, `errors`)  
- [X] `sensor_map.py` — mapeamento de PIDs, unidades e faixas válidas  
- [X] `obd_reader.py` — implementar `MockObdReader` primeiro (geração de sinais plausíveis)  
- [X] `data_manager.py` — normalização, conversões e clamps por faixa  
- [x] `logger.py` — registro de logs e erros  
- [x] `storage.py` — armazenamento local (CSV mínimo, preparar para SQLite depois)  

> ✅ **Progresso:** 90% — Sistema completo com mock reader, logs, storage e integração total  

---

### 🖥️ Etapa 2 — Interface de Usuário (UI)

#### 🌐 Modo Web – Streamlit
- [x] `streamlit_dashboard.py` — layout e gauges  
- [x] `widgets/` — componentes visuais (cards, indicadores, gauges)  
- [x] `charts/` — gráficos de histórico  
- [x] Sistema de alertas em tempo real
- [x] Sidebar com controles e estatísticas
- [x] Integração completa com logs e storage

> ✅ **Progresso:** 95% — Dashboard profissional completo com todas as funcionalidades principais  

#### 💻 Modo Terminal – TUI
- [ ] `terminal_dashboard.py` — interface estilo *htop*  
> ⏳ **Progresso:** 0% — iniciar após Streamlit MVP (usar `rich` inicialmente)  

---

### 🧰 Etapa 3 — Utilitários e Suporte (Utils)
- [x] `config.py` — parâmetros de conexão e refresh  
- [x] `types.py` — definição de contratos de dados (TypedDict, Protocol)  
- [ ] `constants.py` — definição de PIDs e nomes de sensores  
- [ ] `helpers.py` — funções auxiliares  
- [x] Integração com sistema de logs
- [x] Integração com sistema de storage

> ⚙️ **Progresso:** 60%  

---

### 🧪 Etapa 4 — Testes
- [ ] `test_sensor_map.py` — valida metadados e faixas  
- [ ] `test_data_manager.py` — normalização e conversões  
- [ ] `test_obd_reader_mock.py` — geração de sinais e contrato  
- [ ] `test_obd_reader.py` (integração) — OBD real quando disponível  

> 🧱 **Progresso:** 0% — aguardando núcleo estável  

---

### 🖼️ Etapa 5 — Recursos (Assets)
- [x] `logo.png` — logo oficial  
- [x] `preview.png` — prévia do dashboard  
- [ ] `assets/images/` — ícones e gráficos adicionais  

> 🎨 **Progresso:** 40%  

---

### 🚀 Etapa 6 — Execução e CLI
- [x] `dev_run.py` — script de teste do fluxo mock → data_manager  
- [ ] `cli.py` — flags `--ui streamlit|terminal` e `--source mock|obd` (fallback automático)  
- [ ] `main.py` — inicialização central com fallback para `mock` se OBD falhar  
- [x] Integração com dashboard Streamlit
- [x] Sistema de logs integrado

> ⚡ **Progresso:** 40%  

---

### 🧩 Etapa 7 — Documentação
- [x] `README.md` — descrição geral  
- [x] `AETHER_Arquitetura.md` — mapa do sistema  
- [x] `todo.md` — roadmap detalhado do projeto
- [ ] Documentação de API  
- [ ] Guia de instalação e uso  
- [ ] Guia OBD-II multi-OS (Windows/macOS/Linux): pareamento, porta serial, permissões  
- [ ] Troubleshooting: timeouts, COM/tty incorreto, permissões e drivers  
- [ ] Tabela de PIDs suportados no MVP  

> 📚 **Progresso:** 70%  

---

### 🔮 Etapa 8 — Melhorias Futuras
- [ ] Suporte Wi-Fi OBD-II  
- [ ] Registro de trajetos  
- [ ] Dashboard mobile  
- [ ] Alertas configuráveis  
- [ ] Exportação de logs via interface  

---

## 📅 Próximos Passos
1. ✅ ~~Finalizar `utils/constants.py` e `core/sensor_map.py` (PIDs e faixas)~~  
2. ✅ ~~Definir contrato de dados entre `obd_reader` → `data_manager` → UI~~  
3. ✅ ~~Implementar `MockObdReader` e habilitar `--source mock`~~  
4. ✅ ~~Implementar `data_manager` (normalização, conversões, clamps)~~  
5. ✅ ~~Criar Streamlit MVP (3–5 PIDs, histórico curto)~~  
6. ✅ ~~Adicionar logs e storage mínimos (CSV)~~  
7. **🎯 PRIORIDADE:** Implementar `cli.py`/`main.py` com flags e fallback automático  
8. **🎯 PRIORIDADE:** Implementar OBD real (ELM327) com fallback para mock  
9. **🎯 PRIORIDADE:** Adicionar TUI básico após MVP Web  
10. **🧪 IMPORTANTE:** Criar bateria de testes (sensor_map, data_manager, mock, integração OBD)
11. **📚 DOCUMENTAÇÃO:** Criar guia de instalação e uso
12. **🔧 MELHORIAS:** Implementar `utils/constants.py` e `helpers.py`  

---

## 🧾 Observações
- O projeto segue licença **MIT**  
- Documentação com **docstrings** e **tipagem Python**  
- Compatível com **Python 3.10+**  
- Recomendado uso de **venv** e **requirements.txt**  

---

### 🏁 Status Final
> 🟢 **AETHER tem dashboard completo** — sistema Streamlit profissional com gauges, gráficos, logs, storage e componentes visuais implementados. Pronto para implementação de TUI e OBD real.  

---
