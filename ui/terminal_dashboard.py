import sys, os, time
from collections import deque
from datetime import datetime
from typing import Deque, Dict, List, Optional

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
    title = f"AETHER TUI — {ts}  |  source={src}  |  errors={errs}  |  category={current_category.upper()}"
    return Panel(title, style="bold magenta", border_style="magenta")


def controls_panel() -> Panel:
    lines = [
        "[bold]Controls[/bold]  [dim](press keys)[/dim]",
        "[1] Performance   [2] Thermal   [3] Pressure   [4] Movement   [A] All   [Q] Quit",
        f"[dim]Current: {current_category.upper()}[/dim]",
    ]
    return Panel("\n".join(lines), border_style="white")


def gauge_row(name: str, value: float, unit: str, lo: float, hi: float, ok: bool) -> Table:
    tbl = Table.grid(expand=True)
    tbl.add_column(ratio=3)
    tbl.add_column(ratio=6)
    tbl.add_column(ratio=3, justify="right")

    # Barra curta para caber no terminal
    term_width = console.size.width
    bar_len = max(8, min(24, term_width // 6))

    p = percent(value, lo, hi)
    filled = int(p * bar_len)
    bar = Text("█" * filled + "░" * (bar_len - filled))
    bar.stylize("green" if ok else "red")

    left = Text(name, style="bold cyan")
    right = Text(f"{value:.2f} {unit}")

    tbl.add_row(left, bar, right)
    return tbl


def sensors_gauges_panel(payload) -> Panel:
    names = CATEGORIES.get(current_category, CATEGORIES["all"])
    grid = Table.grid(expand=True)
    grid.add_column()
    grid.add_column()

    # duas colunas compactas
    mid = (len(names) + 1) // 2
    left_names = names[:mid]
    right_names = names[mid:]

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
    table = Table(expand=True, show_header=True, header_style="bold white")
    table.add_column("Sensor", style="cyan", ratio=3)
    table.add_column("Value", justify="right", ratio=2)
    table.add_column("Unit", ratio=1)
    table.add_column("Status", justify="center", ratio=1)

    for n in names:
        if n not in payload["sensors"]:
            continue
        sv = payload["sensors"][n]
        val_txt = "—" if sv["value"] is None else f"{sv['value']:.2f}"
        status = Text("OK", style="green") if sv["ok"] else Text("ERR", style="red")
        table.add_row(n, val_txt, sv["unit"], status)

    return Panel(table, title="Sensors", border_style="cyan")


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
    # Cabeçalho, corpo (gauges + tabela), controles e erros
    layout.split_column(
        Layout(header_panel(payload), name="header", size=3),
        Layout(name="body"),
        Layout(controls_panel(), name="controls", size=3),
        Layout(errors_panel(payload), name="errors", size=4),
    )
    # Dentro do corpo, empilhamos gauges e tabela para caber na tela
    body = Layout()
    body.split_column(
        Layout(sensors_gauges_panel(payload), name="gauges", size=console.size.height // 3),
        Layout(sensors_status_table_panel(payload), name="table"),
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