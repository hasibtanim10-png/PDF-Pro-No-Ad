import 'dart:math';
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
