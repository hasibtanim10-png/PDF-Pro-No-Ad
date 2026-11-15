import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import '../converters/pdf_converter_service.dart';
import '../l10n/app_localizations.dart';
import '../providers/app_provider.dart';
import '../scanner/scanner_screen.dart';
import 'bin_screen.dart';
import 'converter_screen.dart';
import 'vault_screen.dart';

class ToolsScreen extends StatelessWidget {
  const ToolsScreen({super.key});

  @override
  Widget build(BuildContext context) {
    final l10n = AppLocalizations.of(context);
    final provider = context.watch<AppProvider>();

    final items = [
      _ToolCardData(
        title: l10n.scanDocument,
        subtitle: 'Auto edge detection, 4-corner crop & filters',
        icon: Icons.document_scanner_rounded,
        onTap: () => Navigator.push(
          context,
          MaterialPageRoute(builder: (_) => const ScannerScreen()),
        ),
      ),
      _ToolCardData(
        title: l10n.convertToJpg,
        subtitle: 'Export selected or all PDF pages as JPG',
        icon: Icons.image_outlined,
        onTap: () => Navigator.push(
          context,
          MaterialPageRoute(
            builder: (_) => const ConverterScreen(
              initialMode: ConverterMode.pdfToImage,
              initialFormat: OutputImageFormat.jpg,
            ),
          ),
        ),
      ),
      _ToolCardData(
        title: l10n.convertToPng,
        subtitle: 'Lossless PNG rendering of PDF pages',
        icon: Icons.broken_image_outlined,
        onTap: () => Navigator.push(
          context,
          MaterialPageRoute(
            builder: (_) => const ConverterScreen(
              initialMode: ConverterMode.pdfToImage,
              initialFormat: OutputImageFormat.png,
            ),
          ),
        ),
      ),
      _ToolCardData(
        title: l10n.imagesToPdf,
        subtitle: 'Combine multiple gallery images into one PDF',
        icon: Icons.picture_as_pdf_outlined,
        onTap: () => Navigator.push(
          context,
          MaterialPageRoute(
            builder: (_) => const ConverterScreen(initialMode: ConverterMode.imagesToPdf),
          ),
        ),
      ),
      _ToolCardData(
        title: '${l10n.lockedVault} (${provider.lockedEntries.length})',
        subtitle: 'Hidden protected PDF documents',
        icon: Icons.lock_outline,
        onTap: () => Navigator.push(
          context,
          MaterialPageRoute(builder: (_) => const VaultScreen()),
        ),
      ),
      _ToolCardData(
        title: '${l10n.recycleBin} (${provider.binEntries.length})',
        subtitle: 'Restore or permanently erase deleted PDFs',
        icon: Icons.delete_sweep_outlined,
        onTap: () => Navigator.push(
          context,
          MaterialPageRoute(builder: (_) => const BinScreen()),
        ),
      ),
    ];

    return GridView.builder(
      padding: const EdgeInsets.all(14),
      gridDelegate: const SliverGridDelegateWithFixedCrossAxisCount(
        crossAxisCount: 2,
        crossAxisSpacing: 12,
        mainAxisSpacing: 12,
        childAspectRatio: 1.05,
      ),
      itemCount: items.length,
      itemBuilder: (_, index) {
        final t = items[index];
        return InkWell(
          borderRadius: BorderRadius.circular(16),
          onTap: t.onTap,
          child: Container(
            padding: const EdgeInsets.all(14),
            decoration: BoxDecoration(
              color: const Color(0xFF0F0F0F),
              borderRadius: BorderRadius.circular(16),
              border: Border.all(color: Colors.white12),
            ),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Container(
                  padding: const EdgeInsets.all(10),
                  decoration: BoxDecoration(
                    color: const Color(0xFFDC143C).withValues(alpha: 0.16),
                    borderRadius: BorderRadius.circular(12),
                  ),
                  child: Icon(t.icon, color: const Color(0xFFDC143C), size: 26),
                ),
                const Spacer(),
                Text(
                  t.title,
                  style: const TextStyle(fontWeight: FontWeight.bold, fontSize: 15),
                ),
                const SizedBox(height: 4),
                Text(
                  t.subtitle,
                  maxLines: 2,
                  overflow: TextOverflow.ellipsis,
                  style: const TextStyle(color: Colors.white60, fontSize: 11.5),
                ),
              ],
            ),
          ),
        );
      },
    );
  }
}

class _ToolCardData {
  final String title;
  final String subtitle;
  final IconData icon;
  final VoidCallback onTap;

  const _ToolCardData({
    required this.title,
    required this.subtitle,
    required this.icon,
    required this.onTap,
  });
}
