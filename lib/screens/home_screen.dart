import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import '../l10n/app_localizations.dart';
import '../providers/app_provider.dart';
import '../scanner/scanner_screen.dart';
import '../widgets/pdf_list_tile.dart';
import 'converter_screen.dart';

class HomeScreen extends StatelessWidget {
  const HomeScreen({super.key});

  @override
  Widget build(BuildContext context) {
    final l10n = AppLocalizations.of(context);
    final provider = context.watch<AppProvider>();
    final recents = provider.recentDocuments;
    final allDocs = provider.filteredDocuments;

    return RefreshIndicator(
      color: const Color(0xFFDC143C),
      onRefresh: provider.refreshAll,
      child: ListView(
        padding: const EdgeInsets.only(bottom: 24),
        children: [
          Container(
            margin: const EdgeInsets.all(14),
            padding: const EdgeInsets.all(18),
            decoration: BoxDecoration(
              gradient: const LinearGradient(
                colors: [Color(0xFF28040B), Color(0xFF0E0E0E)],
                begin: Alignment.topLeft,
                end: Alignment.bottomRight,
              ),
              borderRadius: BorderRadius.circular(18),
              border: Border.all(color: const Color(0xFFDC143C).withValues(alpha: 0.55)),
            ),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Row(
                  children: [
                    const Icon(Icons.verified_user, color: Color(0xFFDC143C), size: 20),
                    const SizedBox(width: 8),
                    Text(
                      'OFFLINE  •  100% AD-FREE',
                      style: TextStyle(
                        color: Colors.white.withValues(alpha: 0.75),
                        fontSize: 11,
                        fontWeight: FontWeight.w700,
                        letterSpacing: 1.1,
                      ),
                    ),
                  ],
                ),
                const SizedBox(height: 10),
                Text(
                  l10n.scanDocument,
                  style: const TextStyle(fontSize: 22, fontWeight: FontWeight.bold),
                ),
                const SizedBox(height: 4),
                Text(
                  l10n.scanSubtitle,
                  style: const TextStyle(color: Colors.white70, fontSize: 13),
                ),
                const SizedBox(height: 14),
                Row(
                  children: [
                    Expanded(
                      child: FilledButton.icon(
                        icon: const Icon(Icons.document_scanner),
                        label: Text(l10n.scanDocument),
                        onPressed: () => Navigator.push(
                          context,
                          MaterialPageRoute(builder: (_) => const ScannerScreen()),
                        ),
                      ),
                    ),
                    const SizedBox(width: 10),
                    OutlinedButton.icon(
                      icon: const Icon(Icons.image),
                      label: Text(l10n.imagesToPdf),
                      onPressed: () => Navigator.push(
                        context,
                        MaterialPageRoute(
                          builder: (_) => const ConverterScreen(
                            initialMode: ConverterMode.imagesToPdf,
                          ),
                        ),
                      ),
                    ),
                  ],
                ),
              ],
            ),
          ),
          if (recents.isNotEmpty) ...[
            Padding(
              padding: const EdgeInsets.fromLTRB(16, 6, 16, 6),
              child: Text(
                l10n.recentFiles,
                style: const TextStyle(fontSize: 16, fontWeight: FontWeight.bold),
              ),
            ),
            ...recents.take(4).map((doc) => PdfListTile(item: doc)),
          ],
          Padding(
            padding: const EdgeInsets.fromLTRB(16, 12, 16, 6),
            child: Row(
              mainAxisAlignment: MainAxisAlignment.spaceBetween,
              children: [
                Text(
                  '${l10n.allPdfs} (${allDocs.length})',
                  style: const TextStyle(fontSize: 16, fontWeight: FontWeight.bold),
                ),
                TextButton.icon(
                  icon: const Icon(Icons.folder_open, size: 18),
                  label: Text(l10n.addFolder),
                  onPressed: () async {
                    await provider.fileService.authorizeNewFolder();
                    await provider.refreshAll();
                  },
                ),
              ],
            ),
          ),
          if (provider.isLoading)
            const Padding(
              padding: EdgeInsets.all(24),
              child: Center(child: CircularProgressIndicator(color: Color(0xFFDC143C))),
            )
          else if (allDocs.isEmpty)
            Padding(
              padding: const EdgeInsets.all(28),
              child: Text(
                l10n.noDocuments,
                textAlign: TextAlign.center,
                style: const TextStyle(color: Colors.white60),
              ),
            )
          else
            ...allDocs.map((doc) => PdfListTile(item: doc)),
        ],
      ),
    );
  }
}
