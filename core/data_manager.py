from utils.types import TelemetryPayload
from core.sensor_map import SENSOR_MAP

def clamp(value: float, lo: float, hi: float) -> float:
    if value < lo:
        return lo
    if value > hi:
        return hi
    return value

def normalize(payload: TelemetryPayload) -> TelemetryPayload:
    sensors = {}
    errors = list(payload.get("errors", []))
    for name, meta in SENSOR_MAP.items():
        sv = payload["sensors"].get(name)
        if sv is None or sv["value"] is None:
            sensors[name] = {"value": None, "unit": meta["unit"], "ok": False, "meta": {"min": meta["min"], "max": meta["max"]}}
            errors.append(f"{name}: no data")
            continue
        v = float(sv["value"])
        lo, hi = float(meta["min"]), float(meta["max"])
        v2 = clamp(v, lo, hi)
        ok = (v == v2)  # ok=True se não precisou clamp (valor dentro da faixa)
        sensors[name] = {"value": v2, "unit": meta["unit"], "ok": ok, "meta": {"min": lo, "max": hi}}
        if not ok:
            errors.append(f"{name}: clamped ({v:.2f}->{v2:.2f})")
    return {"timestamp": payload["timestamp"], "sensors": sensors, "source": payload["source"], "errors": errors}