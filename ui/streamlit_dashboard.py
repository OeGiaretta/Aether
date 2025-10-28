import sys
import os
import time
import streamlit as st

# Adicionar o diretório raiz ao path para importar módulos locais
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.obd_reader import MockObdReader
from core.data_manager import normalize

st.set_page_config(page_title="AETHER", layout="wide")

if "history" not in st.session_state:
    st.session_state["history"] = []

# Inicializar reader se não existir
if "reader" not in st.session_state:
    st.session_state["reader"] = MockObdReader()
    st.session_state["reader"].connect()

reader = st.session_state["reader"]

# Interface principal
st.title("🌌 AETHER - Dashboard Automotivo")
st.markdown("---")

# Colunas para métricas
col1, col2, col3 = st.columns(3)

# Ler dados
payload = normalize(reader.read())

# Atualizar histórico
st.session_state["history"].append({k: v["value"] for k, v in payload["sensors"].items()})

# Manter apenas últimos 50 registros
if len(st.session_state["history"]) > 50:
    st.session_state["history"] = st.session_state["history"][-50:]

# Exibir métricas
with col1:
    st.metric("RPM", f'{payload["sensors"]["rpm"]["value"]:.0f}')
    st.metric("Speed", f'{payload["sensors"]["speed"]["value"]:.0f} km/h')

with col2:
    st.metric("Coolant", f'{payload["sensors"]["coolant_temp"]["value"]:.0f} °C')
    st.metric("Throttle", f'{payload["sensors"]["throttle"]["value"]:.1f} %')

with col3:
    st.metric("Engine Load", f'{payload["sensors"]["engine_load"]["value"]:.1f} %')
    st.metric("Intake Temp", f'{payload["sensors"]["intake_temp"]["value"]:.0f} °C')

# Status
if payload["errors"]:
    st.error("⚠️ Erros detectados: " + ", ".join(payload["errors"]))
else:
    st.success("✅ Todos os sensores OK")

# Auto-refresh a cada 1 segundo
time.sleep(1.0)
st.rerun()
