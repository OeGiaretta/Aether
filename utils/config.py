# utils/config.py
import os
from dataclasses import dataclass
from dotenv import load_dotenv

@dataclass(frozen=True)
class AppConfig:
    source: str
    device: str | None
    refresh_rate: float
    debug: bool

def load_config() -> AppConfig:
    load_dotenv()
    source = os.getenv("SOURCE", "mock").lower()
    device = os.getenv("OBD_DEVICE")
    refresh_rate = float(os.getenv("REFRESH_RATE", "1.0"))
    debug = os.getenv("DEBUG", "false").lower() == "true"

    if source not in ("mock", "obd"):
        source = "mock"
    if refresh_rate <= 0:
        refresh_rate = 1.0

    return AppConfig(source=source, device=device, refresh_rate=refresh_rate, debug=debug)