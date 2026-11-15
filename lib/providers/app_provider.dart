import 'dart:io';
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
