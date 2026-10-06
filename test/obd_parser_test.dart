import 'package:flutter_test/flutter_test.dart';

import 'package:aether/utils/obd_parser.dart';

void main() {
  group('ObdParser', () {
    test('deve interpretar RPM corretamente', () {
      final rpm = ObdParser.parseRpm(
        '41 0C 1A F8',
      );

      expect(rpm, 1726);
    });

    test('deve interpretar velocidade corretamente', () {
      final speed = ObdParser.parseSpeed(
        '41 0D 3C',
      );

      expect(speed, 60);
    });

    test('deve interpretar temperatura corretamente', () {
      final temperature =
          ObdParser.parseCoolantTemperature(
        '41 05 5A',
      );

      expect(temperature, 50);
    });

    test('deve interpretar acelerador corretamente', () {
      final throttle =
          ObdParser.parseThrottlePosition(
        '41 11 80',
      );

      expect(throttle, closeTo(50.2, 0.1));
    });

    test('deve interpretar tensão corretamente', () {
      final voltage = ObdParser.parseVoltage(
        '41 42 37 00',
      );

      expect(voltage, 14.08);
    });
  });
}