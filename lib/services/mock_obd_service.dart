import 'dart:math';

import '../models/vehicle_data.dart';

class MockObdService {
  final Random _random = Random();

  VehicleData generateData() {
    return VehicleData(
      rpm: (800 + _random.nextInt(1200)).toDouble(),
      speed: _random.nextInt(100).toDouble(),
      coolantTemperature:
          (80 + _random.nextInt(15)).toDouble(),
      voltage: 13.8 + _random.nextDouble() * 0.7,
      throttlePosition:
          _random.nextDouble() * 40,
    );
  }
}