

<h1 align="center">🌌 AETHER – Dashboard Automotivo Inteligente
</h1>
<p align="center">

  <b>Conecte-se ao coração do seu carro.</b><br>
  Diagnóstico automotivo moderno com visual futurista e integração OBD-II Bluetooth.
</p>

<p align="center">
  <img src="https://img.shields.io/badge/build-passing-00b894?style=flat-square"/>
  <img src="https://img.shields.io/badge/python-3.11%2B-0984e3?style=flat-square"/>
  <img src="https://img.shields.io/badge/license-MIT-6c5ce7?style=flat-square"/>
</p>

---

## 🚗 Sobre o Projeto

O **AETHER** é um sistema de diagnóstico automotivo inteligente que se conecta à **ECU do veículo via OBD-II Bluetooth**, exibindo dados em tempo real através de dois tipos de dashboards:

- 🖥️ **Interface Web (Streamlit)** — ideal para visualização no PC, com gráficos dinâmicos e indicadores em tempo real.  
- 💻 **Interface Terminal (TUI)** — estilo *htop/btop*, perfeita para Linux e embarcados como o Raspberry Pi.

O projeto une **tecnologia, design e performance**, servindo como ferramenta prática e também como estudo de integração entre **hardware automotivo e software inteligente**.

---

## 📦 Estrutura do Projeto

```
AETHER/
├── core/
│   ├── obd_reader.py
│   ├── data_manager.py
│   ├── sensor_map.py
│   ├── logger.py
│   ├── storage.py
│
├── ui/
│   ├── streamlit_dashboard.py
│   ├── terminal_dashboard.py
│   ├── widgets/
│   ├── charts/
│
├── utils/
│   ├── config.py
│   ├── constants.py
│   ├── helpers.py
│
├── tests/
│   ├── test_obd_reader.py
│   ├── test_data_manager.py
│
├── assets/
│   ├── images/
│   │   ├── aether_banner.png
│   ├── preview.png
│
├── cli.py
├── main.py
├── requirements.txt
├── README.md
└── .env
```

---

## ⚙️ Funcionalidades

- 📡 Conexão Bluetooth com adaptador OBD-II (ex: ELM327)  
- ⚙️ Leitura de PIDs como RPM, temperatura, velocidade etc.  
- 📊 Exibição em tempo real com gauges e gráficos  
- 🧾 Modo terminal TUI com atualização dinâmica (*btop/htop style*)  
- 💾 Registro de histórico e logs de telemetria  
- 🔌 Extensível via API e módulos externos (futuro)

---

## 🚀 Como Executar

### 1️⃣ Clonar o repositório
```bash
git clone https://github.com/SEU_USUARIO/AETHER.git
cd AETHER
````

### 2️⃣ Instalar dependências

```bash
pip install -r requirements.txt
```

### 3️⃣ Configurar o adaptador Bluetooth

Edite o arquivo `.env`:

```
OBD_DEVICE=rfcomm0
REFRESH_RATE=1.0
```

### 4️⃣ Rodar o dashboard

**Interface Terminal (TUI):**

```bash
python main.py --ui terminal
```

**Interface Web (Streamlit):**

```bash
python main.py --ui streamlit
```

---

## 🧠 Tecnologias Utilizadas

| Tipo          | Tecnologias                     |
| ------------- | ------------------------------- |
| Linguagem     | Python 3.11+                    |
| Conexão OBD   | `python-OBD`, `pyserial`        |
| Interface Web | `streamlit`, `plotly`, `pandas` |
| Interface TUI | `rich`, `textual`               |
| Armazenamento | `sqlite3`, `csv`                |
| Utilitários   | `dotenv`, `argparse`, `logging` |

---

## 🧩 Contribuindo

Pull requests são bem-vindos!

1. Faça um fork
2. Crie uma branch (`feature/nome-da-feature`)
3. Commit suas mudanças
4. Abra um Pull Request com sua ideia ✨

---

## 🧾 Licença

Distribuído sob a **Licença MIT**.

```
MIT License © 2025 Eduh Giaretta
```

---

## 🌐 Visão

O **AETHER** nasceu para explorar a integração entre **homem e máquina**, traduzindo os sinais da ECU em **dados visuais e compreensíveis**.
Mais que um projeto técnico, é uma experiência — onde **tecnologia e percepção automotiva se encontram**.

---

<p align="center">
  <i>“Aether é o elo invisível entre o motor e a mente.”</i>
</p>
```

---

Se quiser deixar o README ainda mais bonito, posso gerar também uma **versão com o banner animado** (efeito glow, partículas ou rotação sutil do anel do planeta) — ideal pro GitHub Pages ou pro topo do README via GIF ou SVG animado.
Quer que eu crie esse banner animado pra completar o visual? 🚀
