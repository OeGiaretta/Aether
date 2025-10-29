# 🔧 Documentação Técnica - AETHER Dashboard

> **Arquitetura, APIs e implementação técnica do sistema**

---

## 🏗️ Arquitetura do Sistema

### 📐 Visão Geral
O AETHER segue uma arquitetura modular baseada em camadas, separando responsabilidades e facilitando manutenção e extensibilidade.

```
┌─────────────────────────────────────────────────────────────┐
│                    CAMADA DE APRESENTAÇÃO                   │
├─────────────────────────────────────────────────────────────┤
│  Streamlit Dashboard  │  Terminal UI (TUI)  │  Future Mobile │
├─────────────────────────────────────────────────────────────┤
│                    CAMADA DE APLICAÇÃO                      │
├─────────────────────────────────────────────────────────────┤
│  Data Manager  │  Logger  │  Storage  │  Alert System      │
├─────────────────────────────────────────────────────────────┤
│                    CAMADA DE DADOS                          │
├─────────────────────────────────────────────────────────────┤
│  Mock OBD Reader  │  Real OBD Reader  │  CSV Storage       │
├─────────────────────────────────────────────────────────────┤
│                    CAMADA DE HARDWARE                       │
├─────────────────────────────────────────────────────────────┤
│  ELM327 Adapter  │  Bluetooth/USB  │  Vehicle ECU         │
└─────────────────────────────────────────────────────────────┘
```

---

## 📦 Módulos do Sistema

### 🧠 Core (`core/`)

#### `obd_reader.py` - Leitor OBD-II
```python
class MockObdReader:
    """Implementação mock para desenvolvimento e testes"""
    
    def connect(self, config: ReaderConfig | None = None) -> None
    def read(self) -> TelemetryPayload
    def close(self) -> None
    
    @property
    def connected(self) -> bool
    @property
    def source(self) -> SourceType
```

**Funcionalidades:**
- Geração de dados simulados realísticos
- Implementação do protocolo `ObdReader`
- Configuração via `ReaderConfig`
- Fallback automático para modo mock

#### `data_manager.py` - Gerenciamento de Dados
```python
def normalize(payload: TelemetryPayload) -> TelemetryPayload
def clamp(value: float, lo: float, hi: float) -> float
```

**Funcionalidades:**
- Normalização de dados de sensores
- Validação de faixas de valores
- Clamping de valores fora dos limites
- Detecção de erros e anomalias

#### `logger.py` - Sistema de Logs
```python
class AetherLogger:
    def log_telemetry(self, payload: TelemetryPayload) -> None
    def log_connection(self, source: str, status: str, details: str) -> None
    def log_performance(self, operation: str, duration: float) -> None
```

**Funcionalidades:**
- Logging estruturado com níveis
- Rotação automática de arquivos
- Logs específicos para telemetria
- Integração com sistema de alertas

#### `storage.py` - Armazenamento
```python
class DataStorage:
    def save_telemetry(self, payload: TelemetryPayload) -> bool
    def load_telemetry(self, **kwargs) -> pd.DataFrame
    def get_statistics(self, days: int = 7) -> Dict[str, Any]
    def export_data(self, output_file: str) -> bool
```

**Funcionalidades:**
- Persistência em CSV
- Consultas com filtros temporais
- Estatísticas agregadas
- Exportação em múltiplos formatos

### 🎨 UI (`ui/`)

#### `streamlit_dashboard.py` - Dashboard Principal
**Componentes principais:**
- **Sidebar:** Controles e configurações
- **Métricas:** Cards de dados principais
- **Gauges:** Indicadores visuais circulares
- **Gráficos:** Histórico e correlações
- **Alertas:** Sistema de notificações

#### `widgets/gauges.py` - Componentes Visuais
```python
class AetherGauge:
    @staticmethod
    def create_rpm_gauge(value: float) -> go.Figure
    @staticmethod
    def create_speed_gauge(value: float) -> go.Figure
    @staticmethod
    def create_temperature_gauge(value: float) -> go.Figure

class AetherIndicator:
    @staticmethod
    def create_status_card(title: str, value: Any, status: str) -> None
    @staticmethod
    def create_progress_bar(value: float, max_value: float) -> None
```

**Funcionalidades:**
- Gauges personalizados para dados automotivos
- Indicadores de status com cores dinâmicas
- Barras de progresso visuais
- Caixas de alerta estilizadas

### 🛠️ Utils (`utils/`)

#### `types.py` - Definições de Tipos
```python
class SensorValue(TypedDict):
    value: Optional[float]
    unit: str
    ok: bool
    meta: NotRequired[Dict[str, float]]

class TelemetryPayload(TypedDict):
    timestamp: float
    sensors: Dict[str, SensorValue]
    source: SourceType
    errors: List[str]

class ObdReader(Protocol):
    def connect(self, config: Optional[ReaderConfig] = None) -> None
    def read(self) -> TelemetryPayload
    def close(self) -> None
```

---

## 🔄 Fluxo de Dados

### 1. **Coleta de Dados**
```
Hardware OBD-II → ELM327 → Serial/USB → OBD Reader
```

### 2. **Processamento**
```
Raw Data → Data Manager → Normalization → Validation
```

### 3. **Armazenamento**
```
Processed Data → Logger → Storage → CSV File
```

### 4. **Visualização**
```
Stored Data → Dashboard → Gauges/Charts → User Interface
```

---

## 📊 Estrutura de Dados

### `TelemetryPayload`
```python
{
    "timestamp": 1640995200.0,  # Unix timestamp
    "sensors": {
        "rpm": {
            "value": 2500.0,
            "unit": "rpm",
            "ok": True,
            "meta": {"min": 0.0, "max": 8000.0}
        },
        "speed": {
            "value": 80.5,
            "unit": "km/h", 
            "ok": True,
            "meta": {"min": 0.0, "max": 240.0}
        }
        # ... outros sensores
    },
    "source": "mock",  # ou "obd"
    "errors": []  # Lista de erros detectados
}
```

### `SensorValue`
```python
{
    "value": 85.5,           # Valor numérico
    "unit": "°C",            # Unidade de medida
    "ok": True,              # Status de validação
    "meta": {                # Metadados (opcional)
        "min": -40.0,
        "max": 130.0
    }
}
```

---

## 🔧 APIs e Interfaces

### `ObdReader` Protocol
```python
class ObdReader(Protocol):
    @property
    def source(self) -> SourceType: ...
    @property
    def connected(self) -> bool: ...
    def connect(self, config: Optional[ReaderConfig] = None) -> None: ...
    def read(self) -> TelemetryPayload: ...
    def close(self) -> None: ...
```

### `AetherLogger` API
```python
# Logging básico
logger.info("Mensagem informativa")
logger.warning("Aviso importante")
logger.error("Erro crítico")

# Logging específico
logger.log_telemetry(payload)
logger.log_connection("mock", "connected", "Inicializado")
logger.log_performance("read_sensors", 0.150)
```

### `DataStorage` API
```python
# Salvar dados
storage.save_telemetry(payload)

# Carregar dados
df = storage.load_telemetry(
    start_date=datetime.now() - timedelta(days=7),
    source="mock",
    limit=1000
)

# Estatísticas
stats = storage.get_statistics(days=30)
```

---

## 🎨 Componentes Visuais

### Gauges Plotly
```python
# Estrutura base de um gauge
fig = go.Figure(go.Indicator(
    mode="gauge+number+delta",
    value=current_value,
    domain={'x': [0, 1], 'y': [0, 1]},
    title={'text': "Título do Gauge"},
    gauge={
        'axis': {'range': [min_val, max_val]},
        'bar': {'color': dynamic_color},
        'steps': [
            {'range': [min_val, threshold1], 'color': "green"},
            {'range': [threshold1, threshold2], 'color': "yellow"},
            {'range': [threshold2, max_val], 'color': "red"}
        ]
    }
))
```

### Cards de Status
```python
# HTML/CSS personalizado para cards
st.markdown(f"""
<div style="
    border: 2px solid {color};
    border-radius: 10px;
    padding: 15px;
    background-color: rgba(255, 255, 255, 0.1);
">
    <h4 style="color: {color};">{icon} {title}</h4>
    <h2 style="color: {color};">{value:.1f} {unit}</h2>
</div>
""", unsafe_allow_html=True)
```

---

## 🔍 Sistema de Alertas

### Configuração de Thresholds
```python
ALERT_THRESHOLDS = {
    "rpm": {"warning": 6000, "critical": 7000},
    "coolant_temp": {"warning": 100, "critical": 110},
    "speed": {"warning": 120, "critical": 150},
    "fuel_level": {"warning": 20, "critical": 10}
}
```

### Detecção de Alertas
```python
def check_alerts(payload: TelemetryPayload) -> List[Alert]:
    alerts = []
    
    for sensor_name, sensor_data in payload["sensors"].items():
        if sensor_name in ALERT_THRESHOLDS:
            value = sensor_data["value"]
            thresholds = ALERT_THRESHOLDS[sensor_name]
            
            if value > thresholds["critical"]:
                alerts.append(Alert(sensor_name, "critical", value))
            elif value > thresholds["warning"]:
                alerts.append(Alert(sensor_name, "warning", value))
    
    return alerts
```

---

## 📈 Performance e Otimização

### Cache de Dados
- **Histórico em memória:** 100 registros máximo
- **Rotação automática:** Remove dados antigos
- **Lazy loading:** Carrega dados sob demanda

### Otimizações de UI
- **Streamlit caching:** `@st.cache_data` para operações pesadas
- **Plotly otimizado:** Configurações de performance
- **Refresh inteligente:** Evita atualizações desnecessárias

### Logging Eficiente
- **Rotação de arquivos:** Evita arquivos muito grandes
- **Níveis configuráveis:** Debug em desenvolvimento, Info em produção
- **Logs assíncronos:** Não bloqueia interface principal

---

## 🧪 Testes e Qualidade

### Estrutura de Testes
```
tests/
├── test_sensor_map.py      # Validação de metadados
├── test_data_manager.py    # Normalização e conversões
├── test_obd_reader_mock.py # Geração de sinais
├── test_storage.py         # Persistência de dados
└── test_integration.py     # Testes end-to-end
```

### Métricas de Qualidade
- **Cobertura de código:** > 80%
- **Type hints:** 100% das funções públicas
- **Docstrings:** Documentação completa
- **Linting:** Pylint, Black, isort

---

## 🚀 Extensibilidade

### Adicionando Novos Sensores
1. **Atualizar `sensor_map.py`:**
```python
SENSOR_MAP["new_sensor"] = {
    "unit": "unit",
    "min": 0.0,
    "max": 100.0,
    "pid": "01XX"
}
```

2. **Criar gauge personalizado:**
```python
@staticmethod
def create_new_sensor_gauge(value: float) -> go.Figure:
    # Implementação do gauge
```

3. **Adicionar alertas:**
```python
if payload["sensors"]["new_sensor"]["value"] > threshold:
    # Lógica de alerta
```

### Adicionando Novas Fontes de Dados
1. **Implementar protocolo `ObdReader`**
2. **Configurar conexão específica**
3. **Adicionar fallback para mock**

---

## 📚 Referências Técnicas

### Bibliotecas Principais
- **Streamlit:** Interface web
- **Plotly:** Visualizações interativas
- **Pandas:** Manipulação de dados
- **Python-OBD:** Comunicação OBD-II
- **Rich:** Terminal UI (futuro)

### Padrões Utilizados
- **Protocol:** Para interfaces (Python 3.8+)
- **TypedDict:** Para estruturas de dados
- **Dependency Injection:** Para modularidade
- **Observer Pattern:** Para sistema de alertas

---

## 🔧 Configuração Avançada

### Variáveis de Ambiente
```bash
# OBD-II
OBD_DEVICE=/dev/ttyUSB0
OBD_BAUDRATE=38400
OBD_TIMEOUT=5

# Dashboard
STREAMLIT_PORT=8501
STREAMLIT_HOST=localhost
REFRESH_INTERVAL=5

# Logging
LOG_LEVEL=INFO
LOG_FILE_MAX_SIZE=10MB
LOG_BACKUP_COUNT=5

# Storage
DATA_RETENTION_DAYS=30
CSV_FILE_PATH=data/telemetry_data.csv
```

### Configuração de Desenvolvimento
```python
# config.py
class Config:
    DEBUG = True
    MOCK_MODE = True
    LOG_LEVEL = "DEBUG"
    REFRESH_INTERVAL = 1
    DATA_RETENTION = 7
```

---

**🔧 Esta documentação técnica fornece uma visão completa da arquitetura e implementação do AETHER Dashboard!**
