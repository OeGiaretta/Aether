import '../models/vehicle_data.dart';
import '../utils/obd_parser.dart';
import 'bluetooth_service.dart';

class ObdService {
  final BluetoothService bluetoothService;

  ObdService({
    required this.bluetoothService,
  });

  Future<void> initialize() async {
    await _sendCommand('ATZ');
    await _sendCommand('ATE0');
    await _sendCommand('ATL0');
    await _sendCommand('ATS0');
  }

  Future<String?> _sendCommand(String command) async {
    await bluetoothService.write('$command\r');
    return await bluetoothService.readLine();
  }

  Future<double?> readRpm() async {
    final response = await _sendCommand('010C');

    if (response == null) {
      return null;
    }

    return ObdParser.parseRpm(response);
  }

  Future<double?> readSpeed() async {
    final response = await _sendCommand('010D');

    if (response == null) {
      return null;
    }

    return ObdParser.parseSpeed(response);
  }

  Future<double?> readCoolantTemperature() async {
    final response = await _sendCommand('0105');

    if (response == null) {
      return null;
    }

    return ObdParser.parseCoolantTemperature(response);
  }

  Future<double?> readThrottlePosition() async {
    final response = await _sendCommand('0111');

    if (response == null) {
      return null;
    }

    return ObdParser.parseThrottlePosition(response);
  }

  Future<double?> readVoltage() async {
    final response = await _sendCommand('0142');

    if (response == null) {
      return null;
    }

    return ObdParser.parseVoltage(response);
  }

  Future<VehicleData> readVehicleData() async {
    final rpm = await readRpm();
    final speed = await readSpeed();
    final temperature =
        await readCoolantTemperature();
    final throttle =
        await readThrottlePosition();
    final voltage = await readVoltage();

    return VehicleData(
      rpm: rpm ?? 0,
      speed: speed ?? 0,
      coolantTemperature: temperature ?? 0,
      throttlePosition: throttle ?? 0,
      voltage: voltage ?? 0,
    );
  }
}