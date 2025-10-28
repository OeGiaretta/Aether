# ✅ TODO – AETHER Project Roadmap

> **Versão:** 1.0  
> **Licença:** MIT  
> **Descrição:** Sistema de dashboard automotivo via OBD-II Bluetooth com modos Web (Streamlit) e Terminal (TUI).

---

## 📊 Progresso Geral

| Etapa | Progresso | Barra |
|:------|:-----------:|:------|
| Core | 60% | ██████░░░░░ |
| UI Streamlit | 10% | ██░░░░░░░░░ |
| UI Terminal (TUI) | 0% | ░░░░░░░░░░░ |
| Utils | 40% | ████░░░░░░░ |
| Testes | 0% | ░░░░░░░░░░░ |
| Documentação | 60% | ███████░░░░ |
| Assets | 40% | █████░░░░░░ |
| CLI / Main | 30% | ███░░░░░░░░ |

**Progresso total estimado:**  
🟢 **45% concluído** — núcleo funcional com mock reader e contrato de dados implementados.

---

## 🧠 Estrutura do Desenvolvimento

### 📦 Etapa 1 — Núcleo do Sistema (Core)
- [X] Definir contrato de dados (payload padrão, unidades, flags `ok`, `errors`)  
- [X] `sensor_map.py` — mapeamento de PIDs, unidades e faixas válidas  
- [X] `obd_reader.py` — implementar `MockObdReader` primeiro (geração de sinais plausíveis)  
- [X] `data_manager.py` — normalização, conversões e clamps por faixa  
- [ ] `logger.py` — registro de logs e erros  
- [ ] `storage.py` — armazenamento local (CSV mínimo, preparar para SQLite depois)  

> ✅ **Progresso:** 60% — Mock reader funcional, contrato de dados e normalização implementados  

---

### 🖥️ Etapa 2 — Interface de Usuário (UI)

#### 🌐 Modo Web – Streamlit
- [ ] `streamlit_dashboard.py` — layout e gauges  
- [ ] `widgets/` — componentes visuais (cards, indicadores, gauges)  
- [ ] `charts/` — gráficos de histórico  

> ⏳ **Progresso:** 10% — MVP primeiro (3–5 PIDs), histórico curto  

#### 💻 Modo Terminal – TUI
- [ ] `terminal_dashboard.py` — interface estilo *htop*  
> ⏳ **Progresso:** 0% — iniciar após Streamlit MVP (usar `rich` inicialmente)  

---

### 🧰 Etapa 3 — Utilitários e Suporte (Utils)
- [x] `config.py` — parâmetros de conexão e refresh  
- [x] `types.py` — definição de contratos de dados (TypedDict, Protocol)  
- [ ] `constants.py` — definição de PIDs e nomes de sensores  
- [ ] `helpers.py` — funções auxiliares  

> ⚙️ **Progresso:** 40%  

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

> ⚡ **Progresso:** 30%  

---

### 🧩 Etapa 7 — Documentação
- [x] `README.md` — descrição geral  
- [x] `AETHER_Arquitetura.md` — mapa do sistema  
- [ ] Documentação de API  
- [ ] Guia de instalação e uso  
- [ ] Guia OBD-II multi-OS (Windows/macOS/Linux): pareamento, porta serial, permissões  
- [ ] Troubleshooting: timeouts, COM/tty incorreto, permissões e drivers  
- [ ] Tabela de PIDs suportados no MVP  

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
1. ✅ ~~Finalizar `utils/constants.py` e `core/sensor_map.py` (PIDs e faixas)~~  
2. ✅ ~~Definir contrato de dados entre `obd_reader` → `data_manager` → UI~~  
3. ✅ ~~Implementar `MockObdReader` e habilitar `--source mock`~~  
4. ✅ ~~Implementar `data_manager` (normalização, conversões, clamps)~~  
5. Criar Streamlit MVP (3–5 PIDs, histórico curto)  
6. Adicionar logs e storage mínimos (CSV)  
7. Implementar `cli.py`/`main.py` com flags e fallback automático  
8. Implementar OBD real (ELM327) com fallback para mock  
9. Adicionar TUI básico após MVP Web  
10. Criar bateria de testes (sensor_map, data_manager, mock, integração OBD)  

---

## 🧾 Observações
- O projeto segue licença **MIT**  
- Documentação com **docstrings** e **tipagem Python**  
- Compatível com **Python 3.10+**  
- Recomendado uso de **venv** e **requirements.txt**  

---

### 🏁 Status Final
> 🟢 **AETHER tem núcleo funcional** — mock reader, contrato de dados e normalização implementados. Pronto para desenvolvimento da interface Streamlit MVP.  

---
