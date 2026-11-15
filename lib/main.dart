import 'package:flutter/material.dart';
import 'package:flutter_localizations/flutter_localizations.dart';
import 'package:provider/provider.dart';
import 'l10n/app_localizations.dart';
import 'providers/app_provider.dart';
import 'screens/main_shell.dart';

Future<void> main() async {
  WidgetsFlutterBinding.ensureInitialized();
  final provider = AppProvider();
  await provider.initialize();

  runApp(
    ChangeNotifierProvider.value(
      value: provider,
      child: const PdfProNoAdApp(),
    ),
  );
}

class PdfProNoAdApp extends StatelessWidget {
  const PdfProNoAdApp({super.key});

  @override
  Widget build(BuildContext context) {
    final provider = context.watch<AppProvider>();

    const crimson = Color(0xFFDC143C);
    final darkScheme = ColorScheme.fromSeed(
      seedColor: crimson,
      brightness: Brightness.dark,
      primary: crimson,
      surface: Colors.black,
    );

    return MaterialApp(
      title: 'PDF Pro No Ad',
      debugShowCheckedModeBanner: false,
      locale: provider.locale,
      supportedLocales: const [Locale('en'), Locale('bn')],
      localizationsDelegates: const [
        AppLocalizationsDelegate(),
        GlobalMaterialLocalizations.delegate,
        GlobalWidgetsLocalizations.delegate,
        GlobalCupertinoLocalizations.delegate,
      ],
      themeMode: provider.themeMode,
      theme: ThemeData(
        useMaterial3: true,
        colorScheme: ColorScheme.fromSeed(seedColor: crimson, primary: crimson),
      ),
      darkTheme: ThemeData(
        useMaterial3: true,
        brightness: Brightness.dark,
        scaffoldBackgroundColor: Colors.black,
        colorScheme: darkScheme,
        filledButtonTheme: FilledButtonThemeData(
          style: FilledButton.styleFrom(
            backgroundColor: crimson,
            foregroundColor: Colors.white,
          ),
        ),
      ),
      home: provider.isUnlockedSession ? const MainShell() : const _AppLockScreen(),
    );
  }
}

class _AppLockScreen extends StatefulWidget {
  const _AppLockScreen();

  @override
  State<_AppLockScreen> createState() => _AppLockScreenState();
}

class _AppLockScreenState extends State<_AppLockScreen> {
  final TextEditingController _pinCtrl = TextEditingController();
  String? _error;

  @override
  void initState() {
    super.initState();
    WidgetsBinding.instance.addPostFrameCallback((_) => _tryBiometric());
  }

  Future<void> _tryBiometric() async {
    final provider = context.read<AppProvider>();
    if (!provider.biometricEnabled) return;
    final ok = await provider.securityService.authenticateBiometric();
    if (ok && mounted) {
      provider.unlockSession();
    }
  }

  Future<void> _verifyPin() async {
    final provider = context.read<AppProvider>();
    final ok = await provider.securityService.verifyPin(_pinCtrl.text.trim());
    if (ok) {
      provider.unlockSession();
    } else {
      setState(() => _error = 'Incorrect PIN. Please try again.');
    }
  }

  @override
  Widget build(BuildContext context) {
    final provider = context.watch<AppProvider>();

    return Scaffold(
      backgroundColor: Colors.black,
      body: Center(
        child: Padding(
          padding: const EdgeInsets.all(28),
          child: Column(
            mainAxisSize: MainAxisSize.min,
            children: [
              const Icon(Icons.lock_rounded, color: Color(0xFFDC143C), size: 54),
              const SizedBox(height: 14),
              const Text(
                'PDF Pro No Ad Locked',
                style: TextStyle(fontSize: 20, fontWeight: FontWeight.bold),
              ),
              const SizedBox(height: 18),
              TextField(
                controller: _pinCtrl,
                keyboardType: TextInputType.number,
                obscureText: true,
                maxLength: 6,
                textAlign: TextAlign.center,
                decoration: InputDecoration(
                  labelText: 'Enter PIN',
                  errorText: _error,
                  border: const OutlineInputBorder(),
                ),
                onSubmitted: (_) => _verifyPin(),
              ),
              const SizedBox(height: 10),
              SizedBox(
                width: double.infinity,
                child: FilledButton(
                  onPressed: _verifyPin,
                  child: const Text('Unlock'),
                ),
              ),
              if (provider.biometricEnabled) ...[
                const SizedBox(height: 10),
                TextButton.icon(
                  icon: const Icon(Icons.fingerprint),
                  label: const Text('Unlock with Biometrics'),
                  onPressed: _tryBiometric,
                ),
              ],
            ],
          ),
        ),
      ),
    );
  }
}
