import 'dart:io';
import 'package:flutter/material.dart';
import 'package:intl/intl.dart';
import 'package:provider/provider.dart';
import '../models/pdf_document_item.dart';
import '../pdf_reader/pdf_reader_screen.dart';
import '../providers/app_provider.dart';

class BookmarksScreen extends StatelessWidget {
  const BookmarksScreen({super.key});

  @override
  Widget build(BuildContext context) {
    final provider = context.watch<AppProvider>();
    final bookmarks = provider.bookmarks;

    if (bookmarks.isEmpty) {
      return const Center(
        child: Text(
          'No bookmarks yet.\nBookmark any PDF or page inside the reader.',
          textAlign: TextAlign.center,
          style: TextStyle(color: Colors.white60),
        ),
      );
    }

    return ListView.builder(
      padding: const EdgeInsets.symmetric(vertical: 8),
      itemCount: bookmarks.length,
      itemBuilder: (context, index) {
        final bm = bookmarks[index];
        return Card(
          color: const Color(0xFF0E0E0E),
          margin: const EdgeInsets.symmetric(horizontal: 14, vertical: 5),
          child: ListTile(
            leading: Icon(
              bm.isPageBookmark ? Icons.bookmark : Icons.folder_special,
              color: const Color(0xFFDC143C),
            ),
            title: Text(bm.fileName, maxLines: 1, overflow: TextOverflow.ellipsis),
            subtitle: Text(
              '${bm.isPageBookmark ? 'Page ${bm.pageNumber}' : 'Document Bookmark'}  •  ${DateFormat('dd MMM yyyy').format(bm.createdAt)}',
              style: const TextStyle(color: Colors.white60, fontSize: 12),
            ),
            trailing: IconButton(
              icon: const Icon(Icons.delete_outline),
              onPressed: () {
                if (bm.id != null) provider.removeBookmark(bm.id!);
              },
            ),
            onTap: () async {
              final item = await PdfDocumentItem.fromFile(File(bm.filePath));
              if (item == null) {
                if (context.mounted) {
                  ScaffoldMessenger.of(context).showSnackBar(
                    const SnackBar(content: Text('Bookmarked file no longer exists at path.')),
                  );
                }
                return;
              }
              if (!context.mounted) return;
              Navigator.push(
                context,
                MaterialPageRoute(
                  builder: (_) => PdfReaderScreen(
                    documentItem: item,
                    initialPage: bm.pageNumber ?? 1,
                  ),
                ),
              );
            },
          ),
        );
      },
    );
  }
}
