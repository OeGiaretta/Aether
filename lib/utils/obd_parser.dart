class ObdParser {
  static double? parseRpm(String response) {
    final bytes = _extractBytes(response);

    if (bytes.length < 4) {
      return null;
    }

    if (bytes[0] != 0x41 || bytes[1] != 0x0C) {
      return null;
    }

    final a = bytes[2];
    final b = bytes[3];

    return ((a * 256) + b) / 4;
  }

  static double? parseSpeed(String response) {
    final bytes = _extractBytes(response);

    if (bytes.length < 3) {
      return null;
    }

    if (bytes[0] != 0x41 || bytes[1] != 0x0D) {
      return null;
    }

    return bytes[2].toDouble();
  }

  static double? parseCoolantTemperature(
    String response,
  ) {
    final bytes = _extractBytes(response);

    if (bytes.length < 3) {
      return null;
    }

    if (bytes[0] != 0x41 || bytes[1] != 0x05) {
      return null;
    }

    return bytes[2] - 40;
  }

  static double? parseThrottlePosition(
    String response,
  ) {
    final bytes = _extractBytes(response);

    if (bytes.length < 3) {
      return null;
    }

    if (bytes[0] != 0x41 || bytes[1] != 0x11) {
      return null;
    }

    return (bytes[2] * 100) / 255;
  }

  static double? parseVoltage(String response) {
    final bytes = _extractBytes(response);

    if (bytes.length < 4) {
      return null;
    }

    if (bytes[0] != 0x41 || bytes[1] != 0x42) {
      return null;
    }

    final value = (bytes[2] * 256) + bytes[3];

    return value / 1000;
  }

  static List<int> _extractBytes(String response) {
    final cleaned = response
        .replaceAll(' ', '')
        .replaceAll('\r', '')
        .replaceAll('\n', '')
        .trim();

    if (cleaned.isEmpty) {
      return [];
    }

    final bytes = <int>[];

    for (var i = 0; i + 1 < cleaned.length; i += 2) {
      final byte = int.tryParse(
        cleaned.substring(i, i + 2),
        radix: 16,
      );

      if (byte == null) {
        continue;
      }

      bytes.add(byte);
    }

    return bytes;
  }
}