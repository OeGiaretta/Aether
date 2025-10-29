# utils/helpers.py
from collections import deque
from typing import Iterable, Deque

def clamp(value: float, lo: float, hi: float) -> float:
    return lo if value < lo else hi if value > hi else value

def moving_average(values: Iterable[float], window: int) -> float:
    vals = list(values)[-window:]
    return sum(vals)/len(vals) if vals else 0.0

def ema(prev: float | None, new: float, alpha: float = 0.2) -> float:
    return new if prev is None else (alpha * new + (1 - alpha) * prev)

def c_to_f(c: float) -> float: return c * 9/5 + 32
def kpa_to_bar(kpa: float) -> float: return kpa / 100.0
def kmh_to_mph(kmh: float) -> float: return kmh * 0.621371

class RollingWindow:
    def __init__(self, capacity: int):
        self._buf: Deque[float] = deque(maxlen=capacity)
    def add(self, v: float) -> None: self._buf.append(v)
    def values(self) -> list[float]: return list(self._buf)
    def min(self) -> float | None: return min(self._buf) if self._buf else None
    def max(self) -> float | None: return max(self._buf) if self._buf else None
    def avg(self) -> float | None:
        return (sum(self._buf)/len(self._buf)) if self._buf else None