import 'dart:convert';
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
