import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import '../l10n/app_localizations.dart';
import '../providers/app_provider.dart';

class VaultScreen extends StatelessWidget {
  const VaultScreen({super.key});

  @override
  Widget build(BuildContext context) {
    final l10n = AppLocalizations.of(context);
    final provider = context.watch<AppProvider>();
    final items = provider.lockedEntries;

    return Scaffold(
      backgroundColor: Colors.black,
      appBar: AppBar(
        backgroundColor: const Color(0xFF0A0A0A),
        title: Text('${l10n.lockedVault} (${items.length})'),
      ),
      body: Column(
        children: [
          Container(
            margin: const EdgeInsets.all(14),
            padding: const EdgeInsets.all(12),
            decoration: BoxDecoration(
              color: const Color(0xFF141414),
              borderRadius: BorderRadius.circular(12),
              border: Border.all(color: Colors.white12),
            ),
            child: const Text(
              'Security Note: Locked PDFs are moved into private app-managed vault storage and hidden from normal listings behind your App Lock PIN/Biometric gate. For maximum security, enable App Lock in the Me tab.',
              style: TextStyle(color: Colors.white70, fontSize: 12),
            ),
          ),
          Expanded(
            child: items.isEmpty
                ? const Center(
                    child: Text('No locked documents.', style: TextStyle(color: Colors.white60)),
                  )
                : ListView.builder(
                    itemCount: items.length,
                    itemBuilder: (context, index) {
                      final entry = items[index];
                      return Card(
                        color: const Color(0xFF101010),
                        margin: const EdgeInsets.symmetric(horizontal: 14, vertical: 6),
                        child: ListTile(
                          leading: const Icon(Icons.lock, color: Color(0xFFDC143C)),
                          title: Text(entry.fileName),
                          trailing: FilledButton.tonalIcon(
                            icon: const Icon(Icons.lock_open),
                            label: const Text('Unlock'),
                            onPressed: () async {
                              await provider.securityService.unlockPdfDocument(
                                entry,
                                provider.fileService,
                              );
                              await provider.refreshAll();
                            },
                          ),
                        ),
                      );
                    },
                  ),
          ),
        ],
      ),
    );
  }
}
