import 'package:flutter/material.dart';

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
