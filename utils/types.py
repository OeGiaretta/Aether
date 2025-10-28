from __future__ import annotations

from typing import Dict, List, Literal, NotRequired, Optional, Protocol, TypedDict


# Fontes válidas para identificação da origem dos dados
SourceType = Literal["mock", "obd"]


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


class ReaderConfig(TypedDict, total=False):
    device: Optional[str]
    baudrate: int
    refresh_rate: float


class ObdReader(Protocol):
    @property
    def source(self) -> SourceType:  # "mock" ou "obd"
        ...

    @property
    def connected(self) -> bool:
        ...

    def connect(self, config: Optional[ReaderConfig] = None) -> None:
        ...

    def read(self) -> TelemetryPayload:
        ...

    def close(self) -> None:
        ...


