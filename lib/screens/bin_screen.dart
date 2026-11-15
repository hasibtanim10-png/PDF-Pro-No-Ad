import 'package:flutter/material.dart';
import 'package:intl/intl.dart';
import 'package:provider/provider.dart';
import '../l10n/app_localizations.dart';
import '../providers/app_provider.dart';

class BinScreen extends StatelessWidget {
  const BinScreen({super.key});

  @override
  Widget build(BuildContext context) {
    final l10n = AppLocalizations.of(context);
    final provider = context.watch<AppProvider>();
    final items = provider.binEntries;

    return Scaffold(
      backgroundColor: Colors.black,
      appBar: AppBar(
        backgroundColor: const Color(0xFF0A0A0A),
        title: Text('${l10n.recycleBin} (${items.length})'),
      ),
      body: items.isEmpty
          ? const Center(
              child: Text('Recycle Bin is empty.', style: TextStyle(color: Colors.white60)),
            )
          : ListView.builder(
              itemCount: items.length,
              itemBuilder: (context, index) {
                final entry = items[index];
                return Card(
                  color: const Color(0xFF101010),
                  margin: const EdgeInsets.symmetric(horizontal: 14, vertical: 6),
                  child: ListTile(
                    leading: const Icon(Icons.delete_outline, color: Color(0xFFDC143C)),
                    title: Text(entry.fileName),
                    subtitle: Text(
                      'Moved: ${DateFormat('dd MMM yyyy, HH:mm').format(entry.movedAt)}',
                      style: const TextStyle(color: Colors.white60, fontSize: 12),
                    ),
                    trailing: Row(
                      mainAxisSize: MainAxisSize.min,
                      children: [
                        IconButton(
                          tooltip: l10n.restore,
                          icon: const Icon(Icons.restore, color: Colors.greenAccent),
                          onPressed: () async {
                            await provider.fileService.restoreFromBin(entry);
                            await provider.refreshAll();
                          },
                        ),
                        IconButton(
                          tooltip: l10n.deleteForever,
                          icon: const Icon(Icons.delete_forever, color: Color(0xFFDC143C)),
                          onPressed: () async {
                            final ok = await showDialog<bool>(
                              context: context,
                              builder: (ctx) => AlertDialog(
                                backgroundColor: const Color(0xFF141414),
                                title: Text(l10n.deleteForever),
                                content: Text(
                                  'Permanently delete "${entry.fileName}"? This cannot be undone.',
                                ),
                                actions: [
                                  TextButton(
                                    onPressed: () => Navigator.pop(ctx, false),
                                    child: Text(l10n.cancel),
                                  ),
                                  FilledButton(
                                    onPressed: () => Navigator.pop(ctx, true),
                                    child: Text(l10n.deleteForever),
                                  ),
                                ],
                              ),
                            );
                            if (ok == true) {
                              await provider.fileService.permanentlyDeleteBinEntry(entry);
                              await provider.refreshAll();
                            }
                          },
                        ),
                      ],
                    ),
                  ),
                );
              },
            ),
    );
  }
}
