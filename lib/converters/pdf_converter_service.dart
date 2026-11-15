import 'dart:io';
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
