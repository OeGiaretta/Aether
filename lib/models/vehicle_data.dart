class VehicleData {
  final double rpm;
  final double speed;
  final double coolantTemperature;
  final double voltage;
  final double throttlePosition;

  const VehicleData({
    this.rpm = 0,
    this.speed = 0,
    this.coolantTemperature = 0,
    this.voltage = 0,
    this.throttlePosition = 0,
  });

  VehicleData copyWith({
    double? rpm,
    double? speed,
    double? coolantTemperature,
    double? voltage,
    double? throttlePosition,
  }) {
    return VehicleData(
      rpm: rpm ?? this.rpm,
      speed: speed ?? this.speed,
      coolantTemperature:
          coolantTemperature ?? this.coolantTemperature,
      voltage: voltage ?? this.voltage,
      throttlePosition:
          throttlePosition ?? this.throttlePosition,
    );
  }
}