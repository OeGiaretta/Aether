import sys, os, time
import streamlit as st
import pandas as pd
import plotly.express as px

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

st.set_page_config(page_title="AETHER - History", page_icon="📈", layout="wide")

if "history" not in st.session_state:
    st.session_state["history"] = []

st.title("📈 History")

if not st.session_state["history"]:
    st.info("No data yet. Visit other pages to start collecting.")
else:
    df = pd.DataFrame(st.session_state["history"]).set_index("timestamp")
    cols = [c for c in df.columns if c != "timestamp"]
    pick = st.multiselect("Select sensors:", cols, default=cols[:5])
    if pick:
        st.plotly_chart(px.line(df[pick]), use_container_width=True)
    st.dataframe(df.tail(100), use_container_width=True)

# controls
auto = st.sidebar.toggle("Auto-refresh", value=False)
interval = st.sidebar.slider("Interval (s)", 1, 10, 2)
if auto:
    time.sleep(interval)
    st.rerun()
