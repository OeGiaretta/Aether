import 'package:bluetooth_serial_android/bluetooth_serial_android.dart';

class BluetoothService {
  Future<bool> requestPermissions() async {
    return await FlutterBluetoothSerial.ensurePermissions();
  }

  Future<List<Map<String, String>>> getPairedDevices() async {
    return await FlutterBluetoothSerial.getPairedDevices();
  }

  Future<List<Map<String, String>>> scanDevices() async {
    return await FlutterBluetoothSerial.scanDevices();
  }

  Future<bool> connect(String address) async {
    return await FlutterBluetoothSerial.connect(
      address,
      timeoutMs: 5000,
    );
  }

  Future<void> disconnect() async {
    await FlutterBluetoothSerial.disconnect();
  }

  Future<void> write(String message) async {
    await FlutterBluetoothSerial.write(message);
  }

  Future<String?> read() async {
    return await FlutterBluetoothSerial.read();
  }

  Future<String?> readLine() async {
    return await FlutterBluetoothSerial.readLine('\r');
  }
}