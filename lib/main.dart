import 'dart:async';

import 'package:flutter/material.dart';

import 'models/vehicle_data.dart';
import 'services/bluetooth_service.dart';
import 'services/mock_obd_service.dart';

void main() {
  runApp(const AetherApp());
}

class AetherApp extends StatelessWidget {
  const AetherApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      debugShowCheckedModeBanner: false,
      title: 'Aether',
      theme: ThemeData(
        brightness: Brightness.dark,
        scaffoldBackgroundColor: const Color(0xFF090D12),
        colorScheme: ColorScheme.fromSeed(
          seedColor: const Color(0xFF00D9FF),
          brightness: Brightness.dark,
        ),
        useMaterial3: true,
      ),
      home: const DashboardPage(),
    );
  }
}

class DashboardPage extends StatefulWidget {
  const DashboardPage({super.key});

  @override
  State<DashboardPage> createState() => _DashboardPageState();
}

class _DashboardPageState extends State<DashboardPage> {
  Timer? _telemetryTimer;

  final BluetoothService _bluetoothService = BluetoothService();
  final MockObdService _mockObdService = MockObdService();

  VehicleData _vehicleData = const VehicleData();

  bool _obdConectado = false;
  bool _conectando = false;

  @override
  void initState() {
    super.initState();

    _telemetryTimer = Timer.periodic(
      const Duration(milliseconds: 500),
      (_) {
        if (!mounted) return;

        // Enquanto não temos um OBD real conectado,
        // utilizamos dados simulados.
        if (!_obdConectado) {
          setState(() {
            _vehicleData = _mockObdService.generateData();
          });
        }
      },
    );
  }

  @override
  void dispose() {
    _telemetryTimer?.cancel();
    super.dispose();
  }

  Future<void> _selecionarDispositivoBluetooth() async {
    try {
      final permissao =
          await _bluetoothService.requestPermissions();

      if (!permissao) {
        if (!mounted) return;

        ScaffoldMessenger.of(context).showSnackBar(
          const SnackBar(
            content: Text(
              'Permissão Bluetooth negada.',
            ),
          ),
        );

        return;
      }

      final dispositivos =
          await _bluetoothService.getPairedDevices();

      debugPrint(
        'Dispositivos encontrados: $dispositivos',
      );

      if (!mounted) return;

      if (dispositivos.isEmpty) {
        ScaffoldMessenger.of(context).showSnackBar(
          const SnackBar(
            content: Text(
              'Nenhum dispositivo Bluetooth pareado encontrado.',
            ),
          ),
        );

        return;
      }

      final dispositivoSelecionado =
          await showModalBottomSheet<Map<String, String>>(
        context: context,
        backgroundColor: const Color(0xFF111820),
        builder: (context) {
          return SafeArea(
            child: Padding(
              padding: const EdgeInsets.all(20),
              child: Column(
                mainAxisSize: MainAxisSize.min,
                crossAxisAlignment:
                    CrossAxisAlignment.start,
                children: [
                  const Text(
                    'DISPOSITIVOS BLUETOOTH',
                    style: TextStyle(
                      color: Colors.white,
                      fontSize: 18,
                      fontWeight: FontWeight.bold,
                      letterSpacing: 1.2,
                    ),
                  ),
                  const SizedBox(height: 16),
                  Flexible(
                    child: ListView(
                      shrinkWrap: true,
                      children: dispositivos.map(
                        (dispositivo) {
                          final nome =
                              dispositivo['name'] ??
                                  'Dispositivo desconhecido';

                          final endereco =
                              dispositivo['address'] ?? '';

                          return ListTile(
                            leading: const Icon(
                              Icons.bluetooth,
                              color: Color(0xFF00D9FF),
                            ),
                            title: Text(
                              nome,
                              style: const TextStyle(
                                color: Colors.white,
                                fontWeight: FontWeight.bold,
                              ),
                            ),
                            subtitle: Text(
                              endereco,
                              style: const TextStyle(
                                color: Colors.white54,
                              ),
                            ),
                            onTap: () {
                              Navigator.pop(
                                context,
                                dispositivo,
                              );
                            },
                          );
                        },
                      ).toList(),
                    ),
                  ),
                ],
              ),
            ),
          );
        },
      );

      if (!mounted) return;

      if (dispositivoSelecionado == null) {
        return;
      }

      final nome =
          dispositivoSelecionado['name'] ??
              'Dispositivo';

      final endereco =
          dispositivoSelecionado['address'];

      if (endereco == null || endereco.isEmpty) {
        return;
      }

      debugPrint(
        'Conectando ao dispositivo: $nome - $endereco',
      );

      setState(() {
        _conectando = true;
      });

      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(
          content: Text(
            'Conectando ao $nome...',
          ),
        ),
      );

      final conectado =
          await _bluetoothService.connect(endereco);

      if (!mounted) return;

      setState(() {
        _obdConectado = conectado;
        _conectando = false;
      });

      if (conectado) {
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(
            content: Text(
              'Conectado ao $nome',
            ),
          ),
        );

        // =====================================================
        // TESTE OBD
        // Comando 010C = RPM
        // =====================================================

        debugPrint(
          'Enviando comando OBD: 010C',
        );

        try {
          await _bluetoothService.write('010C\r');

          debugPrint(
            'Comando 010C enviado.',
          );

          final resposta =
              await _bluetoothService.readLine();

          debugPrint(
            'Resposta OBD: $resposta',
          );
        } catch (e) {
          debugPrint(
            'Erro ao ler resposta OBD: $e',
          );
        }
      } else {
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(
            content: Text(
              'Não foi possível conectar ao $nome',
            ),
          ),
        );
      }
    } catch (e) {
      debugPrint(
        'Erro ao acessar Bluetooth: $e',
      );

      if (!mounted) return;

      setState(() {
        _obdConectado = false;
        _conectando = false;
      });

      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(
          content: Text(
            'Erro ao acessar Bluetooth: $e',
          ),
        ),
      );
    }
  }

  Future<void> _desconectarObd() async {
    try {
      await _bluetoothService.disconnect();

      if (!mounted) return;

      setState(() {
        _obdConectado = false;
        _conectando = false;
      });

      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(
          content: Text('OBD desconectado.'),
        ),
      );
    } catch (e) {
      debugPrint('Erro ao desconectar OBD: $e');

      if (!mounted) return;

      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(
          content: Text('Erro ao desconectar OBD: $e'),
        ),
      );
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        backgroundColor: const Color(0xFF090D12),
        elevation: 0,
        title: const Text(
          'AETHER',
          style: TextStyle(
            fontWeight: FontWeight.bold,
            letterSpacing: 3,
          ),
        ),
        actions: [
          IconButton(
            onPressed: () {},
            icon: const Icon(
              Icons.settings_outlined,
            ),
          ),
        ],
      ),
      body: SafeArea(
        child: SingleChildScrollView(
          padding: const EdgeInsets.all(16),
          child: Column(
            crossAxisAlignment:
                CrossAxisAlignment.start,
            children: [
              _connectionStatus(),

              const SizedBox(height: 24),

              const Text(
                'TELEMETRIA',
                style: TextStyle(
                  fontSize: 13,
                  fontWeight: FontWeight.bold,
                  letterSpacing: 2,
                  color: Color(0xFF8A939E),
                ),
              ),

              const SizedBox(height: 12),

              Row(
                children: [
                  Expanded(
                    child: _metricCard(
                      title: 'RPM',
                      value:
                          _vehicleData.rpm
                              .toStringAsFixed(0),
                      unit: 'rpm',
                      icon: Icons.speed,
                    ),
                  ),

                  const SizedBox(width: 12),

                  Expanded(
                    child: _metricCard(
                      title: 'VELOCIDADE',
                      value:
                          _vehicleData.speed
                              .toStringAsFixed(0),
                      unit: 'km/h',
                      icon: Icons.directions_car,
                    ),
                  ),
                ],
              ),

              const SizedBox(height: 12),

              Row(
                children: [
                  Expanded(
                    child: _metricCard(
                      title: 'TEMPERATURA',
                      value:
                          _vehicleData
                              .coolantTemperature
                              .toStringAsFixed(0),
                      unit: '°C',
                      icon: Icons.thermostat,
                    ),
                  ),

                  const SizedBox(width: 12),

                  Expanded(
                    child: _metricCard(
                      title: 'TENSÃO',
                      value:
                          _vehicleData.voltage
                              .toStringAsFixed(1),
                      unit: 'V',
                      icon:
                          Icons.battery_charging_full,
                    ),
                  ),
                ],
              ),

              const SizedBox(height: 24),

              _largeMetricCard(),

              const SizedBox(height: 24),

              SizedBox(
                width: double.infinity,
                height: 54,
                child: ElevatedButton.icon(
                  onPressed:
                      _conectando
                          ? null
                          : _obdConectado
                              ? _desconectarObd
                              : _selecionarDispositivoBluetooth,
                  icon: const Icon(
                    Icons.bluetooth,
                  ),
                  label: Text(
                    _conectando
                        ? 'CONECTANDO...'
                        : _obdConectado
                            ? 'DESCONECTAR OBD'
                            : 'CONECTAR OBD',
                    style: const TextStyle(
                      fontWeight: FontWeight.bold,
                      letterSpacing: 1.5,
                    ),
                  ),
                  style:
                      ElevatedButton.styleFrom(
                    backgroundColor:
                        const Color(0xFF00D9FF),
                    foregroundColor: Colors.black,
                    shape:
                        RoundedRectangleBorder(
                      borderRadius:
                          BorderRadius.circular(12),
                    ),
                  ),
                ),
              ),
            ],
          ),
        ),
      ),
    );
  }

  Widget _connectionStatus() {
    final conectado = _obdConectado;
    final conectando = _conectando;

    final Color statusColor;

    if (conectando) {
      statusColor = Colors.orangeAccent;
    } else if (conectado) {
      statusColor = Colors.greenAccent;
    } else {
      statusColor = Colors.redAccent;
    }

    final String statusText;

    if (conectando) {
      statusText = 'CONECTANDO...';
    } else if (conectado) {
      statusText = 'OBD CONECTADO';
    } else {
      statusText = 'OBD DESCONECTADO';
    }

    return Container(
      padding: const EdgeInsets.symmetric(
        horizontal: 14,
        vertical: 12,
      ),
      decoration: BoxDecoration(
        color: const Color(0xFF11171E),
        borderRadius:
            BorderRadius.circular(12),
        border: Border.all(
          color: const Color(0xFF202832),
        ),
      ),
      child: Row(
        children: [
          Container(
            width: 10,
            height: 10,
            decoration: BoxDecoration(
              color: statusColor,
              shape: BoxShape.circle,
            ),
          ),

          const SizedBox(width: 10),

          Text(
            statusText,
            style: const TextStyle(
              fontSize: 12,
              fontWeight: FontWeight.bold,
              letterSpacing: 1,
            ),
          ),
        ],
      ),
    );
  }

  Widget _metricCard({
    required String title,
    required String value,
    required String unit,
    required IconData icon,
  }) {
    return Container(
      padding: const EdgeInsets.all(16),
      decoration: BoxDecoration(
        color: const Color(0xFF11171E),
        borderRadius:
            BorderRadius.circular(16),
        border: Border.all(
          color: const Color(0xFF202832),
        ),
      ),
      child: Column(
        crossAxisAlignment:
            CrossAxisAlignment.start,
        children: [
          Icon(
            icon,
            size: 20,
            color: const Color(0xFF00D9FF),
          ),

          const SizedBox(height: 14),

          Text(
            title,
            style: const TextStyle(
              fontSize: 11,
              color: Color(0xFF8A939E),
              fontWeight: FontWeight.bold,
              letterSpacing: 1,
            ),
          ),

          const SizedBox(height: 6),

          Row(
            crossAxisAlignment:
                CrossAxisAlignment.end,
            children: [
              Text(
                value,
                style: const TextStyle(
                  fontSize: 26,
                  fontWeight: FontWeight.bold,
                ),
              ),

              const SizedBox(width: 4),

              Padding(
                padding:
                    const EdgeInsets.only(
                  bottom: 3,
                ),
                child: Text(
                  unit,
                  style: const TextStyle(
                    fontSize: 11,
                    color: Color(0xFF8A939E),
                  ),
                ),
              ),
            ],
          ),
        ],
      ),
    );
  }

  Widget _largeMetricCard() {
    final bool conectado = _obdConectado;

    return Container(
      width: double.infinity,
      padding: const EdgeInsets.all(20),
      decoration: BoxDecoration(
        color: const Color(0xFF11171E),
        borderRadius:
            BorderRadius.circular(16),
        border: Border.all(
          color: const Color(0xFF202832),
        ),
      ),
      child: Column(
        crossAxisAlignment:
            CrossAxisAlignment.start,
        children: [
          const Text(
            'STATUS DO MOTOR',
            style: TextStyle(
              fontSize: 11,
              color: Color(0xFF8A939E),
              fontWeight: FontWeight.bold,
              letterSpacing: 1,
            ),
          ),

          const SizedBox(height: 12),

          Row(
            children: [
              Container(
                width: 12,
                height: 12,
                decoration: BoxDecoration(
                  color: conectado
                      ? Colors.greenAccent
                      : const Color(0xFF00D9FF),
                  shape: BoxShape.circle,
                ),
              ),

              const SizedBox(width: 10),

              Text(
                conectado
                    ? 'OBD CONECTADO'
                    : 'AGUARDANDO CONEXÃO',
                style: const TextStyle(
                  fontSize: 15,
                  fontWeight: FontWeight.bold,
                ),
              ),
            ],
          ),
        ],
      ),
    );
  }
}