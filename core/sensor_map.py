from utils.constants import SENSOR_DEF as SENSOR_MAP

SENSOR_MAP = {
    "rpm": {"unit": "rpm", "min": 0.0, "max": 8000.0, "pid": "010C"},
    "speed": {"unit": "km/h", "min": 0.0, "max": 240.0, "pid": "010D"},
    "coolant_temp": {"unit": "°C", "min": -40.0, "max": 130.0, "pid": "0105"},
    "throttle": {"unit": "%", "min": 0.0, "max": 100.0, "pid": "0111"},
    "engine_load": {"unit": "%", "min": 0.0, "max": 100.0, "pid": "0104"},
    "intake_temp": {"unit": "°C", "min": -40.0, "max": 100.0, "pid": "010F"},
    "map": {"unit": "kPa", "min": 10.0, "max": 250.0, "pid": "010B"},
    "fuel_pressure": {"unit": "kPa", "min": 0.0, "max": 500.0, "pid": "010A"},
    "fuel_level": {"unit": "%", "min": 0.0, "max": 100.0, "pid": "012F"},
    "fuel_consumption": {"unit": "L/h", "min": 0.0, "max": 100.0, "pid": "0110"},
    "fuel_consumption_rate": {"unit": "L/h", "min": 0.0, "max": 100.0, "pid": "0110"},
    "fuel_consumption_rate": {"unit": "L/h", "min": 0.0, "max": 100.0, "pid": "0110"},
}