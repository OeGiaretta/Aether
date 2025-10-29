import sys, os, time
from collections import deque
from datetime import datetime
from typing import Deque, Dict, List, Optional

# Guard: evitar execução via Streamlit
if 'streamlit' in sys.modules:
    print("This is a terminal UI (Rich), not a Streamlit app.\nRun with: python ui/terminal_dashboard.py")
    sys.exit(1)

from rich.live import Live
from rich.table import Table
from rich.panel import Panel
from rich.console import Console
from rich.text import Text
from rich.layout import Layout

# Teclado não bloqueante
_IS_WINDOWS = os.name == "nt"
if _IS_WINDOWS:
    try:
        import msvcrt  # type: ignore
    except Exception:  # pragma: no cover
        msvcrt = None
else:
    import select

# Garantir imports locais
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.obd_reader import MockObdReader  # troque depois por RealObdReader via flag
from core.data_manager import normalize
from core.sensor_map import SENSOR_MAP

console = Console()

# Categorias de sensores
CATEGORIES: Dict[str, List[str]] = {
    "all": [
    "rpm", "speed", "coolant_temp", "throttle", "engine_load", "intake_temp", "map"
    ],
    "performance": ["rpm", "engine_load", "throttle"],
    "thermal": ["coolant_temp", "intake_temp"],
    "pressure": ["map"],
    "movement": ["speed"],
}

DEFAULT_CATEGORY = "all"
current_category: str = DEFAULT_CATEGORY

# Histórico curto (mantemos estrutura caso seja útil futuramente)
HISTORY_LEN = 30
history: Dict[str, Deque[float]] = {name: deque(maxlen=HISTORY_LEN) for name in CATEGORIES["all"]}


def percent(value: float, lo: float, hi: float) -> float:
    if hi == lo:
        return 0.0
    v = (value - lo) / (hi - lo)
    return max(0.0, min(1.0, v))


def header_panel(payload) -> Panel:
    ts = datetime.fromtimestamp(payload["timestamp"]).strftime("%H:%M:%S")
    src = payload["source"]
    errs = len(payload["errors"]) or 0
    title = f"AETHER TUI — {ts} | source={src} | errors={errs} | {current_category.upper()}"
    return Panel(title, style="bold magenta", border_style="magenta")


def controls_panel() -> Panel:
    lines = [
        "[bold]Controls[/bold] [dim](press keys)[/dim]",
        "[1]Perf [2]Therm [3]Press [4]Move [A]All [Q]Quit",
    ]
    return Panel("\n".join(lines), border_style="white")


def gauge_row(name: str, value: float, unit: str, lo: float, hi: float, ok: bool) -> Table:
    tbl = Table.grid(expand=True)
    tbl.add_column(ratio=3)
    tbl.add_column(ratio=6)
    tbl.add_column(ratio=3, justify="right")

    # Barra curta para caber no terminal
    term_width = console.size.width
    bar_len = max(6, min(20, term_width // 8))

    p = percent(value, lo, hi)
    filled = int(p * bar_len)
    bar = Text("█" * filled + "░" * (bar_len - filled))
    bar.stylize("green" if ok else "red")

    left = Text(name, style="bold cyan")
    right = Text(f"{value:.0f} {unit}")

    tbl.add_row(left, bar, right)
    return tbl


def _cap_items(names: List[str], max_rows: int) -> List[str]:
    if max_rows <= 0:
        return []
    return names[:max_rows]


def sensors_gauges_panel(payload) -> Panel:
    names = CATEGORIES.get(current_category, CATEGORIES["all"])

    # Calcular quantos gauges cabem por coluna baseado na altura
    term_height = console.size.height
    # Reservar linhas para cabeçalho/controles/erros e outras seções
    available_for_gauges = max(6, int(term_height * 0.33))
    # Aproximar 1 linha por gauge + margens
    per_col_max = max(2, available_for_gauges - 4)

    # duas colunas compactas
    mid = (len(names) + 1) // 2
    left_names = _cap_items(names[:mid], per_col_max)
    right_names = _cap_items(names[mid:], per_col_max)

    grid = Table.grid(expand=True)
    grid.add_column()
    grid.add_column()

    def build_col(names_sel: List[str]) -> Table:
        col = Table.grid(expand=True)
        for n in names_sel:
            if n not in payload["sensors"]:
                continue
            sv = payload["sensors"][n]
            v = float(sv["value"]) if sv["value"] is not None else 0.0
            meta = SENSOR_MAP.get(n, {"min": 0.0, "max": 1.0, "unit": sv["unit"]})
            lo, hi = float(meta["min"]), float(meta["max"])  # type: ignore[index]
            col.add_row(gauge_row(n, v, sv["unit"], lo, hi, sv["ok"]))
        return col

    grid.add_row(build_col(left_names), build_col(right_names))
    return Panel(grid, title="Gauges", border_style="blue")


def sensors_status_table_panel(payload) -> Panel:
    names = CATEGORIES.get(current_category, CATEGORIES["all"])

    # Calcular quantas linhas cabem na tabela
    term_height = console.size.height
    available_for_table = max(6, int(term_height * 0.22))
    # 1 linha por item + header + margens
    max_items = max(3, available_for_table - 3)

    table = Table(expand=True, show_header=True, header_style="bold white")
    table.add_column("Sensor", style="cyan", ratio=3)
    table.add_column("Val", justify="right", ratio=2)
    table.add_column("U", ratio=1)
    table.add_column("St", justify="center", ratio=1)

    count = 0
    for n in names:
        if n not in payload["sensors"]:
            continue
        sv = payload["sensors"][n]
        val_txt = "—" if sv["value"] is None else f"{sv['value']:.0f}"
        status = Text("OK", style="green") if sv["ok"] else Text("ERR", style="red")
        table.add_row(n, val_txt, sv["unit"], status)
        count += 1
        if count >= max_items:
            break

    return Panel(table, title="Sensors", border_style="cyan")


# NOVO: painel de tendências

def _trend_arrow(values: List[float]) -> Text:
    if len(values) < 3:
        return Text("→", style="white")
    delta = values[-1] - values[-3]
    if delta > 0.5:
        return Text("↑", style="green")
    if delta < -0.5:
        return Text("↓", style="red")
    return Text("→", style="yellow")


def trends_panel(payload) -> Panel:
    names = CATEGORIES.get(current_category, CATEGORIES["all"])

    term_height = console.size.height
    available_for_trends = max(5, int(term_height * 0.18))
    max_items = max(3, available_for_trends - 3)

    table = Table(expand=True, show_header=True, header_style="bold white")
    table.add_column("Sensor", style="cyan", ratio=3)
    table.add_column("Now", justify="right", ratio=2)
    table.add_column("Trend", justify="center", ratio=1)

    count = 0
    for n in names:
        if n not in payload["sensors"]:
            continue
        sv = payload["sensors"][n]
        now = 0.0 if sv["value"] is None else float(sv["value"])
        hist = list(history.get(n, []))
        arrow = _trend_arrow(hist)
        table.add_row(n, f"{now:.0f}", arrow)
        count += 1
        if count >= max_items:
            break

    return Panel(table, title="Trends", border_style="magenta")


# NOVO: painel de estatísticas rápidas

def quick_stats_panel(payload) -> Panel:
    names = CATEGORIES.get(current_category, CATEGORIES["all"])

    term_height = console.size.height
    available_for_stats = max(5, int(term_height * 0.18))
    max_items = max(3, available_for_stats - 3)

    table = Table(expand=True, show_header=True, header_style="bold white")
    table.add_column("Sensor", style="cyan", ratio=3)
    table.add_column("Min", justify="right", ratio=1)
    table.add_column("Avg", justify="right", ratio=1)
    table.add_column("Max", justify="right", ratio=1)

    count = 0
    for n in names:
        hist = list(history.get(n, []))
        if not hist:
            table.add_row(n, "—", "—", "—")
        else:
            mn, mx = min(hist), max(hist)
            avg = sum(hist) / len(hist)
            table.add_row(n, f"{mn:.0f}", f"{avg:.0f}", f"{mx:.0f}")
        count += 1
        if count >= max_items:
            break

    return Panel(table, title="Quick Stats", border_style="yellow")


# NOVO: sumário de alertas simples

def alerts_summary_panel(payload) -> Panel:
    names = CATEGORIES.get(current_category, CATEGORIES["all"])
    ok_count = 0
    err_count = 0
    near_limit = 0
    for n in names:
        if n not in payload["sensors"]:
            continue
        sv = payload["sensors"][n]
        if sv["ok"]:
            ok_count += 1
        else:
            err_count += 1
        meta = SENSOR_MAP.get(n)
        if meta and sv["value"] is not None:
            p = percent(float(sv["value"]), float(meta["min"]), float(meta["max"]))
            if p >= 0.9:
                near_limit += 1
    text = f"OK:{ok_count} ERR:{err_count} NearMax:{near_limit}"
    style = "green" if err_count == 0 else "red"
    return Panel(Text(text, style=style), title="Alerts", border_style=style)



def errors_panel(payload) -> Panel:
    if not payload["errors"]:
        return Panel("No errors", border_style="green")
    txt = "\n".join(f"- {e}" for e in payload["errors"])
    return Panel(txt, title="Errors", border_style="red")


def build_layout(payload) -> Layout:
    # atualizar histórico (mantido para possível uso futuro)
    for name, sv in payload["sensors"].items():
        if sv["value"] is not None and name in history:
            history[name].append(float(sv["value"]))

    layout = Layout()
    # Cabeçalho, corpo, controles e erros
    layout.split_column(
        Layout(header_panel(payload), name="header", size=3),
        Layout(name="body"),
        Layout(controls_panel(), name="controls", size=2),
        Layout(errors_panel(payload), name="errors", size=3),
    )

    # Corpo: gauges no topo; abaixo, duas colunas (trends + quick stats) e um alerts compacto
    body = Layout()
    gauges_size = max(7, int(console.size.height * 0.32))
    body.split_column(
        Layout(sensors_gauges_panel(payload), name="gauges", size=gauges_size),
        Layout(name="analytics"),
        Layout(alerts_summary_panel(payload), name="alerts", size=3),
    )
    body["analytics"].split_row(
        Layout(trends_panel(payload), name="trends"),
        Layout(quick_stats_panel(payload), name="qstats"),
    )

    layout["body"].update(body)
    return layout


def _poll_key() -> Optional[str]:
    """Lê uma tecla pressionada sem bloquear, se disponível."""
    if _IS_WINDOWS and msvcrt:
        if msvcrt.kbhit():  # type: ignore[attr-defined]
            ch = msvcrt.getch().decode(errors="ignore")  # type: ignore[attr-defined]
            if ch:
                return ch.lower()
        return None
    else:
        try:
            dr, _, _ = select.select([sys.stdin], [], [], 0)
            if dr:
                ch = sys.stdin.read(1)
                return ch.lower()
        except Exception:
            return None
    return None


def _handle_key(ch: str) -> bool:
    """Aplica ação com base na tecla. Retorna True para continuar, False para sair."""
    global current_category
    if ch == "1":
        current_category = "performance"
    elif ch == "2":
        current_category = "thermal"
    elif ch == "3":
        current_category = "pressure"
    elif ch == "4":
        current_category = "movement"
    elif ch in ("a", "A"):
        current_category = "all"
    elif ch in ("q", "Q"):
        return False
    return True


def run(refresh_rate: float = 0.2) -> None:
    reader = MockObdReader()
    reader.connect()
    try:
        with Live(console=console, refresh_per_second=int(1 / refresh_rate) or 5, screen=True) as live:
            running = True
            while running:
                payload = normalize(reader.read())
                live.update(build_layout(payload))
                ch = _poll_key()
                if ch:
                    running = _handle_key(ch)
                time.sleep(refresh_rate)
    except KeyboardInterrupt:
        console.print("\n[bold yellow]⏹ Interrompido pelo usuário[/bold yellow]")
    finally:
        reader.close()


if __name__ == "__main__":
    run(0.2)