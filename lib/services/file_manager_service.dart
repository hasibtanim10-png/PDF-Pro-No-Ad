import 'dart:io';
import 'package:file_picker/file_picker.dart';
import 'package:path/path.dart' as p;
import 'package:path_provider/path_provider.dart';
import 'package:permission_handler/permission_handler.dart';
import 'package:shared_preferences/shared_preferences.dart';
import '../database/app_database.dart';
import '../models/managed_entry.dart';
import '../models/pdf_document_item.dart';

class StorageStats {
  final int managedPdfBytes;
  final int managedPdfCount;
  final int binBytes;
  final int vaultBytes
    final int vaultBytes;

  const StorageStats({
    required this.managedPdfBytes,
    required this.managedPdfCount,
    required this.binBytes,
    required this.vaultBytes,
  });
}

class FileManagerService {
  static const _prefsFoldersKey = 'authorized_folders_v1';

  Future<Directory> getAppPdfDirectory() async {
    final base = await getApplicationDocumentsDirectory();
    final dir = Directory(p.join(base.path, 'PDFProDocuments'));
    if (!await dir.exists()) await dir.create(recursive: true);
    return dir;
  }

  Future<Directory> getBinDirectory() async {
    final base = await getApplicationSupportDirectory();
    final dir = Directory(p.join(base.path, '.recycle_bin'));
    if (!await dir.exists()) await dir.create(recursive: true);
    return dir;
  }

  Future<Directory> getVaultDirectory() async {
    final base = await getApplicationSupportDirectory();
    final dir = Directory(p.join(base.path, '.locked_vault'));
    if (!await dir.exists()) await dir.create(recursive: true);
    return dir;
  }

  Future<List<String>> getAuthorizedFolders() async {
    final prefs = await SharedPreferences.getInstance();
    final saved = prefs.getStringList(_prefsFoldersKey) ?? [];
    final appDir = await getAppPdfDirectory();
    final all = <String>{appDir.path, ...saved};

    for (final candidate in [
      '/storage/emulated/0/Download',
      '/storage/emulated/0/Documents',
    ]) {
      final d = Directory(candidate);
      if (await d.exists()) {
        all.add(candidate);
      }
    }
    return all.toList();
  }

  Future<String?> authorizeNewFolder() async {
    final selected = await FilePicker.getDirectoryPath(
      dialogTitle: 'Select PDF Folder',
    );
    if (selected == null || selected.isEmpty) return null;
    final prefs = await SharedPreferences.getInstance();
    final existing = prefs.getStringList(_prefsFoldersKey) ?? [];
    if (!existing.contains(selected)) {
      existing.add(selected);
      await prefs.setStringList(_prefsFoldersKey, existing);
    }
    return selected;
  }

  Future<void> importExternalPdfs() async {
    final result = await FilePicker.pickFiles(
      type: FileType.custom,
      allowedExtensions: ['pdf'],
      allowMultiple: true,
    );
    if (result == null) return;
    final targetDir = await getAppPdfDirectory();
    for (final f in result.files) {
      if (f.path == null) continue;
      final src = File(f.path!);
      if (!await src.exists()) continue;
      final destPath = await _uniqueDestination(targetDir.path, p.basename(src.path));
      await src.copy(destPath);
    }
  }

  Future<List<PdfDocumentItem>> scanAccessiblePdfs() async {
    await Permission.storage.request();
    final folders = await getAuthorizedFolders();
    final lockedEntries = await AppDatabase.instance.getLockedEntries();
    final lockedPaths = lockedEntries.map((e) => e.storedPath).toSet();

    final discovered = <String, PdfDocumentItem>{};

    for (final folderPath in folders) {
      final dir = Directory(folderPath);
      if (!await dir.exists()) continue;
      try {
        await for (final entity in dir.list(recursive: false, followLinks: false)) {
          if (entity is File &&
              entity.path.toLowerCase().endsWith('.pdf') &&
              !lockedPaths.contains(entity.path)) {
            final item = await PdfDocumentItem.fromFile(entity);
            if (item != null) {
              discovered[item.path] = item;
            }
          }
        }
      } catch (_) {}
    }
    return discovered.values.toList();
  }

  Future<String?> renamePdf(String oldPath, String newBaseName) async {
    final file = File(oldPath);
    if (!await file.exists()) return null;
    final cleanName = newBaseName.trim().endsWith('.pdf')
        ? newBaseName.trim()
        : '${newBaseName.trim()}.pdf';
    final newPath = p.join(p.dirname(oldPath), cleanName);
    if (newPath == oldPath) return oldPath;
    if (await File(newPath).exists()) {
      throw Exception('A file with that name already exists.');
    }
    final renamed = await file.rename(newPath);
    await AppDatabase.instance.updateBookmarkPath(oldPath, renamed.path, cleanName);
    return renamed.path;
  }

  Future<void> moveToBin(PdfDocumentItem item) async {
    final src = File(item.path);
    if (!await src.exists()) return;
    final binDir = await getBinDirectory();
    final binPath = await _uniqueDestination(
      binDir.path,
      '${DateTime.now().millisecondsSinceEpoch}_${item.name}',
    );
    await _moveFileSafe(src, binPath);
    await AppDatabase.instance.insertBinEntry(
      ManagedEntry(
        originalPath: item.path,
        storedPath: binPath,
        fileName: item.name,
        sizeBytes: item.sizeBytes,
        movedAt: DateTime.now(),
      ),
    );
  }

  Future<void> restoreFromBin(ManagedEntry entry) async {
    final stored = File(entry.storedPath);
    if (await stored.exists()) {
      final parent = Directory(p.dirname(entry.originalPath));
      final targetDir = await parent.exists() ? parent : await getAppPdfDirectory();
      final dest = await _uniqueDestination(targetDir.path, entry.fileName);
      await _moveFileSafe(stored, dest);
    }
    if (entry.id != null) {
      await AppDatabase.instance.deleteBinEntry(entry.id!);
    }
  }

  Future<void> permanentlyDeleteBinEntry(ManagedEntry entry) async {
    final stored = File(entry.storedPath);
    if (await stored.exists()) {
      await stored.delete();
    }
    await AppDatabase.instance.removeBookmarksForPath(entry.originalPath);
    if (entry.id != null) {
      await AppDatabase.instance.deleteBinEntry(entry.id!);
    }
  }

  Future<void> permanentlyDeleteFile(String filePath) async {
    final f = File(filePath);
    if (await f.exists()) {
      await f.delete();
    }
    await AppDatabase.instance.removeBookmarksForPath(filePath);
  }

  Future<StorageStats> computeStorageStats(List<PdfDocumentItem> docs) async {
    final totalDocsBytes = docs.fold<int>(0, (sum, d) => sum + d.sizeBytes);
    final binEntries = await AppDatabase.instance.getBinEntries();
    final vaultEntries = await AppDatabase.instance.getLockedEntries();
    final binBytes = binEntries.fold<int>(0, (sum, e) => sum + e.sizeBytes);
    final vaultBytes = vaultEntries.fold<int>(0, (sum, e) => sum + e.sizeBytes);

    return StorageStats(
      managedPdfBytes: totalDocsBytes,
      managedPdfCount: docs.length,
      binBytes: binBytes,
      vaultBytes: vaultBytes,
    );
  }

  Future<void> _moveFileSafe(File src, String destPath) async {
    try {
      await src.rename(destPath);
    } catch (_) {
      await src.copy(destPath);
      await src.delete();
    }
  }

  Future<String> _uniqueDestination(String dirPath, String fileName) async {
    var candidate = p.join(dirPath, fileName);
    var counter = 1;
    final ext = p.extension(fileName);
    final stem = p.basenameWithoutExtension(fileName);
    while (await File(candidate).exists()) {
      candidate = p.join(dirPath, '${stem}_$counter$ext');
      counter++;
    }
    return candidate;
  }
}
