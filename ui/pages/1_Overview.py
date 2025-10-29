import sys, os, time
import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime

# imports locais
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from core.obd_reader import MockObdReader
from core.data_manager import normalize

st.set_page_config(page_title="AETHER - Overview", page_icon="🌌", layout="wide")

# estado
if "reader" not in st.session_state:
    st.session_state["reader"] = MockObdReader()
    st.session_state["reader"].connect()
if "history" not in st.session_state:
    st.session_state["history"] = []

reader = st.session_state["reader"]

st.title("🌌 Overview")
st.caption("Resumo geral dos principais sensores")

# leitura
payload = normalize(reader.read())
timestamp = datetime.now()
entry = {"timestamp": timestamp, **{k: v["value"] for k, v in payload["sensors"].items()}}
st.session_state["history"].append(entry)
if len(st.session_state["history"]) > 300:
    st.session_state["history"] = st.session_state["history"][-300:]

# cards
c1, c2, c3, c4 = st.columns(4)
with c1: st.metric("RPM", f"{payload['sensors']['rpm']['value']:.0f}")
with c2: st.metric("Speed", f"{payload['sensors']['speed']['value']:.0f} km/h")
with c3: st.metric("Coolant", f"{payload['sensors']['coolant_temp']['value']:.0f} °C")
with c4: st.metric("Throttle", f"{payload['sensors']['throttle']['value']:.0f} %")

# charts
if len(st.session_state["history"]) > 2:
    df = pd.DataFrame(st.session_state["history"]).set_index("timestamp")
    cols = [c for c in ["rpm","speed","coolant_temp","throttle"] if c in df.columns]
    if cols:
        st.subheader("History (last 300 samples)")
        st.plotly_chart(px.line(df[cols]), use_container_width=True)

# refresh
auto = st.sidebar.toggle("Auto-refresh", value=True)
interval = st.sidebar.slider("Interval (s)", 1, 10, 2)
if auto:
    time.sleep(interval)
    st.rerun()
