#!/usr/bin/env python3
"""
PDF Pro No Ad (com.comeback.pdfprona) - Complete Project Generator
Generates all Dart source files, Android configs, pubspec.yaml, tests, and README.md.
"""

from pathlib import Path

FILES: dict[str, str] = {}

# ==============================================================================
# 1. PUBSPEC.YAML
# ==============================================================================
FILES["pubspec.yaml"] = r"""name: pdf_pro_no_ad
description: Premium offline-first, ad-free Android PDF Reader, Manager, Scanner & Converter.
publish_to: 'none'
version: 1.0.0+1

environment:
  sdk: '>=3.4.0 <4.0.0'

dependencies:
  flutter:
    sdk: flutter
  flutter_localizations:
    sdk: flutter
  pdfrx: ^1.0.101
  pdf: ^3.11.1
  image: ^4.3.0
  camera: ^0.11.0+2
  file_picker: ^10.1.2
  path_provider: ^2.1.5
  path: ^1.9.0
  sqflite: ^2.4.1
  shared_preferences: ^2.3.3
  local_auth: ^2.3.0
  crypto: ^3.0.6
  share_plus: ^10.1.2
  permission_handler: ^11.3.1
  intl: any
  provider: ^6.1.2

dev_dependencies:
  flutter_test:
    sdk: flutter
  flutter_lints: ^4.0.0

flutter:
  uses-material-design: true
"""

# ==============================================================================
# 2. ANDROID CONFIGURATION FILES
# ==============================================================================
FILES["android/app/build.gradle"] = r"""plugins {
    id "com.android.application"
    id "kotlin-android"
    id "dev.flutter.flutter-gradle-plugin"
}

android {
    namespace = "com.comeback.pdfprona"
    compileSdk = 36
    ndkVersion = flutter.ndkVersion

    compileOptions {
        sourceCompatibility = JavaVersion.VERSION_17
        targetCompatibility = JavaVersion.VERSION_17
    }

    kotlinOptions {
        jvmTarget = "17"
    }

    defaultConfig {
        applicationId = "com.comeback.pdfprona"
        minSdk = 24
        targetSdk = 35
        versionCode = 1
        versionName = "1.0.0"
        multiDexEnabled = true
    }

    buildTypes {
        release {
            signingConfig = signingConfigs.debug
            minifyEnabled = false
            shrinkResources = false
        }
    }
}

flutter {
    source = "../.."
}
"""

FILES["android/app/src/main/AndroidManifest.xml"] = r"""<manifest xmlns:android="http://schemas.android.com/apk/res/android" xmlns:tools="http://schemas.android.com/tools">
    <!-- Offline-first privacy: No INTERNET permission requested -->
    <uses-permission android:name="android.permission.CAMERA" />
    <uses-permission android:name="android.permission.FLASHLIGHT" />
    <uses-permission android:name="android.permission.USE_BIOMETRIC" />
    <uses-permission android:name="android.permission.READ_EXTERNAL_STORAGE" android:maxSdkVersion="32" />
    <uses-permission android:name="android.permission.WRITE_EXTERNAL_STORAGE" android:maxSdkVersion="29" tools:replace="android:maxSdkVersion" />

    <uses-feature android:name="android.hardware.camera" android:required="false" />
    <uses-feature android:name="android.hardware.camera.autofocus" android:required="false" />

    <application
        android:label="PDF Pro No Ad"
        android:name="${applicationName}"
        android:icon="@mipmap/ic_launcher"
        android:requestLegacyExternalStorage="true">

        <activity
            android:name=".MainActivity"
            android:exported="true"
            android:launchMode="singleTop"
            android:taskAffinity=""
            android:theme="@style/LaunchTheme"
            android:configChanges="orientation|keyboardHidden|keyboard|screenSize|smallestScreenSize|locale|layoutDirection|fontScale|screenLayout|density|uiMode"
            android:hardwareAccelerated="true"
            android:windowSoftInputMode="adjustResize">

            <meta-data
                android:name="io.flutter.embedding.android.NormalTheme"
                android:resource="@style/NormalTheme" />

            <intent-filter>
                <action android:name="android.intent.action.MAIN" />
                <category android:name="android.intent.category.LAUNCHER" />
            </intent-filter>

            <intent-filter>
                <action android:name="android.intent.action.VIEW" />
                <category android:name="android.intent.category.DEFAULT" />
                <category android:name="android.intent.category.BROWSABLE" />
                <data android:scheme="file" />
                <data android:scheme="content" />
                <data android:mimeType="application/pdf" />
            </intent-filter>
        </activity>

        <provider
            android:name="androidx.core.content.FileProvider"
            android:authorities="${applicationId}.fileprovider"
            android:exported="false"
            android:grantUriPermissions="true">
            <meta-data
                android:name="android.support.FILE_PROVIDER_PATHS"
                android:resource="@xml/file_paths" />
        </provider>

        <meta-data
            android:name="flutterEmbedding"
            android:value="2" />
    </application>
</manifest>
"""

FILES["android/app/src/main/kotlin/com/comeback/pdfprona/MainActivity.kt"] = r"""package com.comeback.pdfprona

import io.flutter.embedding.android.FlutterFragmentActivity

class MainActivity : FlutterFragmentActivity()
"""

FILES["android/app/src/main/res/xml/file_paths.xml"] = r"""<?xml version="1.0" encoding="utf-8"?>
<paths xmlns:android="http://schemas.android.com/apk/res/android">
    <cache-path name="cache" path="." />
    <files-path name="files" path="." />
    <external-path name="external" path="." />
    <external-files-path name="external_files" path="." />
</paths>
"""

# ==============================================================================
# 3. LOCALIZATION (ENGLISH & BANGLA)
# ==============================================================================
FILES["lib/l10n/app_localizations.dart"] = r"""import 'package:flutter/material.dart';

class AppLocalizations {
  final Locale locale;
  const AppLocalizations(this.locale);

  static AppLocalizations of(BuildContext context) {
    return Localizations.of<AppLocalizations>(context, AppLocalizations) ??
        const AppLocalizations(Locale('en'));
  }

  bool get isBangla => locale.languageCode == 'bn';

  String get appName => 'PDF Pro No Ad';
  String get home => isBangla ? 'হোম' : 'Home';
  String get documents => isBangla ? 'ডকুমেন্টস' : 'Documents';
  String get tools => isBangla ? 'টুলস' : 'Tools';
  String get me => isBangla ? 'আমি' : 'Me';
  String get bookmarks => isBangla ? 'বুকমার্ক' : 'Bookmarks';

  String get scanDocument => isBangla ? 'ডকুমেন্ট স্ক্যান করুন' : 'Scan Document';
  String get scanSubtitle => isBangla
      ? 'অটো এজ ডিটেকশন ও পার্সপেক্টিভ কারেকশন'
      : 'Auto edge detection & perspective warp';
  String get recentFiles => isBangla ? 'সাম্প্রতিক পিডিএফ' : 'Recent PDFs';
  String get allPdfs => isBangla ? 'সকল পিডিএফ ফাইল' : 'All PDF Files';
  String get searchHint => isBangla ? 'ফাইলের নাম খুঁজুন...' : 'Search PDFs by filename...';
  String get addFolder => isBangla ? 'ফোল্ডার যোগ করুন' : 'Add Folder';
  String get openPdf => isBangla ? 'পিডিএফ খুলুন' : 'Open PDF';
  String get noDocuments => isBangla
      ? 'কোনো পিডিএফ পাওয়া যায়নি। নিচের বাটন থেকে ফোল্ডার বা ফাইল নির্বাচন করুন।'
      : 'No PDFs discovered yet. Tap Add Folder or Scan to begin.';

  String get sortBy => isBangla ? 'সাজান' : 'Sort by';
  String get sortName => isBangla ? 'নাম' : 'Name';
  String get sortDate => isBangla ? 'তারিখ' : 'Date';
  String get sortSize => isBangla ? 'আকার' : 'Size';

  String get share => isBangla ? 'শেয়ার' : 'Share';
  String get bookmark => isBangla ? 'বুকমার্ক' : 'Bookmark';
  String get rename => isBangla ? 'নাম পরিবর্তন' : 'Rename';
  String get delete => isBangla ? 'মুছে ফেলুন' : 'Delete';
  String get moveToBin => isBangla ? 'বিনে পাঠান' : 'Move to Bin';
  String get convertToJpg => isBangla ? 'JPG-তে রূপান্তর' : 'Convert to JPG';
  String get convertToPng => isBangla ? 'PNG-তে রূপান্তর' : 'Convert to PNG';
  String get imagesToPdf => isBangla ? 'ছবি থেকে PDF' : 'Images to PDF';
  String get fileLock => isBangla ? 'ফাইল লক' : 'File Lock';
  String get fileInfo => isBangla ? 'ফাইলের তথ্য' : 'File Info';

  String get recycleBin => isBangla ? 'রিসাইকেল বিন' : 'Recycle Bin';
  String get lockedVault => isBangla ? 'লক করা ফাইল' : 'Locked Vault';
  String get appLock => isBangla ? 'অ্যাপ লক (PIN ও বায়োমেট্রিক)' : 'App Lock (PIN & Biometric)';
  String get language => isBangla ? 'ভাষা (English / বাংলা)' : 'Language (English / বাংলা)';
  String get theme => isBangla ? 'থিম সেটিংস' : 'Theme Settings';
  String get storageInfo => isBangla ? 'স্টোরেজ তথ্য' : 'Storage Information';
  String get scannerPrefs => isBangla ? 'স্ক্যানার পছন্দসমূহ' : 'Scanner Preferences';
  String get privacySecurity => isBangla ? 'গোপনীয়তা ও নিরাপত্তা' : 'Privacy & Security';
  String get about => isBangla ? 'অ্যাপ সম্পর্কে' : 'About';
  String get contact => isBangla ? 'যোগাযোগ' : 'Contact';

  String get cancel => isBangla ? 'বাতিল' : 'Cancel';
  String get confirm => isBangla ? 'নিশ্চিত করুন' : 'Confirm';
  String get save => isBangla ? 'সংরক্ষণ' : 'Save';
  String get restore => isBangla ? 'পুনরুদ্ধার' : 'Restore';
  String get deleteForever => isBangla ? 'স্থায়ীভাবে মুছুন' : 'Delete Forever';
}

class AppLocalizationsDelegate extends LocalizationsDelegate<AppLocalizations> {
  const AppLocalizationsDelegate();

  @override
  bool isSupported(Locale locale) => ['en', 'bn'].contains(locale.languageCode);

  @override
  Future<AppLocalizations> load(Locale locale) async => AppLocalizations(locale);

  @override
  bool shouldReload(covariant LocalizationsDelegate<AppLocalizations> old) => false;
}
"""

# ==============================================================================
# 4. DATA MODELS
# ==============================================================================
FILES["lib/models/pdf_document_item.dart"] = r"""import 'dart:io';
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
"""

FILES["lib/models/bookmark_item.dart"] = r"""class BookmarkItem {
  final int? id;
  final String filePath;
  final String fileName;
  final int? pageNumber;
  final String? label;
  final DateTime createdAt;

  const BookmarkItem({
    this.id,
    required this.filePath,
    required this.fileName,
    this.pageNumber,
    this.label,
    required this.createdAt,
  });

  bool get isPageBookmark => pageNumber != null;

  Map<String, dynamic> toMap() => {
        'id': id,
        'file_path': filePath,
        'file_name': fileName,
        'page_number': pageNumber,
        'label': label,
        'created_at': createdAt.toIso8601String(),
      };

  factory BookmarkItem.fromMap(Map<String, dynamic> map) => BookmarkItem(
        id: map['id'] as int?,
        filePath: map['file_path'] as String,
        fileName: map['file_name'] as String,
        pageNumber: map['page_number'] as int?,
        label: map['label'] as String?,
        createdAt: DateTime.tryParse(map['created_at'] as String? ?? '') ??
            DateTime.now(),
      );
}
"""

FILES["lib/models/managed_entry.dart"] = r"""class ManagedEntry {
  final int? id;
  final String originalPath;
  final String storedPath;
  final String fileName;
  final int sizeBytes;
  final DateTime movedAt;

  const ManagedEntry({
    this.id,
    required this.originalPath,
    required this.storedPath,
    required this.fileName,
    required this.sizeBytes,
    required this.movedAt,
  });

  Map<String, dynamic> toMap() => {
        'id': id,
        'original_path': originalPath,
        'stored_path': storedPath,
        'file_name': fileName,
        'size_bytes': sizeBytes,
        'moved_at': movedAt.toIso8601String(),
      };

  factory ManagedEntry.fromMap(Map<String, dynamic> map) => ManagedEntry(
        id: map['id'] as int?,
        originalPath: map['original_path'] as String,
        storedPath: map['stored_path'] as String,
        fileName: map['file_name'] as String,
        sizeBytes: map['size_bytes'] as int? ?? 0,
        movedAt: DateTime.tryParse(map['moved_at'] as String? ?? '') ??
            DateTime.now(),
      );
}
"""

FILES["lib/models/scanned_page.dart"] = r"""import 'dart:math';

enum ScanFilterType {
  original,
  blackAndWhite,
  grayscale,
  magicColor,
  enhancedDocument,
  custom,
}

class NormalizedQuad {
  final List<Point<double>> corners;

  const NormalizedQuad(this.corners);

  factory NormalizedQuad.defaultInset() => const NormalizedQuad([
        Point(0.08, 0.08),
        Point(0.92, 0.08),
        Point(0.92, 0.92),
        Point(0.08, 0.92),
      ]);

  NormalizedQuad copyWithCorner(int index, Point<double> pt) {
    final updated = List<Point<double>>.from(corners);
    updated[index] = Point(
      pt.x.clamp(0.0, 1.0),
      pt.y.clamp(0.0, 1.0),
    );
    return NormalizedQuad(updated);
  }
}

class ScannedPage {
  final String id;
  final String rawImagePath;
  String processedImagePath;
  NormalizedQuad quad;
  ScanFilterType filter;
  double brightness;
  double contrast;
  int rotationQuarterTurns;

  ScannedPage({
    required this.id,
    required this.rawImagePath,
    required this.processedImagePath,
    required this.quad,
    this.filter = ScanFilterType.enhancedDocument,
    this.brightness = 0.0,
    this.contrast = 1.15,
    this.rotationQuarterTurns = 0,
  });
}
"""

# ==============================================================================
# 5. SQLITE PERSISTENCE DATABASE
# ==============================================================================
FILES["lib/database/app_database.dart"] = r"""import 'package:path/path.dart' as p;
import 'package:sqflite/sqflite.dart';
import '../models/bookmark_item.dart';
import '../models/managed_entry.dart';

class AppDatabase {
  AppDatabase._();
  static final AppDatabase instance = AppDatabase._();

  Database? _db;

  Future<Database> get database async {
    if (_db != null) return _db!;
    final dbDir = await getDatabasesPath();
    final dbPath = p.join(dbDir, 'pdf_pro_no_ad.db');
    _db = await openDatabase(
      dbPath,
      version: 1,
      onCreate: (db, version) async {
        await db.execute('''
          CREATE TABLE bookmarks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            file_path TEXT NOT NULL,
            file_name TEXT NOT NULL,
            page_number INTEGER,
            label TEXT,
            created_at TEXT NOT NULL
          )
        ''');
        await db.execute('''
          CREATE TABLE recycle_bin (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            original_path TEXT NOT NULL,
            stored_path TEXT NOT NULL,
            file_name TEXT NOT NULL,
            size_bytes INTEGER NOT NULL,
            moved_at TEXT NOT NULL
          )
        ''');
        await db.execute('''
          CREATE TABLE locked_files (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            original_path TEXT NOT NULL,
            stored_path TEXT NOT NULL,
            file_name TEXT NOT NULL,
            size_bytes INTEGER NOT NULL,
            moved_at TEXT NOT NULL
          )
        ''');
        await db.execute('''
          CREATE TABLE recent_files (
            file_path TEXT PRIMARY KEY,
            opened_at TEXT NOT NULL
          )
        ''');
      },
    );
    return _db!;
  }

  Future<List<BookmarkItem>> getBookmarks() async {
    final db = await database;
    final rows = await db.query('bookmarks', orderBy: 'created_at DESC');
    return rows.map(BookmarkItem.fromMap).toList();
  }

  Future<void> addBookmark(BookmarkItem item) async {
    final db = await database;
    final existing = await db.query(
      'bookmarks',
      where: item.pageNumber == null
          ? 'file_path = ? AND page_number IS NULL'
          : 'file_path = ? AND page_number = ?',
      whereArgs: item.pageNumber == null
          ? [item.filePath]
          : [item.filePath, item.pageNumber],
    );
    if (existing.isEmpty) {
      await db.insert('bookmarks', item.toMap());
    }
  }

  Future<void> removeBookmark(int id) async {
    final db = await database;
    await db.delete('bookmarks', where: 'id = ?', whereArgs: [id]);
  }

  Future<void> removeBookmarksForPath(String filePath) async {
    final db = await database;
    await db.delete('bookmarks', where: 'file_path = ?', whereArgs: [filePath]);
  }

  Future<void> updateBookmarkPath(String oldPath, String newPath, String newName) async {
    final db = await database;
    await db.update(
      'bookmarks',
      {'file_path': newPath, 'file_name': newName},
      where: 'file_path = ?',
      whereArgs: [oldPath],
    );
  }

  Future<List<ManagedEntry>> getBinEntries() async {
    final db = await database;
    final rows = await db.query('recycle_bin', orderBy: 'moved_at DESC');
    return rows.map(ManagedEntry.fromMap).toList();
  }

  Future<void> insertBinEntry(ManagedEntry entry) async {
    final db = await database;
    await db.insert('recycle_bin', entry.toMap());
  }

  Future<void> deleteBinEntry(int id) async {
    final db = await database;
    await db.delete('recycle_bin', where: 'id = ?', whereArgs: [id]);
  }

  Future<List<ManagedEntry>> getLockedEntries() async {
    final db = await database;
    final rows = await db.query('locked_files', orderBy: 'moved_at DESC');
    return rows.map(ManagedEntry.fromMap).toList();
  }

  Future<void> insertLockedEntry(ManagedEntry entry) async {
    final db = await database;
    await db.insert('locked_files', entry.toMap());
  }

  Future<void> deleteLockedEntry(int id) async {
    final db = await database;
    await db.delete('locked_files', where: 'id = ?', whereArgs: [id]);
  }

  Future<void> recordRecentFile(String filePath) async {
    final db = await database;
    await db.insert(
      'recent_files',
      {'file_path': filePath, 'opened_at': DateTime.now().toIso8601String()},
      conflictAlgorithm: ConflictAlgorithm.replace,
    );
  }

  Future<List<String>> getRecentPaths({int limit = 10}) async {
    final db = await database;
    final rows = await db.query(
      'recent_files',
      orderBy: 'opened_at DESC',
      limit: limit,
    );
    return rows.map((r) => r['file_path'] as String).toList();
  }
}
"""

# ==============================================================================
# 6. CORE SERVICES: FILE MANAGER, CONVERTER & SECURITY
# ==============================================================================
FILES["lib/services/file_manager_service.dart"] = r"""import 'dart:io';
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
"""

FILES["lib/converters/pdf_converter_service.dart"] = r"""import 'dart:io';
import 'dart:typed_data';
import 'dart:ui';
import 'package:image/image.dart' as img;
import 'package:path/path.dart' as p;
import 'package:path_provider/path_provider.dart';
import 'package:pdf/pdf.dart' hide PdfDocument;
import 'package:pdf/widgets.dart' as pw;
import 'package:pdfrx/pdfrx.dart';

enum OutputImageFormat { jpg, png }

enum ConversionQuality {
  standard(scale: 1.5, jpegQuality: 80, label: 'Standard (150 DPI)'),
  high(scale: 2.2, jpegQuality: 92, label: 'High (220 DPI)'),
  ultra(scale: 3.0, jpegQuality: 98, label: 'Ultra (300 DPI)');

  final double scale;
  final int jpegQuality;
  final String label;
  const ConversionQuality({
    required this.scale,
    required this.jpegQuality,
    required this.label,
  });
}

class PdfConverterService {
  Future<Directory> resolveOutputDirectory([String? customFolder]) async {
    if (customFolder != null && customFolder.isNotEmpty) {
      final d = Directory(customFolder);
      if (await d.exists()) return d;
    }
    final docs = await getApplicationDocumentsDirectory();
    final out = Directory(p.join(docs.path, 'PDFProConverted'));
    if (!await out.exists()) await out.create(recursive: true);
    return out;
  }

  Future<int> getPageCount(String pdfPath) async {
    final doc = await PdfDocument.openFile(pdfPath);
    try {
      return doc.pages.length;
    } finally {
      await doc.dispose();
    }
  }

  Future<List<String>> convertPdfToImages({
    required String pdfPath,
    required OutputImageFormat format,
    List<int>? pages,
    ConversionQuality quality = ConversionQuality.high,
    String? outputFolder,
    void Function(int current, int total)? onProgress,
  }) async {
    final outDir = await resolveOutputDirectory(outputFolder);
    final baseName = p.basenameWithoutExtension(pdfPath);
    final doc = await PdfDocument.openFile(pdfPath);
    final outputs = <String>[];

    try {
      final totalPages = doc.pages.length;
      final targetPages = (pages == null || pages.isEmpty)
          ? List<int>.generate(totalPages, (i) => i + 1)
          : pages.where((n) => n >= 1 && n <= totalPages).toList();

      for (var i = 0; i < targetPages.length; i++) {
        final pageNum = targetPages[i];
        onProgress?.call(i + 1, targetPages.length);

        final page = doc.pages[pageNum - 1];
        final renderWidth = (page.width * quality.scale).round().clamp(300, 4200);
        final renderHeight = (page.height * quality.scale).round().clamp(300, 5600);

        final pdfImage = await page.render(
          width: renderWidth,
          height: renderHeight,
          fullWidth: renderWidth.toDouble(),
          fullHeight: renderHeight.toDouble(),
          backgroundColor: const Color(0xFFFFFFFF),
        );
        if (pdfImage == null) continue;

        final decoded = img.Image.fromBytes(
          width: pdfImage.width,
          height: pdfImage.height,
          bytes: pdfImage.pixels.buffer,
          order: img.ChannelOrder.bgra,
        );
        pdfImage.dispose();

        final ext = format == OutputImageFormat.jpg ? 'jpg' : 'png';
        final outPath = p.join(
          outDir.path,
          '${baseName}_page_${pageNum}_${DateTime.now().millisecondsSinceEpoch}.$ext',
        );

        final Uint8List encoded = format == OutputImageFormat.jpg
            ? Uint8List.fromList(img.encodeJpg(decoded, quality: quality.jpegQuality))
            : Uint8List.fromList(img.encodePng(decoded));

        await File(outPath).writeAsBytes(encoded, flush: true);
        outputs.add(outPath);
      }
      return outputs;
    } finally {
      await doc.dispose();
    }
  }

  Future<String> convertImagesToPdf({
    required List<String> imagePaths,
    required String outputFileName,
    ConversionQuality quality = ConversionQuality.high,
    String? outputFolder,
    void Function(int current, int total)? onProgress,
  }) async {
    final outDir = await resolveOutputDirectory(outputFolder);
    final pdfDoc = pw.Document(
      title: outputFileName,
      creator: 'PDF Pro No Ad',
    );

    for (var i = 0; i < imagePaths.length; i++) {
      onProgress?.call(i + 1, imagePaths.length);
      final file = File(imagePaths[i]);
      if (!await file.exists()) continue;

      final bytes = await file.readAsBytes();
      final decoded = img.decodeImage(bytes);
      if (decoded == null) continue;

      final normalizedBytes = Uint8List.fromList(
        img.encodeJpg(decoded, quality: quality.jpegQuality),
      );
      final memImage = pw.MemoryImage(normalizedBytes);
      final isLandscape = decoded.width > decoded.height;

      pdfDoc.addPage(
        pw.Page(
          pageFormat: isLandscape ? PdfPageFormat.a4.landscape : PdfPageFormat.a4,
          margin: const pw.EdgeInsets.all(16),
          build: (_) => pw.Center(
            child: pw.Image(memImage, fit: pw.BoxFit.contain),
          ),
        ),
      );
    }

    final cleanName = outputFileName.trim().isEmpty
        ? 'Converted_${DateTime.now().millisecondsSinceEpoch}.pdf'
        : (outputFileName.trim().endsWith('.pdf')
            ? outputFileName.trim()
            : '${outputFileName.trim()}.pdf');

    final outPath = p.join(outDir.path, cleanName);
    final savedBytes = await pdfDoc.save();
    await File(outPath).writeAsBytes(savedBytes, flush: true);
    return outPath;
  }
}
"""

FILES["lib/security/security_service.dart"] = r"""import 'dart:convert';
import 'dart:io';
import 'dart:math';
import 'package:crypto/crypto.dart';
import 'package:local_auth/local_auth.dart';
import 'package:path/path.dart' as p;
import 'package:shared_preferences/shared_preferences.dart';
import '../database/app_database.dart';
import '../models/managed_entry.dart';
import '../models/pdf_document_item.dart';
import '../services/file_manager_service.dart';

class SecurityService {
  static const _pinHashKey = 'app_lock_pin_hash_v1';
  static const _pinSaltKey = 'app_lock_pin_salt_v1';
  static const _appLockEnabledKey = 'app_lock_enabled_v1';
  static const _biometricEnabledKey = 'app_lock_biometric_v1';

  final LocalAuthentication _localAuth = LocalAuthentication();

  Future<bool> isAppLockEnabled() async {
    final prefs = await SharedPreferences.getInstance();
    return prefs.getBool(_appLockEnabledKey) ?? false;
  }

  Future<bool> isBiometricEnabled() async {
    final prefs = await SharedPreferences.getInstance();
    return prefs.getBool(_biometricEnabledKey) ?? false;
  }

  Future<bool> isBiometricHardwareAvailable() async {
    try {
      final canCheck = await _localAuth.canCheckBiometrics;
      final isSupported = await _localAuth.isDeviceSupported();
      return canCheck && isSupported;
    } catch (_) {
      return false;
    }
  }

  Future<void> setAppPin(String pin) async {
    final prefs = await SharedPreferences.getInstance();
    final rng = Random.secure();
    final saltBytes = List<int>.generate(16, (_) => rng.nextInt(256));
    final salt = base64Encode(saltBytes);
    final hash = _hashPin(pin, salt);
    await prefs.setString(_pinSaltKey, salt);
    await prefs.setString(_pinHashKey, hash);
    await prefs.setBool(_appLockEnabledKey, true);
  }

  Future<bool> verifyPin(String pin) async {
    final prefs = await SharedPreferences.getInstance();
    final salt = prefs.getString(_pinSaltKey);
    final expectedHash = prefs.getString(_pinHashKey);
    if (salt == null || expectedHash == null) return false;
    return _hashPin(pin, salt) == expectedHash;
  }

  Future<void> disableAppLock() async {
    final prefs = await SharedPreferences.getInstance();
    await prefs.setBool(_appLockEnabledKey, false);
    await prefs.setBool(_biometricEnabledKey, false);
  }

  Future<void> setBiometricEnabled(bool enabled) async {
    final prefs = await SharedPreferences.getInstance();
    await prefs.setBool(_biometricEnabledKey, enabled);
  }

  Future<bool> authenticateBiometric() async {
    try {
      return await _localAuth.authenticate(
        localizedReason: 'Authenticate to unlock PDF Pro No Ad',
        options: const AuthenticationOptions(
          biometricOnly: false,
          stickyAuth: true,
        ),
      );
    } catch (_) {
      return false;
    }
  }

  Future<void> lockPdfDocument(
    PdfDocumentItem item,
    FileManagerService fileService,
  ) async {
    final src = File(item.path);
    if (!await src.exists()) return;
    final vaultDir = await fileService.getVaultDirectory();
    final vaultPath = p.join(
      vaultDir.path,
      '${DateTime.now().millisecondsSinceEpoch}_${item.name}.locked',
    );
    try {
      await src.rename(vaultPath);
    } catch (_) {
      await src.copy(vaultPath);
      await src.delete();
    }
    await AppDatabase.instance.insertLockedEntry(
      ManagedEntry(
        originalPath: item.path,
        storedPath: vaultPath,
        fileName: item.name,
        sizeBytes: item.sizeBytes,
        movedAt: DateTime.now(),
      ),
    );
  }

  Future<void> unlockPdfDocument(
    ManagedEntry entry,
    FileManagerService fileService,
  ) async {
    final locked = File(entry.storedPath);
    if (await locked.exists()) {
      final parent = Directory(p.dirname(entry.originalPath));
      final targetDir =
          await parent.exists() ? parent : await fileService.getAppPdfDirectory();
      var dest = p.join(targetDir.path, entry.fileName);
      if (await File(dest).exists()) {
        dest = p.join(
          targetDir.path,
          '${p.basenameWithoutExtension(entry.fileName)}_${DateTime.now().millisecondsSinceEpoch}.pdf',
        );
      }
      try {
        await locked.rename(dest);
      } catch (_) {
        await locked.copy(dest);
        await locked.delete();
      }
    }
    if (entry.id != null) {
      await AppDatabase.instance.deleteLockedEntry(entry.id!);
    }
  }

  String _hashPin(String pin, String salt) {
    final bytes = utf8.encode('$salt:$pin');
    return sha256.convert(bytes).toString();
  }
}
"""

# ==============================================================================
# 7. DOCUMENT SCANNER ENGINE (EDGE DETECTION, HOMOGRAPHY WARP & 6 FILTERS)
# ==============================================================================
FILES["lib/scanner/document_processor.dart"] = r"""import 'dart:io';
import 'dart:isolate';
import 'dart:math';
import 'dart:typed_data';
import 'package:image/image.dart' as img;
import '../models/scanned_page.dart';

class _ProcessRequest {
  final Uint8List rawBytes;
  final NormalizedQuad quad;
  final ScanFilterType filter;
  final double brightness;
  final double contrast;
  final int rotationTurns;

  const _ProcessRequest({
    required this.rawBytes,
    required this.quad,
    required this.filter,
    required this.brightness,
    required this.contrast,
    required this.rotationTurns,
  });
}

class DocumentProcessor {
  static Future<NormalizedQuad> detectDocumentCorners(String imagePath) async {
    final bytes = await File(imagePath).readAsBytes();
    return Isolate.run(() => detectCornersFromBytes(bytes));
  }

  static NormalizedQuad detectCornersFromBytes(Uint8List bytes) {
    final decoded = img.decodeImage(bytes);
    if (decoded == null) return NormalizedQuad.defaultInset();

    const targetW = 240;
    final scale = targetW / decoded.width;
    final targetH = max(60, (decoded.height * scale).round());
    final small = img.copyResize(decoded, width: targetW, height: targetH);
    final gray = img.grayscale(small);

    final grad = Float64List(targetW * targetH);
    double sumGrad = 0;
    int count = 0;

    for (int y = 1; y < targetH - 1; y++) {
      for (int x = 1; x < targetW - 1; x++) {
        final tl = gray.getPixel(x - 1, y - 1).r.toDouble();
        final tc = gray.getPixel(x, y - 1).r.toDouble();
        final tr = gray.getPixel(x + 1, y - 1).r.toDouble();
        final ml = gray.getPixel(x - 1, y).r.toDouble();
        final mr = gray.getPixel(x + 1, y).r.toDouble();
        final bl = gray.getPixel(x - 1, y + 1).r.toDouble();
        final bc = gray.getPixel(x, y + 1).r.toDouble();
        final br = gray.getPixel(x + 1, y + 1).r.toDouble();

        final gx = -tl + tr - 2 * ml + 2 * mr - bl + br;
        final gy = -tl - 2 * tc - tr + bl + 2 * bc + br;
        final mag = sqrt(gx * gx + gy * gy);
        grad[y * targetW + x] = mag;
        sumGrad += mag;
        count++;
      }
    }

    final threshold = max(45.0, (sumGrad / max(1, count)) * 2.1);

    Point<int>? bestTL;
    Point<int>? bestTR;
    Point<int>? bestBR;
    Point<int>? bestBL;
    double scoreTL = double.infinity;
    double scoreTR = double.infinity;
    double scoreBR = double.infinity;
    double scoreBL = double.infinity;

    final marginX = (targetW * 0.04).round();
    final marginY = (targetH * 0.04).round();

    for (int y = marginY; y < targetH - marginY; y++) {
      for (int x = marginX; x < targetW - marginX; x++) {
        if (grad[y * targetW + x] < threshold) continue;

        final dTL = hypot(x.toDouble(), y.toDouble());
        if (dTL < scoreTL) {
          scoreTL = dTL;
          bestTL = Point(x, y);
        }

        final dTR = hypot((targetW - 1 - x).toDouble(), y.toDouble());
        if (dTR < scoreTR) {
          scoreTR = dTR;
          bestTR = Point(x, y);
        }

        final dBR = hypot((targetW - 1 - x).toDouble(), (targetH - 1 - y).toDouble());
        if (dBR < scoreBR) {
          scoreBR = dBR;
          bestBR = Point(x, y);
        }

        final dBL = hypot(x.toDouble(), (targetH - 1 - y).toDouble());
        if (dBL < scoreBL) {
          scoreBL = dBL;
          bestBL = Point(x, y);
        }
      }
    }

    if (bestTL == null || bestTR == null || bestBR == null || bestBL == null) {
      return NormalizedQuad.defaultInset();
    }

    final quad = NormalizedQuad([
      Point(bestTL.x / targetW, bestTL.y / targetH),
      Point(bestTR.x / targetW, bestTR.y / targetH),
      Point(bestBR.x / targetW, bestBR.y / targetH),
      Point(bestBL.x / targetW, bestBL.y / targetH),
    ]);

    if (_polygonArea(quad.corners) < 0.15) {
      return NormalizedQuad.defaultInset();
    }
    return quad;
  }

  static double hypot(double a, double b) => sqrt(a * a + b * b);

  static double _polygonArea(List<Point<double>> pts) {
    double area = 0;
    for (int i = 0; i < pts.length; i++) {
      final j = (i + 1) % pts.length;
      area += pts[i].x * pts[j].y;
      area -= pts[j].x * pts[i].y;
    }
    return area.abs() / 2.0;
  }

  static Future<String> processPage({
    required String rawImagePath,
    required String outputImagePath,
    required NormalizedQuad quad,
    required ScanFilterType filter,
    double brightness = 0.0,
    double contrast = 1.15,
    int rotationQuarterTurns = 0,
  }) async {
    final bytes = await File(rawImagePath).readAsBytes();
    final req = _ProcessRequest(
      rawBytes: bytes,
      quad: quad,
      filter: filter,
      brightness: brightness,
      contrast: contrast,
      rotationTurns: rotationQuarterTurns % 4,
    );
    final outBytes = await Isolate.run(() => _runPipeline(req));
    await File(outputImagePath).writeAsBytes(outBytes, flush: true);
    return outputImagePath;
  }

  static Uint8List _runPipeline(_ProcessRequest req) {
    final src = img.decodeImage(req.rawBytes);
    if (src == null) return req.rawBytes;

    img.Image warped = perspectiveWarp(src, req.quad);

    if (req.rotationTurns != 0) {
      warped = img.copyRotate(warped, angle: req.rotationTurns * 90);
    }

    final enhanced = applyFilter(
      warped,
      req.filter,
      brightness: req.brightness,
      contrast: req.contrast,
    );

    return Uint8List.fromList(img.encodeJpg(enhanced, quality: 92));
  }

  static img.Image perspectiveWarp(img.Image src, NormalizedQuad quad) {
    final w = src.width.toDouble();
    final h = src.height.toDouble();

    final tl = Point(quad.corners[0].x * w, quad.corners[0].y * h);
    final tr = Point(quad.corners[1].x * w, quad.corners[1].y * h);
    final br = Point(quad.corners[2].x * w, quad.corners[2].y * h);
    final bl = Point(quad.corners[3].x * w, quad.corners[3].y * h);

    final topW = hypot(tr.x - tl.x, tr.y - tl.y);
    final bottomW = hypot(br.x - bl.x, br.y - bl.y);
    final leftH = hypot(bl.x - tl.x, bl.y - tl.y);
    final rightH = hypot(br.x - tr.x, br.y - tr.y);

    int outW = max(topW, bottomW).round().clamp(120, 2400);
    int outH = max(leftH, rightH).round().clamp(120, 3200);

    final dstPts = [
      const Point(0.0, 0.0),
      Point(outW - 1.0, 0.0),
      Point(outW - 1.0, outH - 1.0),
      Point(0.0, outH - 1.0),
    ];
    final srcPts = [tl, tr, br, bl];

    final hMat = computeHomography(dstPts, srcPts);
    final out = img.Image(width: outW, height: outH);

    for (int y = 0; y < outH; y++) {
      for (int x = 0; x < outW; x++) {
        final denom = hMat[6] * x + hMat[7] * y + 1.0;
        if (denom.abs() < 1e-8) continue;
        final sx = (hMat[0] * x + hMat[1] * y + hMat[2]) / denom;
        final sy = (hMat[3] * x + hMat[4] * y + hMat[5]) / denom;

        final ix = sx.floor();
        final iy = sy.floor();
        if (ix < 0 || iy < 0 || ix >= src.width - 1 || iy >= src.height - 1) {
          out.setPixelRgb(x, y, 255, 255, 255);
          continue;
        }

        final fx = sx - ix;
        final fy = sy - iy;

        final p00 = src.getPixel(ix, iy);
        final p10 = src.getPixel(ix + 1, iy);
        final p01 = src.getPixel(ix, iy + 1);
        final p11 = src.getPixel(ix + 1, iy + 1);

        final r = _bilerp(p00.r, p10.r, p01.r, p11.r, fx, fy).round().clamp(0, 255);
        final g = _bilerp(p00.g, p10.g, p01.g, p11.g, fx, fy).round().clamp(0, 255);
        final b = _bilerp(p00.b, p10.b, p01.b, p11.b, fx, fy).round().clamp(0, 255);

        out.setPixelRgb(x, y, r, g, b);
      }
    }
    return out;
  }

  static double _bilerp(num c00, num c10, num c01, num c11, double fx, double fy) {
    final top = c00 * (1 - fx) + c10 * fx;
    final bottom = c01 * (1 - fx) + c11 * fx;
    return top * (1 - fy) + bottom * fy;
  }

  static List<double> computeHomography(
    List<Point<double>> from,
    List<Point<double>> to,
  ) {
    final a = List.generate(8, (_) => List<double>.filled(9, 0.0));
    for (int i = 0; i < 4; i++) {
      final x = from[i].x;
      final y = from[i].y;
      final u = to[i].x;
      final v = to[i].y;

      a[2 * i] = [x, y, 1, 0, 0, 0, -u * x, -u * y, u];
      a[2 * i + 1] = [0, 0, 0, x, y, 1, -v * x, -v * y, v];
    }

    for (int col = 0; col < 8; col++) {
      int pivot = col;
      for (int row = col + 1; row < 8; row++) {
        if (a[row][col].abs() > a[pivot][col].abs()) pivot = row;
      }
      final tmp = a[col];
      a[col] = a[pivot];
      a[pivot] = tmp;

      final div = a[col][col].abs() < 1e-10 ? 1e-10 : a[col][col];
      for (int j = col; j <= 8; j++) {
        a[col][j] /= div;
      }
      for (int row = 0; row < 8; row++) {
        if (row == col) continue;
        final factor = a[row][col];
        for (int j = col; j <= 8; j++) {
          a[row][j] -= factor * a[col][j];
        }
      }
    }
    return List<double>.generate(8, (i) => a[i][8]);
  }

  static img.Image applyFilter(
    img.Image input,
    ScanFilterType filter, {
    double brightness = 0.0,
    double contrast = 1.15,
  }) {
    switch (filter) {
      case ScanFilterType.original:
        return input;

      case ScanFilterType.grayscale:
        return img.grayscale(img.Image.from(input));

      case ScanFilterType.blackAndWhite:
        final g = img.grayscale(img.Image.from(input));
        img.adjustColor(g, contrast: 1.55, brightness: 1.08);
        for (int y = 0; y < g.height; y++) {
          for (int x = 0; x < g.width; x++) {
            final lum = g.getPixel(x, y).r;
            final val = lum > 138 ? 255 : 0;
            g.setPixelRgb(x, y, val, val, val);
          }
        }
        return g;

      case ScanFilterType.magicColor:
        final copy = img.Image.from(input);
        img.adjustColor(
          copy,
          contrast: 1.32,
          saturation: 1.28,
          brightness: 1.08,
        );
        return copy;

      case ScanFilterType.enhancedDocument:
        final copy = img.Image.from(input);
        img.adjustColor(
          copy,
          contrast: 1.42,
          brightness: 1.10,
          saturation: 1.05,
        );
        return copy;

      case ScanFilterType.custom:
        final copy = img.Image.from(input);
        img.adjustColor(
          copy,
          brightness: 1.0 + brightness,
          contrast: contrast,
        );
        return copy;
    }
  }
}
"""

FILES["lib/providers/app_provider.dart"] = r"""import 'dart:io';
import 'package:flutter/material.dart';
import 'package:shared_preferences/shared_preferences.dart';
import '../database/app_database.dart';
import '../models/bookmark_item.dart';
import '../models/managed_entry.dart';
import '../models/pdf_document_item.dart';
import '../security/security_service.dart';
import '../services/file_manager_service.dart';

class AppProvider extends ChangeNotifier {
  final FileManagerService fileService = FileManagerService();
  final SecurityService securityService = SecurityService();

  Locale _locale = const Locale('en');
  ThemeMode _themeMode = ThemeMode.dark;
  bool _autoCaptureDefault = false;

  List<PdfDocumentItem> _allDocuments = [];
  List<PdfDocumentItem> _recentDocuments = [];
  List<BookmarkItem> _bookmarks = [];
  List<ManagedEntry> _binEntries = [];
  List<ManagedEntry> _lockedEntries = [];
  StorageStats _storageStats = const StorageStats(
    managedPdfBytes: 0,
    managedPdfCount: 0,
    binBytes: 0,
    vaultBytes: 0,
  );

  String _searchQuery = '';
  SortField _sortField = SortField.date;
  bool _sortAscending = false;
  bool _isLoading = false;

  bool _appLockEnabled = false;
  bool _biometricEnabled = false;
  bool _isUnlockedSession = true;

  Locale get locale => _locale;
  ThemeMode get themeMode => _themeMode;
  bool get autoCaptureDefault => _autoCaptureDefault;
  List<PdfDocumentItem> get recentDocuments => _recentDocuments;
  List<BookmarkItem> get bookmarks => _bookmarks;
  List<ManagedEntry> get binEntries => _binEntries;
  List<ManagedEntry> get lockedEntries => _lockedEntries;
  StorageStats get storageStats => _storageStats;
  String get searchQuery => _searchQuery;
  SortField get sortField => _sortField;
  bool get sortAscending => _sortAscending;
  bool get isLoading => _isLoading;
  bool get appLockEnabled => _appLockEnabled;
  bool get biometricEnabled => _biometricEnabled;
  bool get isUnlockedSession => _isUnlockedSession;

  List<PdfDocumentItem> get filteredDocuments {
    final q = _searchQuery.trim().toLowerCase();
    final filtered = q.isEmpty
        ? List<PdfDocumentItem>.from(_allDocuments)
        : _allDocuments.where((d) => d.name.toLowerCase().contains(q)).toList();

    filtered.sort((a, b) {
      int cmp;
      switch (_sortField) {
        case SortField.name:
          cmp = a.name.toLowerCase().compareTo(b.name.toLowerCase());
        case SortField.date:
          cmp = a.modifiedAt.compareTo(b.modifiedAt);
        case SortField.size:
          cmp = a.sizeBytes.compareTo(b.sizeBytes);
      }
      return _sortAscending ? cmp : -cmp;
    });
    return filtered;
  }

  Future<void> initialize() async {
    final prefs = await SharedPreferences.getInstance();
    final lang = prefs.getString('app_locale') ?? 'en';
    _locale = Locale(lang);
    final isDark = prefs.getBool('amoled_dark_mode') ?? true;
    _themeMode = isDark ? ThemeMode.dark : ThemeMode.light;
    _autoCaptureDefault = prefs.getBool('scanner_auto_capture') ?? false;

    _appLockEnabled = await securityService.isAppLockEnabled();
    _biometricEnabled = await securityService.isBiometricEnabled();
    _isUnlockedSession = !_appLockEnabled;

    notifyListeners();
    await refreshAll();
  }

  Future<void> refreshAll() async {
    _isLoading = true;
    notifyListeners();
    try {
      _allDocuments = await fileService.scanAccessiblePdfs();
      _bookmarks = await AppDatabase.instance.getBookmarks();
      _binEntries = await AppDatabase.instance.getBinEntries();
      _lockedEntries = await AppDatabase.instance.getLockedEntries();
      _storageStats = await fileService.computeStorageStats(_allDocuments);

      final recentPaths = await AppDatabase.instance.getRecentPaths();
      final byPath = {for (final d in _allDocuments) d.path: d};
      final recents = <PdfDocumentItem>[];
      for (final path in recentPaths) {
        if (byPath.containsKey(path)) {
          recents.add(byPath[path]!);
        } else if (await File(path).exists()) {
          final item = await PdfDocumentItem.fromFile(File(path));
          if (item != null) recents.add(item);
        }
      }
      _recentDocuments = recents;
    } finally {
      _isLoading = false;
      notifyListeners();
    }
  }

  void setSearchQuery(String query) {
    _searchQuery = query;
    notifyListeners();
  }

  void setSort(SortField field) {
    if (_sortField == field) {
      _sortAscending = !_sortAscending;
    } else {
      _sortField = field;
      _sortAscending = field == SortField.name;
    }
    notifyListeners();
  }

  Future<void> setLocale(String languageCode) async {
    _locale = Locale(languageCode);
    final prefs = await SharedPreferences.getInstance();
    await prefs.setString('app_locale', languageCode);
    notifyListeners();
  }

  Future<void> setDarkMode(bool dark) async {
    _themeMode = dark ? ThemeMode.dark : ThemeMode.light;
    final prefs = await SharedPreferences.getInstance();
    await prefs.setBool('amoled_dark_mode', dark);
    notifyListeners();
  }

  Future<void> setAutoCaptureDefault(bool value) async {
    _autoCaptureDefault = value;
    final prefs = await SharedPreferences.getInstance();
    await prefs.setBool('scanner_auto_capture', value);
    notifyListeners();
  }

  void unlockSession() {
    _isUnlockedSession = true;
    notifyListeners();
  }

  Future<void> refreshSecurityState() async {
    _appLockEnabled = await securityService.isAppLockEnabled();
    _biometricEnabled = await securityService.isBiometricEnabled();
    notifyListeners();
  }

  Future<void> recordOpened(String filePath) async {
    await AppDatabase.instance.recordRecentFile(filePath);
    await refreshAll();
  }

  Future<void> addBookmark(BookmarkItem item) async {
    await AppDatabase.instance.addBookmark(item);
    _bookmarks = await AppDatabase.instance.getBookmarks();
    notifyListeners();
  }

  Future<void> removeBookmark(int id) async {
    await AppDatabase.instance.removeBookmark(id);
    _bookmarks = await AppDatabase.instance.getBookmarks();
    notifyListeners();
  }
}
"""

FILES["lib/widgets/pin_dialog.dart"] = r"""import 'package:flutter/material.dart';

Future<String?> showPinPromptDialog(
  BuildContext context, {
  required String title,
  String? subtitle,
}) async {
  final controller = TextEditingController();
  return showDialog<String>(
    context: context,
    barrierDismissible: false,
    builder: (ctx) => AlertDialog(
      backgroundColor: const Color(0xFF121212),
      title: Text(title),
      content: Column(
        mainAxisSize: MainAxisSize.min,
        children: [
          if (subtitle != null) ...[
            Text(subtitle, style: const TextStyle(color: Colors.white70)),
            const SizedBox(height: 12),
          ],
          TextField(
            controller: controller,
            keyboardType: TextInputType.number,
            obscureText: true,
            maxLength: 6,
            autofocus: true,
            decoration: const InputDecoration(
              labelText: '4–6 Digit PIN',
              border: OutlineInputBorder(),
            ),
          ),
        ],
      ),
      actions: [
        TextButton(
          onPressed: () => Navigator.pop(ctx, null),
          child: const Text('Cancel'),
        ),
        FilledButton(
          onPressed: () {
            final text = controller.text.trim();
            if (text.length >= 4) {
              Navigator.pop(ctx, text);
            }
          },
          child: const Text('Confirm'),
        ),
      ],
    ),
  );
}
"""

FILES["lib/widgets/pdf_list_tile.dart"] = r"""import 'package:flutter/material.dart';
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
"""

FILES["lib/pdf_reader/pdf_reader_screen.dart"] = r"""import 'package:flutter/material.dart';
import 'package:pdfrx/pdfrx.dart';
import 'package:provider/provider.dart';
import 'package:share_plus/share_plus.dart';
import '../converters/pdf_converter_service.dart';
import '../l10n/app_localizations.dart';
import '../models/bookmark_item.dart';
import '../models/pdf_document_item.dart';
import '../providers/app_provider.dart';
import '../screens/converter_screen.dart';

class PdfReaderScreen extends StatefulWidget {
  final PdfDocumentItem documentItem;
  final int initialPage;

  const PdfReaderScreen({
    super.key,
    required this.documentItem,
    this.initialPage = 1,
  });

  @override
  State<PdfReaderScreen> createState() => _PdfReaderScreenState();
}

class _PdfReaderScreenState extends State<PdfReaderScreen> {
  late PdfDocumentItem _doc;
  final PdfViewerController _controller = PdfViewerController();
  late final PdfTextSearcher _textSearcher;

  int _currentPage = 1;
  int _totalPages = 0;
  bool _fitPageMode = false;
  bool _showSearchBar = false;
  final TextEditingController _searchCtrl = TextEditingController();

  @override
  void initState() {
    super.initState();
    _doc = widget.documentItem;
    _currentPage = widget.initialPage;
    _textSearcher = PdfTextSearcher(_controller)..addListener(_onSearchChanged);
  }

  void _onSearchChanged() {
    if (mounted) setState(() {});
  }

  @override
  void dispose() {
    _textSearcher.removeListener(_onSearchChanged);
    _textSearcher.dispose();
    _searchCtrl.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    final l10n = AppLocalizations.of(context);

    return Scaffold(
      backgroundColor: Colors.black,
      appBar: AppBar(
        backgroundColor: const Color(0xFF0A0A0A),
        title: Text(
          _doc.name,
          maxLines: 1,
          overflow: TextOverflow.ellipsis,
          style: const TextStyle(fontSize: 16),
        ),
        actions: [
          IconButton(
            tooltip: 'Search text',
            icon: Icon(_showSearchBar ? Icons.search_off : Icons.search),
            onPressed: () {
              setState(() {
                _showSearchBar = !_showSearchBar;
                if (!_showSearchBar) {
                  _searchCtrl.clear();
                  _textSearcher.resetTextSearch();
                }
              });
            },
          ),
          IconButton(
            tooltip: _fitPageMode ? 'Fit to Width' : 'Fit to Page',
            icon: Icon(_fitPageMode ? Icons.fit_screen : Icons.width_full_outlined),
            onPressed: _toggleFitMode,
          ),
          PopupMenuButton<String>(
            icon: const Icon(Icons.more_vert),
            color: const Color(0xFF161616),
            onSelected: (value) => _handleMenuAction(value, l10n),
            itemBuilder: (_) => [
              PopupMenuItem(value: 'share', child: Text(l10n.share)),
              PopupMenuItem(value: 'bookmark', child: Text(l10n.bookmark)),
              PopupMenuItem(value: 'rename', child: Text(l10n.rename)),
              PopupMenuItem(value: 'jpg', child: Text(l10n.convertToJpg)),
              PopupMenuItem(value: 'png', child: Text(l10n.convertToPng)),
              PopupMenuItem(
                value: 'delete',
                child: Text(l10n.delete, style: const TextStyle(color: Color(0xFFDC143C))),
              ),
            ],
          ),
        ],
      ),
      body: Column(
        children: [
          if (_showSearchBar) _buildSearchBanner(),
          Expanded(
            child: Stack(
              children: [
                PdfViewer.file(
                  _doc.path,
                  controller: _controller,
                  params: PdfViewerParams(
                    backgroundColor: Colors.black,
                    maxScale: 6.0,
                    minScale: 0.5,
                    pagePaintCallbacks: [
                      _textSearcher.pageTextMatchPaintCallback,
                    ],
                    onPageChanged: (pageNumber) {
                      if (pageNumber != null && mounted) {
                        setState(() => _currentPage = pageNumber);
                      }
                    },
                    onViewerReady: (document, controller) {
                      if (mounted) {
                        setState(() => _totalPages = document.pages.length);
                      }
                      if (widget.initialPage > 1 &&
                          widget.initialPage <= document.pages.length) {
                        controller.goToPage(pageNumber: widget.initialPage);
                      }
                    },
                  ),
                ),
                Positioned(
                  bottom: 16,
                  left: 16,
                  right: 16,
                  child: _buildPageHud(),
                ),
              ],
            ),
          ),
        ],
      ),
    );
  }

  Widget _buildSearchBanner() {
    final matches = _textSearcher.matches.length;
    final currentIdx = _textSearcher.currentIndex;

    return Container(
      color: const Color(0xFF141414),
      padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 6),
      child: Row(
        children: [
          Expanded(
            child: TextField(
              controller: _searchCtrl,
              autofocus: true,
              decoration: const InputDecoration(
                hintText: 'Find text in PDF...',
                isDense: true,
                border: OutlineInputBorder(),
              ),
              onChanged: (q) => _textSearcher.startTextSearch(q, caseInsensitive: true),
            ),
          ),
          const SizedBox(width: 8),
          Text(
            matches == 0 ? '0/0' : '${(currentIdx ?? 0) + 1}/$matches',
            style: const TextStyle(fontSize: 12, color: Colors.white70),
          ),
          IconButton(
            icon: const Icon(Icons.keyboard_arrow_up),
            onPressed: matches > 0 ? () => _textSearcher.goToPrevMatch() : null,
          ),
          IconButton(
            icon: const Icon(Icons.keyboard_arrow_down),
            onPressed: matches > 0 ? () => _textSearcher.goToNextMatch() : null,
          ),
        ],
      ),
    );
  }

  Widget _buildPageHud() {
    return Center(
      child: Container(
        padding: const EdgeInsets.symmetric(horizontal: 14, vertical: 6),
        decoration: BoxDecoration(
          color: const Color(0xFF121212).withValues(alpha: 0.92),
          borderRadius: BorderRadius.circular(24),
          border: Border.all(color: const Color(0xFFDC143C).withValues(alpha: 0.6)),
        ),
        child: Row(
          mainAxisSize: MainAxisSize.min,
          children: [
            IconButton(
              icon: const Icon(Icons.chevron_left, size: 20),
              constraints: const BoxConstraints(),
              padding: const EdgeInsets.all(4),
              onPressed: _currentPage > 1
                  ? () => _controller.goToPage(pageNumber: _currentPage - 1)
                  : null,
            ),
            InkWell(
              onTap: _promptJumpToPage,
              child: Padding(
                padding: const EdgeInsets.symmetric(horizontal: 10),
                child: Text(
                  'Page $_currentPage of ${_totalPages == 0 ? '?' : _totalPages}',
                  style: const TextStyle(fontWeight: FontWeight.w600, fontSize: 13),
                ),
              ),
            ),
            IconButton(
              icon: const Icon(Icons.chevron_right, size: 20),
              constraints: const BoxConstraints(),
              padding: const EdgeInsets.all(4),
              onPressed: _currentPage < _totalPages
                  ? () => _controller.goToPage(pageNumber: _currentPage + 1)
                  : null,
            ),
            const SizedBox(width: 8),
            IconButton(
              tooltip: 'Bookmark current page',
              icon: const Icon(Icons.bookmark_add_outlined, color: Color(0xFFDC143C), size: 20),
              constraints: const BoxConstraints(),
              padding: const EdgeInsets.all(4),
              onPressed: _bookmarkCurrentPage,
            ),
          ],
        ),
      ),
    );
  }

  void _toggleFitMode() {
    setState(() => _fitPageMode = !_fitPageMode);
    if (_controller.isReady) {
      _controller.setZoom(
        _controller.centerPosition,
        _fitPageMode ? 0.85 : 1.0,
      );
    }
  }

  Future<void> _promptJumpToPage() async {
    if (_totalPages <= 1) return;
    final ctrl = TextEditingController(text: '$_currentPage');
    final page = await showDialog<int>(
      context: context,
      builder: (ctx) => AlertDialog(
        backgroundColor: const Color(0xFF141414),
        title: Text('Jump to Page (1–$_totalPages)'),
        content: TextField(
          controller: ctrl,
          keyboardType: TextInputType.number,
          autofocus: true,
        ),
        actions: [
          TextButton(onPressed: () => Navigator.pop(ctx), child: const Text('Cancel')),
          FilledButton(
            onPressed: () => Navigator.pop(ctx, int.tryParse(ctrl.text)),
            child: const Text('Go'),
          ),
        ],
      ),
    );
    if (page != null && page >= 1 && page <= _totalPages) {
      _controller.goToPage(pageNumber: page);
    }
  }

  Future<void> _bookmarkCurrentPage() async {
    final provider = context.read<AppProvider>();
    await provider.addBookmark(
      BookmarkItem(
        filePath: _doc.path,
        fileName: _doc.name,
        pageNumber: _currentPage,
        label: 'Page $_currentPage',
        createdAt: DateTime.now(),
      ),
    );
    if (mounted) {
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content: Text('Bookmarked Page $_currentPage of ${_doc.name}')),
      );
    }
  }

  Future<void> _handleMenuAction(String action, AppLocalizations l10n) async {
    final provider = context.read<AppProvider>();

    switch (action) {
      case 'share':
        await Share.shareXFiles([XFile(_doc.path)], text: _doc.name);

      case 'bookmark':
        await _bookmarkCurrentPage();

      case 'rename':
        final ctrl = TextEditingController(
          text: _doc.name.replaceAll(RegExp(r'\.pdf$', caseSensitive: false), ''),
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
          final updatedPath = await provider.fileService.renamePdf(_doc.path, newName);
          if (updatedPath != null && mounted) {
            setState(() {
              _doc = PdfDocumentItem(
                path: updatedPath,
                name: updatedPath.split('/').last,
                sizeBytes: _doc.sizeBytes,
                modifiedAt: DateTime.now(),
              );
            });
            await provider.refreshAll();
          }
        }

      case 'jpg':
        if (!mounted) return;
        Navigator.push(
          context,
          MaterialPageRoute(
            builder: (_) => ConverterScreen(
              initialMode: ConverterMode.pdfToImage,
              preselectedPdfPath: _doc.path,
              initialFormat: OutputImageFormat.jpg,
            ),
          ),
        );

      case 'png':
        if (!mounted) return;
        Navigator.push(
          context,
          MaterialPageRoute(
            builder: (_) => ConverterScreen(
              initialMode: ConverterMode.pdfToImage,
              preselectedPdfPath: _doc.path,
              initialFormat: OutputImageFormat.png,
            ),
          ),
        );

      case 'delete':
        final confirmed = await showDialog<bool>(
          context: context,
          builder: (ctx) => AlertDialog(
            backgroundColor: const Color(0xFF141414),
            title: Text(l10n.delete),
            content: Text('Move "${_doc.name}" to Recycle Bin?'),
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
          await provider.fileService.moveToBin(_doc);
          await provider.refreshAll();
          if (mounted) Navigator.pop(context);
        }
    }
  }
}
"""

FILES["lib/scanner/crop_filter_screen.dart"] = r"""import 'dart:io';
import 'dart:math';
import 'package:flutter/material.dart';
import '../models/scanned_page.dart';
import 'document_processor.dart';

class CropFilterScreen extends StatefulWidget {
  final ScannedPage page;

  const CropFilterScreen({super.key, required this.page});

  @override
  State<CropFilterScreen> createState() => _CropFilterScreenState();
}

class _CropFilterScreenState extends State<CropFilterScreen> {
  late NormalizedQuad _quad;
  late ScanFilterType _filter;
  late double _brightness;
  late double _contrast;
  late int _rotationTurns;
  late String _previewPath;
  bool _isProcessing = false;
  bool _editingCorners = true;

  @override
  void initState() {
    super.initState();
    _quad = widget.page.quad;
    _filter = widget.page.filter;
    _brightness = widget.page.brightness;
    _contrast = widget.page.contrast;
       _rotationTurns = widget.page.rotationQuarterTurns;
    _previewPath = widget.page.processedImagePath;
  }

  Future<void> _applyWarpAndFilter() async {
    setState(() => _isProcessing = true);
    try {
      final outPath =
          '${widget.page.rawImagePath}_proc_${DateTime.now().millisecondsSinceEpoch}.jpg';
      await DocumentProcessor.processPage(
        rawImagePath: widget.page.rawImagePath,
        outputImagePath: outPath,
        quad: _quad,
        filter: _filter,
        brightness: _brightness,
        contrast: _contrast,
        rotationQuarterTurns: _rotationTurns,
      );
      if (mounted) {
        setState(() {
          _previewPath = outPath;
          _editingCorners = false;
        });
      }
    } finally {
      if (mounted) setState(() => _isProcessing = false);
    }
  }

  void _saveAndClose() {
    widget.page.quad = _quad;
    widget.page.filter = _filter;
    widget.page.brightness = _brightness;
    widget.page.contrast = _contrast;
    widget.page.rotationQuarterTurns = _rotationTurns;
    widget.page.processedImagePath = _previewPath;
    Navigator.pop(context, widget.page);
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: Colors.black,
      appBar: AppBar(
        backgroundColor: const Color(0xFF0A0A0A),
        title: Text(_editingCorners ? 'Adjust Document Corners' : 'Enhance Document'),
        actions: [
          IconButton(
            tooltip: 'Rotate 90°',
            icon: const Icon(Icons.rotate_right),
            onPressed: () async {
              setState(() => _rotationTurns = (_rotationTurns + 1) % 4);
              await _applyWarpAndFilter();
            },
          ),
          TextButton(
            onPressed: _isProcessing ? null : _saveAndClose,
            child: const Text(
              'DONE',
              style: TextStyle(color: Color(0xFFDC143C), fontWeight: FontWeight.bold),
            ),
          ),
        ],
      ),
      body: Column(
        children: [
          Expanded(
            child: Stack(
              alignment: Alignment.center,
              children: [
                if (_editingCorners)
                  _InteractiveQuadEditor(
                    imagePath: widget.page.rawImagePath,
                    quad: _quad,
                    onChanged: (q) => setState(() => _quad = q),
                  )
                else
                  Image.file(
                    File(_previewPath),
                    key: ValueKey(_previewPath),
                    fit: BoxFit.contain,
                  ),
                if (_isProcessing)
                  Container(
                    color: Colors.black54,
                    child: const Center(
                      child: CircularProgressIndicator(color: Color(0xFFDC143C)),
                    ),
                  ),
              ],
            ),
          ),
          _buildControlsPanel(),
        ],
      ),
    );
  }

  Widget _buildControlsPanel() {
    return Container(
      padding: const EdgeInsets.all(14),
      decoration: const BoxDecoration(
        color: Color(0xFF0F0F0F),
        border: Border(top: BorderSide(color: Colors.white12)),
      ),
      child: Column(
        mainAxisSize: MainAxisSize.min,
        children: [
          Row(
            children: [
              Expanded(
                child: OutlinedButton.icon(
                  icon: Icon(_editingCorners ? Icons.crop_free : Icons.edit_location_alt),
                  label: Text(_editingCorners ? 'Editing 4 Corners' : 'Re-adjust Crop'),
                  onPressed: () => setState(() => _editingCorners = true),
                ),
              ),
              const SizedBox(width: 10),
              Expanded(
                child: FilledButton.icon(
                  icon: const Icon(Icons.auto_fix_high),
                  label: const Text('Apply Warp & Filter'),
                  onPressed: _isProcessing ? null : _applyWarpAndFilter,
                ),
              ),
            ],
          ),
          const SizedBox(height: 12),
          SizedBox(
            height: 44,
            child: ListView(
              scrollDirection: Axis.horizontal,
              children: ScanFilterType.values.map((f) {
                final selected = _filter == f;
                return Padding(
                  padding: const EdgeInsets.only(right: 8),
                  child: ChoiceChip(
                    label: Text(_filterLabel(f)),
                    selected: selected,
                    selectedColor: const Color(0xFFDC143C),
                    onSelected: (_) async {
                      setState(() => _filter = f);
                      await _applyWarpAndFilter();
                    },
                  ),
                );
              }).toList(),
            ),
          ),
          if (_filter == ScanFilterType.custom) ...[
            const SizedBox(height: 8),
            Row(
              children: [
                const Text('Brightness', style: TextStyle(fontSize: 12)),
                Expanded(
                  child: Slider(
                    value: _brightness,
                    min: -0.4,
                    max: 0.4,
                    activeColor: const Color(0xFFDC143C),
                    onChanged: (v) => setState(() => _brightness = v),
                    onChangeEnd: (_) => _applyWarpAndFilter(),
                  ),
                ),
              ],
            ),
            Row(
              children: [
                const Text('Contrast', style: TextStyle(fontSize: 12)),
                Expanded(
                  child: Slider(
                    value: _contrast,
                    min: 0.6,
                    max: 1.9,
                    activeColor: const Color(0xFFDC143C),
                    onChanged: (v) => setState(() => _contrast = v),
                    onChangeEnd: (_) => _applyWarpAndFilter(),
                  ),
                ),
              ],
            ),
          ],
        ],
      ),
    );
  }

  String _filterLabel(ScanFilterType f) {
    switch (f) {
      case ScanFilterType.original:
        return 'Original';
      case ScanFilterType.blackAndWhite:
        return 'Black & White';
      case ScanFilterType.grayscale:
        return 'Grayscale';
      case ScanFilterType.magicColor:
        return 'Magic Color';
      case ScanFilterType.enhancedDocument:
        return 'Enhanced Doc';
      case ScanFilterType.custom:
        return 'Custom';
    }
  }
}

class _InteractiveQuadEditor extends StatelessWidget {
  final String imagePath;
  final NormalizedQuad quad;
  final ValueChanged<NormalizedQuad> onChanged;

  const _InteractiveQuadEditor({
    required this.imagePath,
    required this.quad,
    required this.onChanged,
  });

  @override
  Widget build(BuildContext context) {
    return LayoutBuilder(
      builder: (context, constraints) {
        final w = constraints.maxWidth;
        final h = constraints.maxHeight;

        return Stack(
          fit: StackFit.expand,
          children: [
            Image.file(File(imagePath), fit: BoxFit.fill),
            CustomPaint(
              painter: _QuadPainter(quad),
            ),
            for (int i = 0; i < 4; i++)
              Positioned(
                left: quad.corners[i].x * w - 18,
                top: quad.corners[i].y * h - 18,
                child: GestureDetector(
                  onPanUpdate: (details) {
                    final nx = (quad.corners[i].x * w + details.delta.dx) / w;
                    final ny = (quad.corners[i].y * h + details.delta.dy) / h;
                    onChanged(quad.copyWithCorner(i, Point(nx, ny)));
                  },
                  child: Container(
                    width: 36,
                    height: 36,
                    decoration: BoxDecoration(
                      color: const Color(0xFFDC143C).withValues(alpha: 0.85),
                      shape: BoxShape.circle,
                      border: Border.all(color: Colors.white, width: 2.5),
                    ),
                    child: Center(
                      child: Text(
                        '${i + 1}',
                        style: const TextStyle(fontSize: 11, fontWeight: FontWeight.bold),
                      ),
                    ),
                  ),
                ),
              ),
          ],
        );
      },
    );
  }
}

class _QuadPainter extends CustomPainter {
  final NormalizedQuad quad;
  _QuadPainter(this.quad);

  @override
  void paint(Canvas canvas, Size size) {
    final pts = quad.corners
        .map((p) => Offset(p.x * size.width, p.y * size.height))
        .toList();

    final path = Path()
      ..moveTo(pts[0].dx, pts[0].dy)
      ..lineTo(pts[1].dx, pts[1].dy)
      ..lineTo(pts[2].dx, pts[2].dy)
      ..lineTo(pts[3].dx, pts[3].dy)
      ..close();

    canvas.drawPath(
      path,
      Paint()
        ..color = const Color(0xFFDC143C).withValues(alpha: 0.18)
        ..style = PaintingStyle.fill,
    );
    canvas.drawPath(
      path,
      Paint()
        ..color = const Color(0xFFDC143C)
        ..strokeWidth = 2.5
        ..style = PaintingStyle.stroke,
    );
  }

  @override
  bool shouldRepaint(covariant _QuadPainter oldDelegate) => oldDelegate.quad != quad;
}
"""
FILES["lib/scanner/scanner_screen.dart"] = r"""import 'dart:async';
import 'dart:io';
import 'package:camera/camera.dart';
import 'package:file_picker/file_picker.dart';
import 'package:flutter/material.dart';
import 'package:path/path.dart' as p;
import 'package:path_provider/path_provider.dart';
import 'package:permission_handler/permission_handler.dart';
import 'package:provider/provider.dart';
import '../converters/pdf_converter_service.dart';
import '../models/scanned_page.dart';
import '../providers/app_provider.dart';
import 'crop_filter_screen.dart';
import 'document_processor.dart';

class ScannerScreen extends StatefulWidget {
  const ScannerScreen({super.key});

  @override
  State<ScannerScreen> createState() => _ScannerScreenState();
}

class _ScannerScreenState extends State<ScannerScreen> {
  CameraController? _cameraController;
  bool _cameraReady = false;
  bool _flashOn = false;
  bool _autoCapture = false;
  bool _isBusy = false;
  Timer? _autoCaptureTimer;

  final List<ScannedPage> _sessionPages = [];

  @override
  void initState() {
    super.initState();
    _autoCapture = context.read<AppProvider>().autoCaptureDefault;
    _initCamera();
  }

  Future<void> _initCamera() async {
    final status = await Permission.camera.request();
    if (!status.isGranted) return;

    try {
      final cameras = await availableCameras();
      if (cameras.isEmpty) return;
      final back = cameras.firstWhere(
        (c) => c.lensDirection == CameraLensDirection.back,
        orElse: () => cameras.first,
      );
      final ctrl = CameraController(
        back,
        ResolutionPreset.high,
        enableAudio: false,
        imageFormatGroup: ImageFormatGroup.jpeg,
      );
      await ctrl.initialize();
      if (!mounted) return;
      setState(() {
        _cameraController = ctrl;
        _cameraReady = true;
      });
      if (_autoCapture) _startAutoCaptureTimer();
    } catch (_) {}
  }

  void _startAutoCaptureTimer() {
    _autoCaptureTimer?.cancel();
    _autoCaptureTimer = Timer.periodic(const Duration(seconds: 4), (_) {
      if (_autoCapture && _cameraReady && !_isBusy && mounted) {
        _captureFromCamera();
      }
    });
  }

  @override
  void dispose() {
    _autoCaptureTimer?.cancel();
    _cameraController?.dispose();
    super.dispose();
  }

  Future<void> _toggleFlash() async {
    if (_cameraController == null || !_cameraReady) return;
    final next = !_flashOn;
    await _cameraController!.setFlashMode(next ? FlashMode.torch : FlashMode.off);
    setState(() => _flashOn = next);
  }

  Future<void> _captureFromCamera({int? replaceIndex}) async {
    if (_cameraController == null || !_cameraReady || _isBusy) return;
    setState(() => _isBusy = true);
    try {
      final xFile = await _cameraController!.takePicture();
      await _ingestImageFile(xFile.path, replaceIndex: replaceIndex);
    } finally {
      if (mounted) setState(() => _isBusy = false);
    }
  }

  Future<void> _importFromGallery() async {
    final res = await FilePicker.pickFiles(
      type: FileType.image,
      allowMultiple: true,
    );
    if (res == null) return;
    setState(() => _isBusy = true);
    try {
      for (final f in res.files) {
        if (f.path != null) {
          await _ingestImageFile(f.path!);
        }
      }
    } finally {
      if (mounted) setState(() => _isBusy = false);
    }
  }

  Future<void> _ingestImageFile(String sourcePath, {int? replaceIndex}) async {
    final cacheDir = await getTemporaryDirectory();
    final id = DateTime.now().microsecondsSinceEpoch.toString();
    final rawCopy = p.join(cacheDir.path, 'scan_raw_$id.jpg');
    final procOut = p.join(cacheDir.path, 'scan_proc_$id.jpg');
    await File(sourcePath).copy(rawCopy);

    final detectedQuad = await DocumentProcessor.detectDocumentCorners(rawCopy);
    await DocumentProcessor.processPage(
      rawImagePath: rawCopy,
      outputImagePath: procOut,
      quad: detectedQuad,
      filter: ScanFilterType.enhancedDocument,
    );

    final page = ScannedPage(
      id: id,
      rawImagePath: rawCopy,
      processedImagePath: procOut,
      quad: detectedQuad,
    );

    if (!mounted) return;
    setState(() {
      if (replaceIndex != null && replaceIndex < _sessionPages.length) {
        _sessionPages[replaceIndex] = page;
      } else {
        _sessionPages.add(page);
      }
    });
  }

  Future<void> _exportSessionToPdf() async {
    if (_sessionPages.isEmpty) return;
    final provider = context.read<AppProvider>();
    final nameCtrl = TextEditingController(
      text: 'Scan_${DateTime.now().year}${DateTime.now().month.toString().padLeft(2, '0')}${DateTime.now().day.toString().padLeft(2, '0')}_${DateTime.now().hour}${DateTime.now().minute}',
    );
    final chosenName = await showDialog<String>(
      context: context,
      builder: (ctx) => AlertDialog(
        backgroundColor: const Color(0xFF141414),
        title: const Text('Export Scanned PDF'),
        content: TextField(
          controller: nameCtrl,
          decoration: const InputDecoration(labelText: 'PDF Filename'),
        ),
        actions: [
          TextButton(onPressed: () => Navigator.pop(ctx), child: const Text('Cancel')),
          FilledButton(
            onPressed: () => Navigator.pop(ctx, nameCtrl.text),
            child: const Text('Export PDF'),
          ),
        ],
      ),
    );
    if (chosenName == null) return;

    setState(() => _isBusy = true);
    try {
      final outDir = await provider.fileService.getAppPdfDirectory();
      final converter = PdfConverterService();
      final savedPath = await converter.convertImagesToPdf(
        imagePaths: _sessionPages.map((e) => e.processedImagePath).toList(),
        outputFileName: chosenName,
        outputFolder: outDir.path,
      );
      await provider.refreshAll();
      if (!mounted) return;
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content: Text('Saved PDF: ${p.basename(savedPath)}')),
      );
      Navigator.pop(context);
    } finally {
      if (mounted) setState(() => _isBusy = false);
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: Colors.black,
      appBar: AppBar(
        backgroundColor: const Color(0xFF0A0A0A),
        title: Text('Document Scanner (${_sessionPages.length})'),
        actions: [
          IconButton(
            tooltip: 'Toggle Flash',
            icon: Icon(_flashOn ? Icons.flash_on : Icons.flash_off),
            onPressed: _toggleFlash,
          ),
          IconButton(
            tooltip: 'Auto-Capture',
            icon: Icon(
              _autoCapture ? Icons.hdr_auto : Icons.hdr_auto_outlined,
              color: _autoCapture ? const Color(0xFFDC143C) : Colors.white,
            ),
            onPressed: () {
              setState(() => _autoCapture = !_autoCapture);
              if (_autoCapture) {
                _startAutoCaptureTimer();
              } else {
                _autoCaptureTimer?.cancel();
              }
            },
          ),
          if (_sessionPages.isNotEmpty)
            TextButton(
              onPressed: _isBusy ? null : _exportSessionToPdf,
              child: const Text(
                'SAVE PDF',
                style: TextStyle(color: Color(0xFFDC143C), fontWeight: FontWeight.bold),
              ),
            ),
        ],
      ),
      body: Column(
        children: [
          Expanded(
            flex: 3,
            child: Stack(
              fit: StackFit.expand,
              children: [
                if (_cameraReady && _cameraController != null)
                  CameraPreview(_cameraController!)
                else
                  const Center(
                    child: Text(
                      'Camera preview unavailable.\nUse Gallery Import below to scan images.',
                      textAlign: TextAlign.center,
                      style: TextStyle(color: Colors.white60),
                    ),
                  ),
                IgnorePointer(
                  child: Container(
                    margin: const EdgeInsets.all(24),
                    decoration: BoxDecoration(
                      border: Border.all(
                        color: const Color(0xFFDC143C).withValues(alpha: 0.7),
                        width: 2,
                      ),
                      borderRadius: BorderRadius.circular(12),
                    ),
                  ),
                ),
                if (_isBusy)
                  Container(
                    color: Colors.black54,
                    child: const Center(
                      child: CircularProgressIndicator(color: Color(0xFFDC143C)),
                    ),
                  ),
              ],
            ),
          ),
          if (_sessionPages.isNotEmpty)
            SizedBox(
              height: 126,
              child: ReorderableListView.builder(
                scrollDirection: Axis.horizontal,
                padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 8),
                itemCount: _sessionPages.length,
                onReorder: (oldIndex, newIndex) {
                  setState(() {
                    if (newIndex > oldIndex) newIndex -= 1;
                    final item = _sessionPages.removeAt(oldIndex);
                    _sessionPages.insert(newIndex, item);
                  });
                },
                itemBuilder: (context, index) {
                  final page = _sessionPages[index];
                  return Container(
                    key: ValueKey(page.id),
                    width: 88,
                    margin: const EdgeInsets.only(right: 8),
                    decoration: BoxDecoration(
                      border: Border.all(color: const Color(0xFFDC143C)),
                      borderRadius: BorderRadius.circular(8),
                    ),
                    child: Stack(
                      fit: StackFit.expand,
                      children: [
                        GestureDetector(
                          onTap: () async {
                            final updated = await Navigator.push<ScannedPage>(
                              context,
                              MaterialPageRoute(
                                builder: (_) => CropFilterScreen(page: page),
                              ),
                            );
                            if (updated != null && mounted) setState(() {});
                          },
                          child: ClipRRect(
                            borderRadius: BorderRadius.circular(7),
                            child: Image.file(
                              File(page.processedImagePath),
                              key: ValueKey(page.processedImagePath),
                              fit: BoxFit.cover,
                            ),
                          ),
                        ),
                        Positioned(
                          top: 2,
                          left: 4,
                          child: CircleAvatar(
                            radius: 10,
                            backgroundColor: Colors.black87,
                            child: Text(
                              '${index + 1}',
                              style: const TextStyle(fontSize: 10, color: Colors.white),
                            ),
                          ),
                        ),
                        Positioned(
                          top: 0,
                          right: 0,
                          child: InkWell(
                            onTap: () => setState(() => _sessionPages.removeAt(index)),
                            child: const CircleAvatar(
                              radius: 11,
                              backgroundColor: Color(0xFFDC143C),
                              child: Icon(Icons.close, size: 13, color: Colors.white),
                            ),
                          ),
                        ),
                        Positioned(
                          bottom: 2,
                          right: 2,
                          child: InkWell(
                            onTap: () => _captureFromCamera(replaceIndex: index),
                            child: const CircleAvatar(
                              radius: 11,
                              backgroundColor: Colors.black87,
                              child: Icon(Icons.refresh, size: 13, color: Colors.white),
                            ),
                          ),
                        ),
                      ],
                    ),
                  );
                },
              ),
            ),
          Container(
            padding: const EdgeInsets.symmetric(horizontal: 24, vertical: 14),
            color: const Color(0xFF0A0A0A),
            child: Row(
              mainAxisAlignment: MainAxisAlignment.spaceAround,
              children: [
                IconButton.filledTonal(
                  tooltip: 'Import from Gallery',
                  icon: const Icon(Icons.photo_library_outlined),
                  onPressed: _isBusy ? null : _importFromGallery,
                ),
                GestureDetector(
                  onTap: _isBusy ? null : () => _captureFromCamera(),
                  child: Container(
                    width: 68,
                    height: 68,
                    decoration: BoxDecoration(
                      shape: BoxShape.circle,
                      border: Border.all(color: Colors.white, width: 3),
                      color: const Color(0xFFDC143C),
                    ),
                    child: const Icon(Icons.camera_alt, color: Colors.white, size: 30),
                  ),
                ),
                IconButton.filledTonal(
                  tooltip: 'Edit Last Page',
                  icon: const Icon(Icons.tune),
                  onPressed: _sessionPages.isEmpty
                      ? null
                      : () async {
                          final updated = await Navigator.push<ScannedPage>(
                            context,
                            MaterialPageRoute(
                              builder: (_) => CropFilterScreen(page: _sessionPages.last),
                            ),
                          );
                          if (updated != null && mounted) setState(() {});
                        },
                ),
              ],
            ),
          ),
        ],
      ),
    );
  }
}
"""

FILES["lib/screens/converter_screen.dart"] = r"""import 'dart:io';
import 'package:file_picker/file_picker.dart';
import 'package:flutter/material.dart';
import 'package:path/path.dart' as p;
import 'package:provider/provider.dart';
import 'package:share_plus/share_plus.dart';
import '../converters/pdf_converter_service.dart';
import '../providers/app_provider.dart';

enum ConverterMode { pdfToImage, imagesToPdf }

class ConverterScreen extends StatefulWidget {
  final ConverterMode initialMode;
  final String? preselectedPdfPath;
  final OutputImageFormat initialFormat;

  const ConverterScreen({
    super.key,
    required this.initialMode,
    this.preselectedPdfPath,
    this.initialFormat = OutputImageFormat.jpg,
  });

  @override
  State<ConverterScreen> createState() => _ConverterScreenState();
}

class _ConverterScreenState extends State<ConverterScreen> {
  final PdfConverterService _converter = PdfConverterService();
  late ConverterMode _mode;
  late OutputImageFormat _format;
  ConversionQuality _quality = ConversionQuality.high;

  String? _selectedPdfPath;
  int _pdfTotalPages = 0;
  bool _convertAllPages = true;
  final TextEditingController _pageRangeCtrl = TextEditingController(text: '1');

  final List<String> _selectedImages = [];
  final TextEditingController _outPdfNameCtrl = TextEditingController(text: 'Merged_Images');

  String? _customOutputFolder;
  bool _isConverting = false;
  String _progressText = '';
  List<String> _generatedFiles = [];

  @override
  void initState() {
    super.initState();
    _mode = widget.initialMode;
    _format = widget.initialFormat;
    if (widget.preselectedPdfPath != null) {
      _loadPdf(widget.preselectedPdfPath!);
    }
  }

  Future<void> _loadPdf(String path) async {
    final count = await _converter.getPageCount(path);
    if (mounted) {
      setState(() {
        _selectedPdfPath = path;
        _pdfTotalPages = count;
        _generatedFiles = [];
      });
    }
  }

  List<int> _parsePageSelection(String input, int maxPages) {
    final result = <int>{};
    for (final part in input.split(',')) {
      final trimmed = part.trim();
      if (trimmed.contains('-')) {
        final bounds = trimmed.split('-');
        if (bounds.length == 2) {
          final start = int.tryParse(bounds[0].trim()) ?? 1;
          final end = int.tryParse(bounds[1].trim()) ?? maxPages;
          for (int i = start; i <= end; i++) {
            if (i >= 1 && i <= maxPages) {
              result.add(i);
            }
          }
        }
      } else {
        final single = int.tryParse(trimmed);
        if (single != null && single >= 1 && single <= maxPages) {
          result.add(single);
        }
      }
    }
    return result.toList()..sort();
  }

  Future<void> _runConversion() async {
    setState(() {
      _isConverting = true;
      _generatedFiles = [];
    });
    try {
      if (_mode == ConverterMode.pdfToImage && _selectedPdfPath != null) {
        final pages = _convertAllPages
            ? null
            : _parsePageSelection(_pageRangeCtrl.text, _pdfTotalPages);
        final files = await _converter.convertPdfToImages(
          pdfPath: _selectedPdfPath!,
          format: _format,
          pages: pages,
          quality: _quality,
          outputFolder: _customOutputFolder,
          onProgress: (cur, tot) {
            if (mounted) {
              setState(() => _progressText = 'Rendering page $cur of $tot...');
            }
          },
        );
        if (mounted) setState(() => _generatedFiles = files);
      } else if (_mode == ConverterMode.imagesToPdf && _selectedImages.isNotEmpty) {
        final provider = context.read<AppProvider>();
        final outPdf = await _converter.convertImagesToPdf(
          imagePaths: _selectedImages,
          outputFileName: _outPdfNameCtrl.text,
          quality: _quality,
          outputFolder: _customOutputFolder,
          onProgress: (cur, tot) {
            if (mounted) {
              setState(() => _progressText = 'Embedding image $cur of $tot...');
            }
          },
        );
        await provider.refreshAll();
        if (mounted) setState(() => _generatedFiles = [outPdf]);
      }
    } finally {
      if (mounted) {
        setState(() {
          _isConverting = false;
          _progressText = '';
        });
      }
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: Colors.black,
      appBar: AppBar(
        backgroundColor: const Color(0xFF0A0A0A),
        title: Text(_mode == ConverterMode.pdfToImage ? 'PDF to Image' : 'Images to PDF'),
      ),
      body: ListView(
        padding: const EdgeInsets.all(16),
        children: [
          SegmentedButton<ConverterMode>(
            segments: const [
              ButtonSegment(value: ConverterMode.pdfToImage, label: Text('PDF → JPG/PNG')),
              ButtonSegment(value: ConverterMode.imagesToPdf, label: Text('Images → PDF')),
            ],
            selected: {_mode},
            onSelectionChanged: (s) => setState(() {
              _mode = s.first;
              _generatedFiles = [];
            }),
          ),
          const SizedBox(height: 16),
          if (_mode == ConverterMode.pdfToImage) ...[
            OutlinedButton.icon(
              icon: const Icon(Icons.picture_as_pdf),
              label: Text(
                _selectedPdfPath == null
                    ? 'Select Source PDF'
                    : '${p.basename(_selectedPdfPath!)} ($_pdfTotalPages pages)',
              ),
              onPressed: () async {
                final res = await FilePicker.pickFiles(
                  type: FileType.custom,
                  allowedExtensions: ['pdf'],
                );
                if (res != null && res.files.single.path != null) {
                  await _loadPdf(res.files.single.path!);
                }
              },
            ),
            const SizedBox(height: 12),
            SegmentedButton<OutputImageFormat>(
              segments: const [
                ButtonSegment(value: OutputImageFormat.jpg, label: Text('JPG')),
                ButtonSegment(value: OutputImageFormat.png, label: Text('PNG')),
              ],
              selected: {_format},
              onSelectionChanged: (s) => setState(() => _format = s.first),
            ),
            SwitchListTile(
              title: const Text('Convert All Pages'),
              value: _convertAllPages,
              activeThumbColor: const Color(0xFFDC143C),
              onChanged: (v) => setState(() => _convertAllPages = v),
            ),
            if (!_convertAllPages)
              TextField(
                controller: _pageRangeCtrl,
                decoration: const InputDecoration(
                  labelText: 'Selected Pages (e.g. 1, 3-5)',
                  border: OutlineInputBorder(),
                ),
              ),
          ] else ...[
            OutlinedButton.icon(
              icon: const Icon(Icons.add_photo_alternate),
              label: Text('Select Images (${_selectedImages.length} selected)'),
              onPressed: () async {
                final res = await FilePicker.pickFiles(
                  type: FileType.image,
                  allowMultiple: true,
                );
                if (res != null) {
                  setState(() {
                    _selectedImages.addAll(
                      res.files.where((f) => f.path != null).map((f) => f.path!),
                    );
                  });
                }
              },
            ),
            const SizedBox(height: 12),
            TextField(
              controller: _outPdfNameCtrl,
              decoration: const InputDecoration(
                labelText: 'Output PDF Name',
                border: OutlineInputBorder(),
              ),
            ),
          ],
          const SizedBox(height: 12),
          DropdownButtonFormField<ConversionQuality>(
            initialValue: _quality,
            decoration: const InputDecoration(
              labelText: 'Output Quality',
              border: OutlineInputBorder(),
            ),
            items: ConversionQuality.values
                .map((q) => DropdownMenuItem(value: q, child: Text(q.label)))
                .toList(),
            onChanged: (q) {
              if (q != null) setState(() => _quality = q);
            },
          ),
          const SizedBox(height: 12),
          OutlinedButton.icon(
            icon: const Icon(Icons.folder_open),
            label: Text(
              _customOutputFolder == null
                  ? 'Output Folder: Default (PDFProConverted)'
                  : 'Output: $_customOutputFolder',
              maxLines: 1,
              overflow: TextOverflow.ellipsis,
            ),
            onPressed: () async {
              final dir = await FilePicker.getDirectoryPath();
              if (dir != null) setState(() => _customOutputFolder = dir);
            },
          ),
          const SizedBox(height: 18),
          FilledButton.icon(
            icon: const Icon(Icons.bolt),
            label: Text(_isConverting ? _progressText : 'Start Conversion'),
            onPressed: _isConverting ? null : _runConversion,
          ),
          if (_generatedFiles.isNotEmpty) ...[
            const SizedBox(height: 20),
            Row(
              mainAxisAlignment: MainAxisAlignment.spaceBetween,
              children: [
                Text(
                  'Converted Files (${_generatedFiles.length})',
                  style: const TextStyle(fontWeight: FontWeight.bold, fontSize: 16),
                ),
                FilledButton.tonalIcon(
                  icon: const Icon(Icons.share),
                  label: const Text('Share All'),
                  onPressed: () => Share.shareXFiles(
                    _generatedFiles.map((path) => XFile(path)).toList(),
                  ),
                ),
              ],
            ),
            const SizedBox(height: 10),
            _selectedPdfPath == null
                    ? 'Select Source PDF'
                    : '${p.basename(_selectedPdfPath!)} ($_pdfTotalPages pages)',
              ),
              onPressed: () async {
                final res = await FilePicker.pickFiles(
                  type: FileType.custom,
                  allowedExtensions: ['pdf'],
                );
                if (res != null && res.files.single.path != null) {
                  await _loadPdf(res.files.single.path!);
                }
              },
            ),
            const SizedBox(height: 12),
            SegmentedButton<OutputImageFormat>(
              segments: const [
                ButtonSegment(value: OutputImageFormat.jpg, label: Text('JPG')),
                ButtonSegment(value: OutputImageFormat.png, label: Text('PNG')),
              ],
              selected: {_format},
              onSelectionChanged: (s) => setState(() => _format = s.first),
            ),
            SwitchListTile(
              title: const Text('Convert All Pages'),
              value: _convertAllPages,
              activeThumbColor: const Color(0xFFDC143C),
              onChanged: (v) => setState(() => _convertAllPages = v),
            ),
            if (!_convertAllPages)
              TextField(
                controller: _pageRangeCtrl,
                decoration: const InputDecoration(
                  labelText: 'Selected Pages (e.g. 1, 3-5)',
                  border: OutlineInputBorder(),
                ),
              ),
          ] else ...[
            OutlinedButton.icon(
              icon: const Icon(Icons.add_photo_alternate),
              label: Text('Select Images (${_selectedImages.length} selected)'),
              onPressed: () async {
                final res = await FilePicker.pickFiles(
                  type: FileType.image,
                  allowMultiple: true,
                );
                if (res != null) {
                  setState(() {
                    _selectedImages.addAll(
                      res.files.where((f) => f.path != null).map((f) => f.path!),
                    );
                  });
                }
              },
            ),
            const SizedBox(height: 12),
            TextField(
              controller: _outPdfNameCtrl,
              decoration: const InputDecoration(
                labelText: 'Output PDF Name',
                border: OutlineInputBorder(),
              ),
            ),
          ],
          const SizedBox(height: 12),
          DropdownButtonFormField<ConversionQuality>(
            initialValue: _quality,
            decoration: const InputDecoration(
              labelText: 'Output Quality',
              border: OutlineInputBorder(),
            ),
            items: ConversionQuality.values
                .map((q) => DropdownMenuItem(value: q, child: Text(q.label)))
                .toList(),
            onChanged: (q) {
              if (q != null) setState(() => _quality = q);
            },
          ),
          const SizedBox(height: 12),
          OutlinedButton.icon(
            icon: const Icon(Icons.folder_open),
            label: Text(
              _customOutputFolder == null
                  ? 'Output Folder: Default (PDFProConverted)'
                  : 'Output: $_customOutputFolder',
              maxLines: 1,
              overflow: TextOverflow.ellipsis,
            ),
            onPressed: () async {
              final dir = await FilePicker.getDirectoryPath();
              if (dir != null) setState(() => _customOutputFolder = dir);
            },
          ),
          const SizedBox(height: 18),
          FilledButton.icon(
            icon: const Icon(Icons.bolt),
            label: Text(_isConverting ? _progressText : 'Start Conversion'),
            onPressed: _isConverting ? null : _runConversion,
          ),
          if (_generatedFiles.isNotEmpty) ...[
            const SizedBox(height: 20),
            Row(
              mainAxisAlignment: MainAxisAlignment.spaceBetween,
              children: [
                Text(
                  'Converted Files (${_generatedFiles.length})',
                  style: const TextStyle(fontWeight: FontWeight.bold, fontSize: 16),
                ),
                FilledButton.tonalIcon(
                  icon: const Icon(Icons.share),
                  label: const Text('Share All'),
                  onPressed: () => Share.shareXFiles(
                    _generatedFiles.map((path) => XFile(path)).toList(),
                  ),
                ),
              ],
            ),
            const SizedBox(height: 10),
            ..._generatedFiles.map(
              (filePath) => Card(
                color: const Color(0xFF121212),
                child: ListTile(
                  leading: filePath.endsWith('.pdf')
                      ? const Icon(Icons.picture_as_pdf, color: Color(0xFFDC143C))
                      : Image.file(File(filePath), width: 44, height: 44, fit: BoxFit.cover),
                  title: Text(p.basename(filePath), maxLines: 1, overflow: TextOverflow.ellipsis),
                  trailing: IconButton(
                    icon: const Icon(Icons.share),
                    onPressed: () => Share.shareXFiles([XFile(filePath)]),
                  ),
                ),
              ),
            ),
          ],
        ],
      ),
    );
  }
}
"""
FILES["lib/screens/bin_screen.dart"] = r"""import 'package:flutter/material.dart';
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
"""

FILES["lib/screens/vault_screen.dart"] = r"""import 'package:flutter/material.dart';
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
"""

FILES["lib/screens/home_screen.dart"] = r"""import 'package:flutter/material.dart';
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
"""

FILES["lib/screens/documents_screen.dart"] = r"""import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import '../l10n/app_localizations.dart';
import '../models/pdf_document_item.dart';
import '../providers/app_provider.dart';
import '../widgets/pdf_list_tile.dart';

class DocumentsScreen extends StatelessWidget {
  const DocumentsScreen({super.key});

  @override
  Widget build(BuildContext context) {
    final l10n = AppLocalizations.of(context);
    final provider = context.watch<AppProvider>();
    final docs = provider.filteredDocuments;

    return Column(
      children: [
        Padding(
          padding: const EdgeInsets.fromLTRB(14, 10, 14, 6),
          child: Row(
            children: [
              Expanded(
                child: TextField(
                  onChanged: provider.setSearchQuery,
                  decoration: InputDecoration(
                    hintText: l10n.searchHint,
                    prefixIcon: const Icon(Icons.search),
                    filled: true,
                    fillColor: const Color(0xFF121212),
                    isDense: true,
                    border: OutlineInputBorder(
                      borderRadius: BorderRadius.circular(12),
                      borderSide: BorderSide.none,
                    ),
                  ),
                ),
              ),
              const SizedBox(width: 8),
              PopupMenuButton<SortField>(
                tooltip: l10n.sortBy,
                icon: const Icon(Icons.sort_rounded),
                color: const Color(0xFF161616),
                onSelected: provider.setSort,
                itemBuilder: (_) => [
                  PopupMenuItem(value: SortField.name, child: Text(l10n.sortName)),
                  PopupMenuItem(value: SortField.date, child: Text(l10n.sortDate)),
                  PopupMenuItem(value: SortField.size, child: Text(l10n.sortSize)),
                ],
              ),
            ],
          ),
        ),
        Padding(
          padding: const EdgeInsets.symmetric(horizontal: 14, vertical: 4),
          child: Row(
            children: [
              Expanded(
                child: OutlinedButton.icon(
                  icon: const Icon(Icons.create_new_folder_outlined, size: 18),
                  label: Text(l10n.addFolder),
                  onPressed: () async {
                    await provider.fileService.authorizeNewFolder();
                    await provider.refreshAll();
                  },
                ),
              ),
              const SizedBox(width: 8),
              Expanded(
                child: OutlinedButton.icon(
                  icon: const Icon(Icons.file_open_outlined, size: 18),
                  label: Text(l10n.openPdf),
                  onPressed: () async {
                    await provider.fileService.importExternalPdfs();
                    await provider.refreshAll();
                  },
                ),
              ),
            ],
          ),
        ),
        Expanded(
          child: RefreshIndicator(
            color: const Color(0xFFDC143C),
            onRefresh: provider.refreshAll,
            child: docs.isEmpty
                ? ListView(
                    children: [
                      const SizedBox(height: 80),
                      Center(
                        child: Padding(
                          padding: const EdgeInsets.all(24),
                          child: Text(
                            l10n.noDocuments,
                            textAlign: TextAlign.center,
                            style: const TextStyle(color: Colors.white60),
                          ),
                        ),
                      ),
                    ],
                  )
                : ListView.builder(
                    itemCount: docs.length,
                    itemBuilder: (_, index) => PdfListTile(item: docs[index]),
                  ),
          ),
        ),
      ],
    );
  }
}
"""
FILES["lib/screens/tools_screen.dart"] = r"""import 'package:flutter/material.dart';
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
"""

FILES["lib/screens/bookmarks_screen.dart"] = r"""import 'dart:io';
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
"""

FILES["lib/screens/me_screen.dart"] = r"""import 'package:flutter/material.dart';
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
"""
FILES["lib/screens/main_shell.dart"] = r"""import 'package:flutter/material.dart';
import '../l10n/app_localizations.dart';
import 'bookmarks_screen.dart';
import 'documents_screen.dart';
import 'home_screen.dart';
import 'me_screen.dart';
import 'tools_screen.dart';

class MainShell extends StatefulWidget {
  const MainShell({super.key});

  @override
  State<MainShell> createState() => _MainShellState();
}

class _MainShellState extends State<MainShell> {
  int _currentIndex = 0;

  final List<Widget> _screens = const [
    HomeScreen(),
    DocumentsScreen(),
    ToolsScreen(),
    MeScreen(),
    BookmarksScreen(),
  ];

  @override
  Widget build(BuildContext context) {
    final l10n = AppLocalizations.of(context);

    return Scaffold(
      appBar: AppBar(
        backgroundColor: Colors.black,
        title: Row(
          children: [
            Container(
              padding: const EdgeInsets.all(6),
              decoration: BoxDecoration(
                color: const Color(0xFFDC143C),
                borderRadius: BorderRadius.circular(8),
              ),
              child: const Icon(Icons.picture_as_pdf, color: Colors.white, size: 18),
            ),
            const SizedBox(width: 10),
            Text(
              l10n.appName,
              style: const TextStyle(fontWeight: FontWeight.w800, letterSpacing: 0.3),
            ),
          ],
        ),
      ),
      body: IndexedStack(
        index: _currentIndex,
        children: _screens,
      ),
      bottomNavigationBar: NavigationBar(
        selectedIndex: _currentIndex,
        backgroundColor: const Color(0xFF080808),
        indicatorColor: const Color(0xFFDC143C).withValues(alpha: 0.24),
        onDestinationSelected: (idx) => setState(() => _currentIndex = idx),
        destinations: [
          NavigationDestination(
            icon: const Icon(Icons.home_outlined),
            selectedIcon: const Icon(Icons.home, color: Color(0xFFDC143C)),
            label: l10n.home,
          ),
          NavigationDestination(
            icon: const Icon(Icons.folder_copy_outlined),
            selectedIcon: const Icon(Icons.folder_copy, color: Color(0xFFDC143C)),
            label: l10n.documents,
          ),
          NavigationDestination(
            icon: const Icon(Icons.grid_view_outlined),
            selectedIcon: const Icon(Icons.grid_view_rounded, color: Color(0xFFDC143C)),
            label: l10n.tools,
          ),
          NavigationDestination(
            icon: const Icon(Icons.person_outline),
            selectedIcon: const Icon(Icons.person, color: Color(0xFFDC143C)),
            label: l10n.me,
          ),
          NavigationDestination(
            icon: const Icon(Icons.bookmarks_outlined),
            selectedIcon: const Icon(Icons.bookmarks, color: Color(0xFFDC143C)),
            label: l10n.bookmarks,
          ),
        ],
      ),
    );
  }
}
"""

FILES["lib/main.dart"] = r"""import 'package:flutter/material.dart';
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
"""

FILES["test/widget_test.dart"] = r"""import 'dart:math';
import 'dart:typed_data';
import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:image/image.dart' as img;
import 'package:pdf_pro_no_ad/l10n/app_localizations.dart';
import 'package:pdf_pro_no_ad/models/pdf_document_item.dart';
import 'package:pdf_pro_no_ad/models/scanned_page.dart';
import 'package:pdf_pro_no_ad/scanner/document_processor.dart';

void main() {
  test('Projective homography accurately maps tilted quadrilateral to rectangle', () {
    final src = img.Image(width: 200, height: 200);
    img.fill(src, color: img.ColorRgb8(20, 20, 20));
    for (int y = 40; y < 160; y++) {
      for (int x = 40; x < 160; x++) {
        src.setPixelRgb(x, y, 240, 240, 240);
      }
    }

    const quad = NormalizedQuad([
      Point(0.2, 0.2),
      Point(0.8, 0.2),
      Point(0.8, 0.8),
      Point(0.2, 0.8),
    ]);

    final warped = DocumentProcessor.perspectiveWarp(src, quad);
    expect(warped.width, equals(120));
    expect(warped.height, equals(120));
    final centerPixel = warped.getPixel(60, 60);
    expect(centerPixel.r, greaterThan(220));
  });

  test('Automatic edge detector locates high-contrast rectangular document', () {
    final canvas = img.Image(width: 240, height: 320);
    img.fill(canvas, color: img.ColorRgb8(15, 15, 15));
    for (int y = 48; y < 272; y++) {
      for (int x = 36; x < 204; x++) {
        canvas.setPixelRgb(x, y, 245, 245, 245);
      }
    }
    final jpg = Uint8List.fromList(img.encodeJpg(canvas));
    final quad = DocumentProcessor.detectCornersFromBytes(jpg);
    expect(quad.corners.length, equals(4));
    expect(quad.corners[0].x, lessThan(0.3));
    expect(quad.corners[2].x, greaterThan(0.7));
  });

  test('PdfDocumentItem formats file sizes accurately', () {
    final item = PdfDocumentItem(
      path: '/tmp/sample.pdf',
      name: 'sample.pdf',
      sizeBytes: 2097152,
      modifiedAt: DateTime(2026, 1, 1),
    );
    expect(item.formattedSize, equals('2.00 MB'));
  });

  test('AppLocalizations supports English and Bangla', () {
    const en = AppLocalizations(Locale('en'));
    const bn = AppLocalizations(Locale('bn'));
    expect(en.home, equals('Home'));
    expect(bn.home, equals('হোম'));
  });
}
"""

FILES["README.md"] = r"""# PDF Pro No Ad (`com.comeback.pdfprona`)

Offline-first, ad-free Android PDF Reader, File Manager, Document Scanner, and PDF Converter built with Flutter and Dart.
"""


def main() -> None:
    root = Path(__file__).resolve().parent
    for rel_path, content in FILES.items():
        target = root / rel_path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(content.lstrip("\n"), encoding="utf-8")
        print(f"Wrote {rel_path}")
    print(f"\nGenerated {len(FILES)} files successfully.")


if __name__ == "__main__":
    main()
