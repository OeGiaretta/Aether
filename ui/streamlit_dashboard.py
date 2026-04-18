import sys
import os
import time
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta

# Adicionar o diretório raiz ao path para importar módulos locais
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.obd_reader import MockObdReader
from core.data_manager import normalize
from core.logger import get_logger, log_telemetry, log_connection
from core.storage import save_telemetry, load_telemetry, get_statistics
from ui.widgets.gauges import AetherGauge, AetherIndicator

st.set_page_config(
    page_title="AETHER Dashboard", 
    page_icon="🌌", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# Inicializar logger
logger = get_logger("streamlit_dashboard")

if "history" not in st.session_state:
    st.session_state["history"] = []

# Inicializar reader se não existir
if "reader" not in st.session_state:
    st.session_state["reader"] = MockObdReader()
    st.session_state["reader"].connect()
    log_connection("mock", "connected", "Mock OBD reader initialized")

reader = st.session_state["reader"]

# Ler dados primeiro
payload = normalize(reader.read())

# Log e salvar dados
log_telemetry(payload)
save_telemetry(payload)

# Sidebar com controles
with st.sidebar:
    st.image("assets/images/Aether.png", width=200)
    st.title("🌌 AETHER")
    st.markdown("**Dashboard Automotivo**")
    
    st.markdown("---")
    st.subheader("⚙️ Configurações")
    
    # Controles de refresh
    auto_refresh = st.checkbox("🔄 Auto-refresh", value=True)
    refresh_interval = st.slider("Intervalo (segundos)", 1, 30, 5)
    
    st.markdown("---")
    st.subheader("📊 Sensores")
    
    # Filtros de sensores
    sensor_options = list(payload["sensors"].keys())
    selected_sensors = st.multiselect(
        "Mostrar sensores:", 
        sensor_options, 
        default=sensor_options[:6] if len(sensor_options) >= 6 else sensor_options
    )
    
    st.markdown("---")
    st.subheader("📈 Estatísticas")
    
    # Estatísticas dos últimos 7 dias
    if st.button("📊 Atualizar Estatísticas"):
        stats = get_statistics(days=7)
        if "error" not in stats:
            st.success(f"📊 {stats['total_records']} registros nos últimos 7 dias")
            st.write(f"**Período:** {stats['date_range']['start'][:10]} a {stats['date_range']['end'][:10]}")
            
            # Mostrar estatísticas dos sensores principais
            main_sensors = ['rpm', 'speed', 'coolant_temp', 'throttle']
            for sensor in main_sensors:
                if sensor in stats['sensor_stats']:
                    sensor_stats = stats['sensor_stats'][sensor]
                    st.write(f"**{sensor.upper()}:**")
                    st.write(f"  • Média: {sensor_stats['mean']:.1f}")
                    st.write(f"  • Min: {sensor_stats['min']:.1f}")
                    st.write(f"  • Max: {sensor_stats['max']:.1f}")
        else:
            st.error(f"Erro ao carregar estatísticas: {stats['error']}")
    
    st.markdown("---")
    st.subheader("💾 Dados")
    
    # Informações sobre armazenamento
    if st.button("📁 Info de Armazenamento"):
        from core.storage import storage
        file_sizes = storage.get_file_size()
        
        st.write("**Arquivos de Dados:**")
        for file_type, size in file_sizes.items():
            size_mb = size / (1024 * 1024)
            st.write(f"  • {file_type.upper()}: {size_mb:.2f} MB")
        
        # Estatísticas rápidas
        recent_data = load_telemetry(limit=100)
        if not recent_data.empty:
            st.write(f"**Últimos 100 registros:**")
            st.write(f"  • Período: {recent_data['timestamp'].min()} a {recent_data['timestamp'].max()}")
            st.write(f"  • Fontes: {', '.join(recent_data['source'].unique())}")
    
    st.markdown("---")
    st.subheader("🚨 Alertas")
    
    # Verificar alertas críticos
    critical_alerts = []
    
    # RPM muito alto
    if payload["sensors"]["rpm"]["value"] > 6000:
        critical_alerts.append(("RPM Alto", "warning"))
    
    # Temperatura alta
    if payload["sensors"]["coolant_temp"]["value"] > 100:
        critical_alerts.append(("Temperatura Alta", "error"))
    
    # Velocidade alta
    if payload["sensors"]["speed"]["value"] > 120:
        critical_alerts.append(("Velocidade Alta", "warning"))
    
    # Nível de combustível baixo
    if payload["sensors"]["fuel_level"]["value"] < 20:
        critical_alerts.append(("Combustível Baixo", "warning"))
    
    # Exibir alertas
    if critical_alerts:
        for alert, alert_type in critical_alerts:
            AetherIndicator.create_alert_box(alert, alert_type)
    else:
        AetherIndicator.create_alert_box("Sistema Operacional", "success")

# Interface principal
st.title("🌌 AETHER - Dashboard Automotivo")
st.markdown("Sistema de monitoramento automotivo em tempo real via OBD-II")

# Atualizar histórico com timestamp
timestamp = datetime.now()
history_entry = {
    "timestamp": timestamp,
    **{k: v["value"] for k, v in payload["sensors"].items()}
}
st.session_state["history"].append(history_entry)

# Manter apenas últimos 100 registros
if len(st.session_state["history"]) > 100:
    st.session_state["history"] = st.session_state["history"][-100:]

# Status do sistema
col_status1, col_status2, col_status3 = st.columns(3)

with col_status1:
    if payload["errors"]:
        st.error(f"⚠️ {len(payload['errors'])} erro(s) detectado(s)")
    else:
        st.success("✅ Todos os sensores OK")

with col_status2:
    st.info(f"📡 Fonte: {payload['source'].upper()}")

with col_status3:
    st.info(f"🕐 Última atualização: {timestamp.strftime('%H:%M:%S')}")

st.markdown("---")

# Métricas principais em cards
st.subheader("📊 Métricas Principais")

# Criar cards para as métricas principais
col1, col2, col3, col4 = st.columns(4)

# Função para criar card de métrica
def create_metric_card(title, value, unit, delta=None, delta_color="normal"):
    with st.container():
        st.metric(
            label=title,
            value=f"{value:.1f} {unit}",
            delta=delta,
            delta_color=delta_color
        )

with col1:
    create_metric_card("RPM", payload["sensors"]["rpm"]["value"], "rpm")

with col2:
    create_metric_card("Velocidade", payload["sensors"]["speed"]["value"], "km/h")

with col3:
    create_metric_card("Temperatura", payload["sensors"]["coolant_temp"]["value"], "°C")

with col4:
    create_metric_card("Acelerador", payload["sensors"]["throttle"]["value"], "%")

# Métricas secundárias
st.subheader("🔧 Detalhes do Motor")

col5, col6, col7, col8 = st.columns(4)

with col5:
    create_metric_card("Carga do Motor", payload["sensors"]["engine_load"]["value"], "%")

with col6:
    create_metric_card("Temp. Admissão", payload["sensors"]["intake_temp"]["value"], "°C")

with col7:
    create_metric_card("Pressão MAP", payload["sensors"]["map"]["value"], "kPa")

with col8:
    create_metric_card("Nível Combustível", payload["sensors"]["fuel_level"]["value"], "%")

# Seção de Gauges Visuais
st.subheader("🎯 Gauges Visuais")

# Gauges principais
gauge_col1, gauge_col2, gauge_col3 = st.columns(3)

with gauge_col1:
    rpm_gauge = AetherGauge.create_rpm_gauge(
        payload["sensors"]["rpm"]["value"],
        title="RPM do Motor"
    )
    st.plotly_chart(rpm_gauge, use_container_width=True)

with gauge_col2:
    speed_gauge = AetherGauge.create_speed_gauge(
        payload["sensors"]["speed"]["value"],
        title="Velocidade"
    )
    st.plotly_chart(speed_gauge, use_container_width=True)

with gauge_col3:
    temp_gauge = AetherGauge.create_temperature_gauge(
        payload["sensors"]["coolant_temp"]["value"],
        title="Temperatura do Motor"
    )
    st.plotly_chart(temp_gauge, use_container_width=True)

# Gauges secundários
gauge_col4, gauge_col5, gauge_col6 = st.columns(3)

with gauge_col4:
    throttle_gauge = AetherGauge.create_percentage_gauge(
        payload["sensors"]["throttle"]["value"],
        title="Acelerador"
    )
    st.plotly_chart(throttle_gauge, use_container_width=True)

with gauge_col5:
    engine_load_gauge = AetherGauge.create_percentage_gauge(
        payload["sensors"]["engine_load"]["value"],
        title="Carga do Motor"
    )
    st.plotly_chart(engine_load_gauge, use_container_width=True)

with gauge_col6:
    fuel_gauge = AetherGauge.create_percentage_gauge(
        payload["sensors"]["fuel_level"]["value"],
        title="Nível de Combustível"
    )
    st.plotly_chart(fuel_gauge, use_container_width=True)

# Gráficos de histórico
if len(st.session_state["history"]) > 1:
    st.subheader("📈 Histórico dos Sensores")
    
    # Converter histórico para DataFrame
    df = pd.DataFrame(st.session_state["history"])
    df.set_index('timestamp', inplace=True)
    
    # Filtrar sensores selecionados
    if selected_sensors:
        available_sensors = [s for s in selected_sensors if s in df.columns]
        if available_sensors:
            # Criar gráfico de linha
            fig = px.line(
                df[available_sensors], 
                title="Evolução dos Sensores ao Longo do Tempo",
                labels={'value': 'Valor', 'timestamp': 'Tempo'}
            )
            fig.update_layout(
                height=400,
                showlegend=True,
                xaxis_title="Tempo",
                yaxis_title="Valor"
            )
            st.plotly_chart(fig, use_container_width=True)
            
            # Gráfico de correlação
            if len(available_sensors) > 1:
                st.subheader("🔗 Matriz de Correlação")
                corr_matrix = df[available_sensors].corr()
                fig_corr = px.imshow(
                    corr_matrix,
                    text_auto=True,
                    aspect="auto",
                    title="Correlação entre Sensores"
                )
                st.plotly_chart(fig_corr, use_container_width=True)

# Controles de refresh
st.markdown("---")
col_refresh1, col_refresh2 = st.columns(2)

with col_refresh1:
    if st.button("🔄 Atualizar Dados", type="primary"):
        st.rerun()

with col_refresh2:
    if st.button("🗑️ Limpar Histórico"):
        st.session_state["history"] = []
        st.rerun()

# Auto-refresh automático
if auto_refresh:
    placeholder = st.empty()
    with placeholder.container():
        st.info(f"⏳ Próxima atualização em {refresh_interval} segundos...")
    time.sleep(refresh_interval)
    st.rerun()

# Informações adicionais
st.markdown("---")
st.subheader("ℹ️ Informações do Sistema")

col_info1, col_info2 = st.columns(2)

with col_info1:
    st.info(f"""
    **Status da Conexão:** {'🟢 Conectado' if reader.connected else '🔴 Desconectado'}  
    **Total de Leituras:** {len(st.session_state['history'])}  
    **Fonte de Dados:** {payload['source'].upper()}  
    **Última Leitura:** {timestamp.strftime('%d/%m/%Y %H:%M:%S')}
    """)

with col_info2:
    if payload["errors"]:
        st.error("**Erros Detectados:**")
        for error in payload["errors"]:
            st.write(f"• {error}")
    else:
        st.success("**Sistema Operacional** - Todos os sensores funcionando normalmente")
