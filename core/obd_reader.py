import time, math, random
from utils.types import TelemetryPayload, SensorValue, ReaderConfig, ObdReader
from core.sensor_map import SENSOR_MAP

class MockObdReader:
    def __init__(self) -> None:
        self._connected = False

    @property
    def source(self):
        return "mock"
    
    @property
    def connected(self) -> bool:
        return self._connected

    def connect(self, config: ReaderConfig | None = None) -> None:
        self._connected = True

    def _gen(self, name: str, t: float) -> float:
        # Generate a random value for a given sensor name and time
        m = SENSOR_MAP[name]
        lo, hi = m["min"], m["max"]
        base = (math.sin(t / 2.0) + 1.0) / 2.0
        noise = random.uniform(-0.05, 0.05)
        x = max(0.0, min(1.0, base + noise))
        return lo + x * (hi - lo)

    def read(self) -> TelemetryPayload:
        now = time.time()
        sensors: dict[str, SensorValue] = {}
        for name, meta in SENSOR_MAP.items():
            val = self._gen(name, now)
            sensors[name] = {
                "value": float(val),
                "unit": meta["unit"],
                "ok": True,
                "meta": {"min": meta["min"], "max": meta["max"]},
            }
        return {
            "timestamp": now, 
            "sensors": sensors, 
            "source": "mock", 
            "errors": []
        }

    def close(self) -> None:
        self._connected = False
