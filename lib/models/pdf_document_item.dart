import 'dart:io';
import 'package:path/path.dart' as p;

enum SortField { name, date, size }

class PdfDocumentItem {
  final String path;
  final String name;
  final int sizeBytes;
  final DateTime modifiedAt;

  const PdfDocumentItem({
    required this.path,
    required this.name,
    required this.sizeBytes,
    required this.modifiedAt,
  });

  static Future<PdfDocumentItem?> fromFile(File file) async {
    try {
      if (!await file.exists()) return null;
      final stat = await file.stat();
      return PdfDocumentItem(
        path: file.path,
        name: p.basename(file.path),
        sizeBytes: stat.size,
        modifiedAt: stat.modified,
      );
    } catch (_) {
      return null;
    }
  }

  String get formattedSize {
    if (sizeBytes < 1024) return '$sizeBytes B';
    if (sizeBytes < 1024 * 1024) {
      return '${(sizeBytes / 1024).toStringAsFixed(1)} KB';
    }
    return '${(sizeBytes / (1024 * 1024)).toStringAsFixed(2)} MB';
  }
}
