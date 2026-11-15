import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import '../l10n/app_localizations.dart';
import '../providers/app_provider.dart';
import '../widgets/pin_dialog.dart';

class MeScreen extends StatelessWidget {
  const MeScreen({super.key});

  String _fmtBytes(int bytes) {
    if (bytes < 1024 * 1024) return '${(bytes / 1024).toStringAsFixed(1)} KB';
    return '${(bytes / (1024 * 1024)).toStringAsFixed(2)} MB';
  }

  @override
  Widget build(BuildContext context) {
    final l10n = AppLocalizations.of(context);
    final provider = context.watch<AppProvider>();
    final stats = provider.storageStats;

    return ListView(
      padding: const EdgeInsets.all(14),
      children: [
        Card(
          color: const Color(0xFF101010),
          child: Padding(
            padding: const EdgeInsets.all(16),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text(
                  l10n.storageInfo,
                  style: const TextStyle(fontWeight: FontWeight.bold, fontSize: 16),
                ),
                const SizedBox(height: 8),
                Text('Discovered PDFs: ${stats.managedPdfCount} (${_fmtBytes(stats.managedPdfBytes)})'),
                Text('Recycle Bin: ${_fmtBytes(stats.binBytes)}'),
                Text('Locked Vault: ${_fmtBytes(stats.vaultBytes)}'),
              ],
            ),
          ),
        ),
        const SizedBox(height: 8),
        SwitchListTile(
          title: Text(l10n.appLock),
          subtitle: const Text('Require PIN / Biometrics on launch'),
          value: provider.appLockEnabled,
          activeThumbColor: const Color(0xFFDC143C),
          onChanged: (enable) async {
            if (enable) {
              final pin = await showPinPromptDialog(
                context,
                title: 'Create App Lock PIN',
                subtitle: 'Enter a 4–6 digit PIN to protect PDF Pro No Ad.',
              );
              if (pin != null) {
                await provider.securityService.setAppPin(pin);
                await provider.refreshSecurityState();
              }
            } else {
              await provider.securityService.disableAppLock();
              await provider.refreshSecurityState();
            }
          },
        ),
        if (provider.appLockEnabled)
          SwitchListTile(
            title: const Text('Biometric Unlock'),
            subtitle: const Text('Use Fingerprint or Face authentication'),
            value: provider.biometricEnabled,
            activeThumbColor: const Color(0xFFDC143C),
            onChanged: (val) async {
              await provider.securityService.setBiometricEnabled(val);
              await provider.refreshSecurityState();
            },
          ),
        ListTile(
          leading: const Icon(Icons.language, color: Color(0xFFDC143C)),
          title: Text(l10n.language),
          trailing: SegmentedButton<String>(
            segments: const [
              ButtonSegment(value: 'en', label: Text('EN')),
              ButtonSegment(value: 'bn', label: Text('বাংলা')),
            ],
            selected: {provider.locale.languageCode},
            onSelectionChanged: (s) => provider.setLocale(s.first),
          ),
        ),
        SwitchListTile(
          secondary: const Icon(Icons.contrast, color: Color(0xFFDC143C)),
          title: Text(l10n.theme),
          subtitle: const Text('AMOLED Black Primary Mode'),
          value: provider.themeMode == ThemeMode.dark,
          activeThumbColor: const Color(0xFFDC143C),
          onChanged: provider.setDarkMode,
        ),
        SwitchListTile(
          secondary: const Icon(Icons.hdr_auto, color: Color(0xFFDC143C)),
          title: Text(l10n.scannerPrefs),
          subtitle: const Text('Enable Auto-Capture by default in scanner'),
          value: provider.autoCaptureDefault,
          activeThumbColor: const Color(0xFFDC143C),
          onChanged: provider.setAutoCaptureDefault,
        ),
        ListTile(
          leading: const Icon(Icons.folder_special, color: Color(0xFFDC143C)),
          title: const Text('Storage Folder Selection'),
          subtitle: const Text('Authorize additional folders for PDF scanning'),
          onTap: () async {
            await provider.fileService.authorizeNewFolder();
            await provider.refreshAll();
          },
        ),
        ListTile(
          leading: const Icon(Icons.shield_outlined, color: Color(0xFFDC143C)),
          title: Text(l10n.privacySecurity),
          onTap: () => showDialog(
            context: context,
            builder: (ctx) => AlertDialog(
              backgroundColor: const Color(0xFF141414),
              title: Text(l10n.privacySecurity),
              content: const Text(
                '• 100% Offline-First: No INTERNET permission in AndroidManifest.\n'
                '• Zero advertisements, trackers, or analytics.\n'
                '• All scanning, perspective correction, and PDF conversions run locally on your device.\n'
                '• Locked files are isolated in app-managed storage behind your PIN/Biometric lock.',
              ),
              actions: [
                TextButton(onPressed: () => Navigator.pop(ctx), child: const Text('Close')),
              ],
            ),
          ),
        ),
        ListTile(
          leading: const Icon(Icons.info_outline, color: Color(0xFFDC143C)),
          title: Text(l10n.about),
          subtitle: const Text('PDF Pro No Ad • v1.0.0 (com.comeback.pdfprona)'),
        ),
        ListTile(
          leading: const Icon(Icons.mail_outline, color: Color(0xFFDC143C)),
          title: Text(l10n.contact),
          subtitle: const Text('support@comeback.dev (Offline Support Reference)'),
        ),
      ],
    );
  }
}
