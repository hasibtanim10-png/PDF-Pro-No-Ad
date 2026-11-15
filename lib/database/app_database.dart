import 'package:path/path.dart' as p;
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
