# 📚 API Reference - AETHER Dashboard

> **Documentação completa das APIs e interfaces do sistema**

---

## 🧠 Core APIs

### `core.obd_reader.MockObdReader`

#### Construtor
```python
MockObdReader() -> MockObdReader
```
Cria uma nova instância do leitor OBD mock.

#### Propriedades
```python
@property
def source(self) -> SourceType
```
Retorna o tipo de fonte de dados. Sempre retorna `"mock"`.

```python
@property
def connected(self) -> bool
```
Retorna `True` se o leitor estiver conectado, `False` caso contrário.

#### Métodos
```python
def connect(self, config: ReaderConfig | None = None) -> None
```
Conecta o leitor mock. O parâmetro `config` é ignorado no modo mock.

**Parâmetros:**
- `config` (ReaderConfig, opcional): Configuração de conexão

```python
def read(self) -> TelemetryPayload
```
Lê dados de telemetria simulados.

**Retorna:**
- `TelemetryPayload`: Dados de telemetria com sensores simulados

```python
def close(self) -> None
```
Desconecta o leitor mock.

---

### `core.data_manager`

#### `normalize(payload: TelemetryPayload) -> TelemetryPayload`
Normaliza e valida dados de telemetria.

**Parâmetros:**
- `payload` (TelemetryPayload): Dados brutos de telemetria

**Retorna:**
- `TelemetryPayload`: Dados normalizados e validados

**Funcionalidades:**
- Aplica clamping de valores dentro das faixas definidas
- Detecta valores fora dos limites
- Adiciona erros à lista de erros do payload
- Preserva metadados dos sensores

#### `clamp(value: float, lo: float, hi: float) -> float`
Limita um valor entre os limites mínimo e máximo.

**Parâmetros:**
- `value` (float): Valor a ser limitado
- `lo` (float): Limite inferior
- `hi` (float): Limite superior

**Retorna:**
- `float`: Valor limitado entre `lo` e `hi`

---

### `core.logger.AetherLogger`

#### Construtor
```python
AetherLogger(
    name: str = "aether",
    log_dir: str = "logs",
    max_file_size: int = 10 * 1024 * 1024,
    backup_count: int = 5,
    level: int = logging.INFO
) -> AetherLogger
```

**Parâmetros:**
- `name` (str): Nome do logger
- `log_dir` (str): Diretório para arquivos de log
- `max_file_size` (int): Tamanho máximo do arquivo de log em bytes
- `backup_count` (int): Número de arquivos de backup
- `level` (int): Nível de logging

#### Métodos de Logging
```python
def debug(self, message: str, **kwargs) -> None
def info(self, message: str, **kwargs) -> None
def warning(self, message: str, **kwargs) -> None
def error(self, message: str, **kwargs) -> None
def critical(self, message: str, **kwargs) -> None
```

**Parâmetros:**
- `message` (str): Mensagem de log
- `**kwargs`: Contexto adicional para formatação

#### Métodos Específicos
```python
def log_telemetry(self, payload: TelemetryPayload) -> None
```
Log específico para dados de telemetria.

```python
def log_connection(self, source: str, status: str, details: str) -> None
```
Log de eventos de conexão.

```python
def log_performance(self, operation: str, duration: float, **kwargs) -> None
```
Log de performance de operações.

---

### `core.storage.DataStorage`

#### Construtor
```python
DataStorage(
    data_dir: str = "data",
    csv_filename: str = "telemetry_data.csv",
    sqlite_filename: str = "aether.db"
) -> DataStorage
```

#### Métodos Principais
```python
def save_telemetry(self, payload: TelemetryPayload) -> bool
```
Salva dados de telemetria no CSV.

**Retorna:**
- `bool`: `True` se salvou com sucesso, `False` caso contrário

```python
def load_telemetry(
    self,
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
    source: Optional[str] = None,
    limit: Optional[int] = None
) -> pd.DataFrame
```
Carrega dados de telemetria do CSV.

**Parâmetros:**
- `start_date` (datetime, opcional): Data de início
- `end_date` (datetime, opcional): Data de fim
- `source` (str, opcional): Fonte de dados
- `limit` (int, opcional): Limite de registros

**Retorna:**
- `pd.DataFrame`: DataFrame com os dados carregados

```python
def get_statistics(self, days: int = 7, source: Optional[str] = None) -> Dict[str, Any]
```
Calcula estatísticas dos dados armazenados.

**Retorna:**
- `Dict[str, Any]`: Estatísticas agregadas

```python
def export_data(
    self,
    output_file: str,
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
    source: Optional[str] = None
) -> bool
```
Exporta dados para um arquivo.

**Parâmetros:**
- `output_file` (str): Caminho do arquivo de saída
- `start_date` (datetime, opcional): Data de início
- `end_date` (datetime, opcional): Data de fim
- `source` (str, opcional): Fonte de dados

**Retorna:**
- `bool`: `True` se exportou com sucesso

---

## 🎨 UI APIs

### `ui.widgets.gauges.AetherGauge`

#### Métodos Estáticos
```python
@staticmethod
def create_rpm_gauge(
    value: float,
    min_val: float = 0,
    max_val: float = 8000,
    title: str = "RPM"
) -> go.Figure
```
Cria um gauge para RPM do motor.

```python
@staticmethod
def create_speed_gauge(
    value: float,
    min_val: float = 0,
    max_val: float = 240,
    title: str = "Velocidade"
) -> go.Figure
```
Cria um gauge para velocidade.

```python
@staticmethod
def create_temperature_gauge(
    value: float,
    min_val: float = -40,
    max_val: float = 130,
    title: str = "Temperatura"
) -> go.Figure
```
Cria um gauge para temperatura.

```python
@staticmethod
def create_percentage_gauge(
    value: float,
    title: str = "Percentual",
    unit: str = "%"
) -> go.Figure
```
Cria um gauge para valores percentuais.

### `ui.widgets.gauges.AetherIndicator`

#### Métodos Estáticos
```python
@staticmethod
def create_status_card(
    title: str,
    value: Any,
    unit: str = "",
    status: str = "normal",
    delta: Optional[float] = None
) -> None
```
Cria um card de status visual.

**Parâmetros:**
- `title` (str): Título do card
- `value` (Any): Valor a ser exibido
- `unit` (str): Unidade do valor
- `status` (str): Status ("normal", "warning", "error")
- `delta` (float, opcional): Variação do valor

```python
@staticmethod
def create_progress_bar(
    value: float,
    max_value: float,
    title: str,
    color: str = "blue"
) -> None
```
Cria uma barra de progresso visual.

```python
@staticmethod
def create_alert_box(message: str, alert_type: str = "info") -> None
```
Cria uma caixa de alerta.

**Parâmetros:**
- `message` (str): Mensagem do alerta
- `alert_type` (str): Tipo ("info", "warning", "error", "success")

---

## 🛠️ Utils APIs

### `utils.types`

#### `SensorValue`
```python
class SensorValue(TypedDict):
    value: Optional[float]
    unit: str
    ok: bool
    meta: NotRequired[Dict[str, float]]
```

#### `TelemetryPayload`
```python
class TelemetryPayload(TypedDict):
    timestamp: float
    sensors: Dict[str, SensorValue]
    source: SourceType
    errors: List[str]
```

#### `ReaderConfig`
```python
class ReaderConfig(TypedDict, total=False):
    device: Optional[str]
    baudrate: int
    refresh_rate: float
```

#### `ObdReader` Protocol
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

---

## 🔧 Funções de Conveniência

### Logger Global
```python
from core.logger import get_logger, log_telemetry, log_connection, log_performance

# Obter logger
logger = get_logger("my_module")

# Logging básico
logger.info("Mensagem informativa")
logger.error("Erro crítico")

# Logging específico
log_telemetry(payload)
log_connection("mock", "connected", "Inicializado")
log_performance("operation", 0.150)
```

### Storage Global
```python
from core.storage import save_telemetry, load_telemetry, get_statistics

# Salvar dados
save_telemetry(payload)

# Carregar dados
df = load_telemetry(limit=100)

# Estatísticas
stats = get_statistics(days=7)
```

---

## 📊 Estruturas de Dados

### Exemplo de `TelemetryPayload`
```python
{
    "timestamp": 1640995200.0,
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
        },
        "coolant_temp": {
            "value": 85.5,
            "unit": "°C",
            "ok": True,
            "meta": {"min": -40.0, "max": 130.0}
        }
    },
    "source": "mock",
    "errors": []
}
```

### Exemplo de `ReaderConfig`
```python
{
    "device": "/dev/ttyUSB0",
    "baudrate": 38400,
    "refresh_rate": 1.0
}
```

---

## 🚨 Códigos de Erro

### Logger
- **DEBUG (10):** Informações detalhadas de debug
- **INFO (20):** Informações gerais
- **WARNING (30):** Avisos importantes
- **ERROR (40):** Erros que não impedem funcionamento
- **CRITICAL (50):** Erros críticos que impedem funcionamento

### Storage
- **FileNotFoundError:** Arquivo de dados não encontrado
- **PermissionError:** Sem permissão para escrever arquivo
- **ValueError:** Dados inválidos fornecidos
- **KeyError:** Chave não encontrada nos dados

### OBD Reader
- **ConnectionError:** Falha na conexão com dispositivo
- **TimeoutError:** Timeout na comunicação
- **ValueError:** Dados recebidos inválidos
- **NotImplementedError:** Funcionalidade não implementada

---

## 📝 Exemplos de Uso

### Exemplo Básico
```python
from core.obd_reader import MockObdReader
from core.data_manager import normalize
from core.logger import get_logger
from core.storage import save_telemetry

# Inicializar componentes
reader = MockObdReader()
reader.connect()
logger = get_logger("example")

# Ler e processar dados
raw_data = reader.read()
processed_data = normalize(raw_data)

# Log e salvar
logger.log_telemetry(processed_data)
save_telemetry(processed_data)

# Fechar conexão
reader.close()
```

### Exemplo com Gauges
```python
from ui.widgets.gauges import AetherGauge, AetherIndicator
import streamlit as st

# Criar gauges
rpm_gauge = AetherGauge.create_rpm_gauge(2500)
speed_gauge = AetherGauge.create_speed_gauge(80)

# Exibir no Streamlit
st.plotly_chart(rpm_gauge, use_container_width=True)
st.plotly_chart(speed_gauge, use_container_width=True)

# Criar indicadores
AetherIndicator.create_status_card("RPM", 2500, "rpm", "normal")
AetherIndicator.create_alert_box("Sistema OK", "success")
```

### Exemplo com Storage
```python
from core.storage import DataStorage
from datetime import datetime, timedelta

# Inicializar storage
storage = DataStorage()

# Carregar dados dos últimos 7 dias
end_date = datetime.now()
start_date = end_date - timedelta(days=7)
df = storage.load_telemetry(start_date, end_date, limit=1000)

# Obter estatísticas
stats = storage.get_statistics(days=7)
print(f"Total de registros: {stats['total_records']}")

# Exportar dados
storage.export_data("export.csv", start_date, end_date)
```

---

**📚 Esta documentação de API fornece uma referência completa para desenvolvedores que desejam integrar ou estender o AETHER Dashboard!**
