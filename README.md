# PDF-Pro-No-Ad# PDF Pro No Ad (`com.comeback.pdfprona`)

**PDF Pro No Ad** is a premium, 100% offline-first, ad-free Android PDF Reader, Document Manager, CamScanner-style Document Scanner, and PDF/Image Converter built with Flutter and Dart.

## Key Features
- **AMOLED Pitch-Black & Crimson Red UI:** Material 3 dark interface (`#000000` background with `#DC143C` crimson accents) supporting both **English** and **Bangla (বাংলা)**.
- **5-Tab Bottom Navigation:** Home, Documents, Tools, Me, and Bookmarks.
- **Automatic PDF Discovery & File Manager:** Scans authorized folders via Android Storage Access Framework (SAF), supports search by filename, sorting (name, date, size), renaming, Recycle Bin (move, restore, permanent delete), and storage analytics.
- **Professional Multi-Script PDF Reader:** Smooth vertical scrolling, pinch-to-zoom, page jump HUD, fit-to-width/page, in-document text search, page bookmarking, and single-document actions. Supports Bengali, English, Arabic, Urdu, Hindi, Chinese, Japanese, and Korean documents.
- **CamScanner-Style Document Scanner:** Live camera preview, flashlight toggle, auto-capture, gallery import, automatic edge detection, manual 4-corner adjustment, projective homography perspective correction, 6 enhancement filters (Original, Black & White, Grayscale, Magic Color, Enhanced Document, Custom Brightness/Contrast), and multi-page PDF export.
- **PDF & Image Conversion Tools:** Convert selected or all PDF pages to JPG/PNG, and merge multiple gallery images into a single PDF with quality and output folder selection.
- **Privacy & Security:**
  - Zero advertisements, trackers, or analytics.
  - **No `INTERNET` permission** in `AndroidManifest.xml` — all processing happens locally on the device.
  - SHA-256 salted PIN App Lock, Biometric authentication, and a hidden Locked Vault for sensitive PDFs.

## Build & Release APK (GitHub Actions)
1. Push `generate_pdf_pro.py` and `.github/workflows/build.yml` to the `main` branch.
2. Open the **Actions** tab and select **Build PDF Pro No Ad Release APK**.
3. Download **`PDF-Pro-No-Ad-v1.0.0-release-apk`** from the **Artifacts** section once the workflow completes.

---
**Developed by:** Come Back (HASIBUR RAHMAN)  
**Package ID:** `com.comeback.pdfprona` | **Version:** `1.0.0`
