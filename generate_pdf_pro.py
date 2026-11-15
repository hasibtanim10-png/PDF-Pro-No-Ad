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

    for (int y = marginY; y < targetH
