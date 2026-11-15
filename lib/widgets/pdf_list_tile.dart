import 'package:flutter/material.dart';
import 'package:intl/intl.dart';
import 'package:provider/provider.dart';
import 'package:share_plus/share_plus.dart';
import '../converters/pdf_converter_service.dart';
import '../l10n/app_localizations.dart';
import '../models/bookmark_item.dart';
import '../models/pdf_document_item.dart';
import '../pdf_reader/pdf_reader_screen.dart';
import '../providers/app_provider.dart';
import '../screens/converter_screen.dart';

class PdfListTile extends StatelessWidget {
  final PdfDocumentItem item;

  const PdfListTile({super.key, required this.item});

  @override
  Widget build(BuildContext context) {
    final l10n = AppLocalizations.of(context);
    final dateStr = DateFormat('dd MMM yyyy, HH:mm').format(item.modifiedAt);

    return Card(
      color: const Color(0xFF0E0E0E),
      margin: const EdgeInsets.symmetric(horizontal: 14, vertical: 5),
      shape: RoundedRectangleBorder(
        borderRadius: BorderRadius.circular(14),
        side: BorderSide(color: Colors.white.withValues(alpha: 0.08)),
      ),
      child: ListTile(
        contentPadding: const EdgeInsets.symmetric(horizontal: 14, vertical: 6),
        leading: Container(
          width: 46,
          height: 52,
          decoration: BoxDecoration(
            color: const Color(0xFFDC143C).withValues(alpha: 0.16),
            borderRadius: BorderRadius.circular(10),
            border: Border.all(color: const Color(0xFFDC143C), width: 1.1),
          ),
          child: const Column(
            mainAxisAlignment: MainAxisAlignment.center,
            children: [
              Icon(Icons.picture_as_pdf_rounded, color: Color(0xFFDC143C), size: 22),
              Text(
                'PDF',
                style: TextStyle(
                  color: Color(0xFFDC143C),
                  fontSize: 9,
                  fontWeight: FontWeight.w800,
                      ),
              ),
            ],
          ),
        ),
        title: Text(
          item.name,
          maxLines: 1,
          overflow: TextOverflow.ellipsis,
          style: const TextStyle(fontWeight: FontWeight.w600, fontSize: 15),
        ),
        subtitle: Padding(
          padding: const EdgeInsets.only(top: 4),
          child: Text(
            '${item.formattedSize}  •  $dateStr',
            style: const TextStyle(color: Colors.white60, fontSize: 12),
          ),
        ),
        trailing: PopupMenuButton<String>(
          icon: const Icon(Icons.more_vert_rounded),
          color: const Color(0xFF161616),
          onSelected: (action) => _handleAction(context, action, l10n),
          itemBuilder: (_) => [
            PopupMenuItem(value: 'share', child: Text(l10n.share)),
            PopupMenuItem(value: 'bookmark', child: Text(l10n.bookmark)),
            PopupMenuItem(value: 'rename', child: Text(l10n.rename)),
            PopupMenuItem(value: 'jpg', child: Text(l10n.convertToJpg)),
            PopupMenuItem(value: 'png', child: Text(l10n.convertToPng)),
            PopupMenuItem(value: 'lock', child: Text(l10n.fileLock)),
            PopupMenuItem(value: 'info', child: Text(l10n.fileInfo)),
            PopupMenuItem(
              value: 'bin',
              child: Text(l10n.moveToBin, style: const TextStyle(color: Color(0xFFDC143C))),
            ),
          ],
        ),
        onTap: () => _openReader(context),
      ),
    );
  }

  Future<void> _openReader(BuildContext context) async {
    final provider = context.read<AppProvider>();
    await provider.recordOpened(item.path);
    if (!context.mounted) return;
    await Navigator.push(
      context,
      MaterialPageRoute(
        builder: (_) => PdfReaderScreen(documentItem: item),
      ),
    );
    if (context.mounted) {
      await provider.refreshAll();
    }
  }

  Future<void> _handleAction(
    BuildContext context,
    String action,
    AppLocalizations l10n,
  ) async {
    final provider = context.read<AppProvider>();

    switch (action) {
      case 'share':
        await Share.shareXFiles([XFile(item.path)], text: item.name);

      case 'bookmark':
        await provider.addBookmark(
          BookmarkItem(
            filePath: item.path,
            fileName: item.name,
            createdAt: DateTime.now(),
          ),
        );
        if (context.mounted) {
          ScaffoldMessenger.of(context).showSnackBar(
            SnackBar(content: Text('Bookmarked ${item.name}')),
          );
        }

      case 'rename':
        final ctrl = TextEditingController(
          text: item.name.replaceAll(RegExp(r'\.pdf$', caseSensitive: false), ''),
        );
        final newName = await showDialog<String>(
          context: context,
          builder: (ctx) => AlertDialog(
            backgroundColor: const Color(0xFF141414),
            title: Text(l10n.rename),
            content: TextField(controller: ctrl, autofocus: true),
            actions: [
              TextButton(onPressed: () => Navigator.pop(ctx), child: Text(l10n.cancel)),
              FilledButton(
                onPressed: () => Navigator.pop(ctx, ctrl.text),
                child: Text(l10n.save),
              ),
            ],
          ),
        );
        if (newName != null && newName.trim().isNotEmpty) {
          await provider.fileService.renamePdf(item.path, newName);
          await provider.refreshAll();
        }

      case 'jpg':
        if (!context.mounted) return;
        Navigator.push(
          context,
          MaterialPageRoute(
            builder: (_) => ConverterScreen(
              initialMode: ConverterMode.pdfToImage,
              preselectedPdfPath: item.path,
              initialFormat: OutputImageFormat.jpg,
            ),
          ),
        );

      case 'png':
        if (!context.mounted) return;
        Navigator.push(
          context,
          MaterialPageRoute(
            builder: (_) => ConverterScreen(
              initialMode: ConverterMode.pdfToImage,
              preselectedPdfPath: item.path,
              initialFormat: OutputImageFormat.png,
            ),
          ),
        );

      case 'lock':
        await provider.securityService.lockPdfDocument(item, provider.fileService);
        await provider.refreshAll();
        if (context.mounted) {
          ScaffoldMessenger.of(context).showSnackBar(
            SnackBar(content: Text('Moved ${item.name} to Locked Vault')),
          );
        }

      case 'info':
        if (!context.mounted) return;
        showDialog(
          context: context,
          builder: (ctx) => AlertDialog(
            backgroundColor: const Color(0xFF141414),
            title: Text(l10n.fileInfo),
            content: SelectableText(
              'Name: ${item.name}\n'
              'Size: ${item.formattedSize} (${item.sizeBytes} bytes)\n'
              'Modified: ${DateFormat('yyyy-MM-dd HH:mm:ss').format(item.modifiedAt)}\n'
              'Path: ${item.path}',
            ),
            actions: [
              TextButton(onPressed: () => Navigator.pop(ctx), child: const Text('OK')),
            ],
          ),
        );

      case 'bin':
        final confirmed = await showDialog<bool>(
          context: context,
          builder: (ctx) => AlertDialog(
            backgroundColor: const Color(0xFF141414),
            title: Text(l10n.moveToBin),
            content: Text('Move "${item.name}" to Recycle Bin?'),
            actions: [
              TextButton(
                onPressed: () => Navigator.pop(ctx, false),
                child: Text(l10n.cancel),
              ),
              FilledButton(
                onPressed: () => Navigator.pop(ctx, true),
                child: Text(l10n.confirm),
              ),
            ],
          ),
        );
        if (confirmed == true) {
          await provider.fileService.moveToBin(item);
          await provider.refreshAll();
        }
    }
  }
}
