import 'dart:math';

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
