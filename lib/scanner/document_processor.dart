import 'dart:io';
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
