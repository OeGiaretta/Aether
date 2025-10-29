import sys, os, time
import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from core.obd_reader import MockObdReader
from core.data_manager import normalize

st.set_page_config(page_title="AETHER - Performance", page_icon="⚙️", layout="wide")

if "reader" not in st.session_state:
    st.session_state["reader"] = MockObdReader()
    st.session_state["reader"].connect()
if "history" not in st.session_state:
    st.session_state["history"] = []

reader = st.session_state["reader"]

st.title("⚙️ Performance")

payload = normalize(reader.read())
timestamp = datetime.now()
entry = {"timestamp": timestamp, **{k: v["value"] for k, v in payload["sensors"].items()}}
st.session_state["history"].append(entry)
if len(st.session_state["history"]) > 500:
    st.session_state["history"] = st.session_state["history"][-500:]

c1, c2, c3 = st.columns(3)
with c1: st.metric("RPM", f"{payload['sensors']['rpm']['value']:.0f}")
with c2: st.metric("Engine Load", f"{payload['sensors']['engine_load']['value']:.0f} %")
with c3: st.metric("Throttle", f"{payload['sensors']['throttle']['value']:.0f} %")

if len(st.session_state["history"]) > 2:
    df = pd.DataFrame(st.session_state["history"]).set_index("timestamp")
    cols = [c for c in ["rpm","engine_load","throttle"] if c in df.columns]
    if cols:
        st.subheader("Performance History")
        st.plotly_chart(px.line(df[cols]), use_container_width=True)

auto = st.sidebar.toggle("Auto-refresh", value=True)
interval = st.sidebar.slider("Interval (s)", 1, 10, 2)
if auto:
    time.sleep(interval)
    st.rerun()
