SENSOR_DEF = {
"rpm": {"unit": "rpm", "min":0.0, "max":8000.0, "pid": "010C"},
"speed": {"uni": "km/h", "min":0.0, "max":240.0, "pid": "010D"},
"coolant_temp": {"uni": "°C", "min":-40.0, "max":130.0, "pid": "0105"},
"throttle": {"uni": "%", "min":0.0, "max":100.0, "pid": "0111"},
"engine_load": {"uni": "%", "min":0.0, "max":100.0, "pid": "0104"},
"intake_temp": {"uni": "°C", "min":0.0, "max":100.0, "pid": "010F"},
"map": {"uni": "kPa", "min":0.0, "max":250.0, "pid": "0108"},
}
 # opcionalmente: "fuel_level": {"unit": "%", "min": 0.0, "max": 100.0, "pid": "012F"},
Primary_sensors = ["rpm", "speed", "coolant_temp", "throttle"]