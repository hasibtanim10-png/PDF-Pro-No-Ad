import 'dart:io';
import 'dart:math';
import 'package:flutter/material.dart';
import '../models/scanned_page.dart';
import 'document_processor.dart';

class CropFilterScreen extends StatefulWidget {
  final ScannedPage page;

  const CropFilterScreen({super.key, required this.page});

  @override
  State<CropFilterScreen> createState() => _CropFilterScreenState();
}

class _CropFilterScreenState extends State<CropFilterScreen> {
  late NormalizedQuad _quad;
  late ScanFilterType _filter;
  late double _brightness;
  late double _contrast;
  late int _rotationTurns;
  late String _previewPath;
  bool _isProcessing = false;
  bool _editingCorners = true;

  @override
  void initState() {
    super.initState();
    _quad = widget.page.quad;
    _filter = widget.page.filter;
    _brightness = widget.page.brightness;
    _contrast = widget.page.contrast;
       _rotationTurns = widget.page.rotationQuarterTurns;
    _previewPath = widget.page.processedImagePath;
  }

  Future<void> _applyWarpAndFilter() async {
    setState(() => _isProcessing = true);
    try {
      final outPath =
          '${widget.page.rawImagePath}_proc_${DateTime.now().millisecondsSinceEpoch}.jpg';
      await DocumentProcessor.processPage(
        rawImagePath: widget.page.rawImagePath,
        outputImagePath: outPath,
        quad: _quad,
        filter: _filter,
        brightness: _brightness,
        contrast: _contrast,
        rotationQuarterTurns: _rotationTurns,
      );
      if (mounted) {
        setState(() {
          _previewPath = outPath;
          _editingCorners = false;
        });
      }
    } finally {
      if (mounted) setState(() => _isProcessing = false);
    }
  }

  void _saveAndClose() {
    widget.page.quad = _quad;
    widget.page.filter = _filter;
    widget.page.brightness = _brightness;
    widget.page.contrast = _contrast;
    widget.page.rotationQuarterTurns = _rotationTurns;
    widget.page.processedImagePath = _previewPath;
    Navigator.pop(context, widget.page);
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: Colors.black,
      appBar: AppBar(
        backgroundColor: const Color(0xFF0A0A0A),
        title: Text(_editingCorners ? 'Adjust Document Corners' : 'Enhance Document'),
        actions: [
          IconButton(
            tooltip: 'Rotate 90°',
            icon: const Icon(Icons.rotate_right),
            onPressed: () async {
              setState(() => _rotationTurns = (_rotationTurns + 1) % 4);
              await _applyWarpAndFilter();
            },
          ),
          TextButton(
            onPressed: _isProcessing ? null : _saveAndClose,
            child: const Text(
              'DONE',
              style: TextStyle(color: Color(0xFFDC143C), fontWeight: FontWeight.bold),
            ),
          ),
        ],
      ),
      body: Column(
        children: [
          Expanded(
            child: Stack(
              alignment: Alignment.center,
              children: [
                if (_editingCorners)
                  _InteractiveQuadEditor(
                    imagePath: widget.page.rawImagePath,
                    quad: _quad,
                    onChanged: (q) => setState(() => _quad = q),
                  )
                else
                  Image.file(
                    File(_previewPath),
                    key: ValueKey(_previewPath),
                    fit: BoxFit.contain,
                  ),
                if (_isProcessing)
                  Container(
                    color: Colors.black54,
                    child: const Center(
                      child: CircularProgressIndicator(color: Color(0xFFDC143C)),
                    ),
                  ),
              ],
            ),
          ),
          _buildControlsPanel(),
        ],
      ),
    );
  }

  Widget _buildControlsPanel() {
    return Container(
      padding: const EdgeInsets.all(14),
      decoration: const BoxDecoration(
        color: Color(0xFF0F0F0F),
        border: Border(top: BorderSide(color: Colors.white12)),
      ),
      child: Column(
        mainAxisSize: MainAxisSize.min,
        children: [
          Row(
            children: [
              Expanded(
                child: OutlinedButton.icon(
                  icon: Icon(_editingCorners ? Icons.crop_free : Icons.edit_location_alt),
                  label: Text(_editingCorners ? 'Editing 4 Corners' : 'Re-adjust Crop'),
                  onPressed: () => setState(() => _editingCorners = true),
                ),
              ),
              const SizedBox(width: 10),
              Expanded(
                child: FilledButton.icon(
                  icon: const Icon(Icons.auto_fix_high),
                  label: const Text('Apply Warp & Filter'),
                  onPressed: _isProcessing ? null : _applyWarpAndFilter,
                ),
              ),
            ],
          ),
          const SizedBox(height: 12),
          SizedBox(
            height: 44,
            child: ListView(
              scrollDirection: Axis.horizontal,
              children: ScanFilterType.values.map((f) {
                final selected = _filter == f;
                return Padding(
                  padding: const EdgeInsets.only(right: 8),
                  child: ChoiceChip(
                    label: Text(_filterLabel(f)),
                    selected: selected,
                    selectedColor: const Color(0xFFDC143C),
                    onSelected: (_) async {
                      setState(() => _filter = f);
                      await _applyWarpAndFilter();
                    },
                  ),
                );
              }).toList(),
            ),
          ),
          if (_filter == ScanFilterType.custom) ...[
            const SizedBox(height: 8),
            Row(
              children: [
                const Text('Brightness', style: TextStyle(fontSize: 12)),
                Expanded(
                  child: Slider(
                    value: _brightness,
                    min: -0.4,
                    max: 0.4,
                    activeColor: const Color(0xFFDC143C),
                    onChanged: (v) => setState(() => _brightness = v),
                    onChangeEnd: (_) => _applyWarpAndFilter(),
                  ),
                ),
              ],
            ),
            Row(
              children: [
                const Text('Contrast', style: TextStyle(fontSize: 12)),
                Expanded(
                  child: Slider(
                    value: _contrast,
                    min: 0.6,
                    max: 1.9,
                    activeColor: const Color(0xFFDC143C),
                    onChanged: (v) => setState(() => _contrast = v),
                    onChangeEnd: (_) => _applyWarpAndFilter(),
                  ),
                ),
              ],
            ),
          ],
        ],
      ),
    );
  }

  String _filterLabel(ScanFilterType f) {
    switch (f) {
      case ScanFilterType.original:
        return 'Original';
      case ScanFilterType.blackAndWhite:
        return 'Black & White';
      case ScanFilterType.grayscale:
        return 'Grayscale';
      case ScanFilterType.magicColor:
        return 'Magic Color';
      case ScanFilterType.enhancedDocument:
        return 'Enhanced Doc';
      case ScanFilterType.custom:
        return 'Custom';
    }
  }
}

class _InteractiveQuadEditor extends StatelessWidget {
  final String imagePath;
  final NormalizedQuad quad;
  final ValueChanged<NormalizedQuad> onChanged;

  const _InteractiveQuadEditor({
    required this.imagePath,
    required this.quad,
    required this.onChanged,
  });

  @override
  Widget build(BuildContext context) {
    return LayoutBuilder(
      builder: (context, constraints) {
        final w = constraints.maxWidth;
        final h = constraints.maxHeight;

        return Stack(
          fit: StackFit.expand,
          children: [
            Image.file(File(imagePath), fit: BoxFit.fill),
            CustomPaint(
              painter: _QuadPainter(quad),
            ),
            for (int i = 0; i < 4; i++)
              Positioned(
                left: quad.corners[i].x * w - 18,
                top: quad.corners[i].y * h - 18,
                child: GestureDetector(
                  onPanUpdate: (details) {
                    final nx = (quad.corners[i].x * w + details.delta.dx) / w;
                    final ny = (quad.corners[i].y * h + details.delta.dy) / h;
                    onChanged(quad.copyWithCorner(i, Point(nx, ny)));
                  },
                  child: Container(
                    width: 36,
                    height: 36,
                    decoration: BoxDecoration(
                      color: const Color(0xFFDC143C).withValues(alpha: 0.85),
                      shape: BoxShape.circle,
                      border: Border.all(color: Colors.white, width: 2.5),
                    ),
                    child: Center(
                      child: Text(
                        '${i + 1}',
                        style: const TextStyle(fontSize: 11, fontWeight: FontWeight.bold),
                      ),
                    ),
                  ),
                ),
              ),
          ],
        );
      },
    );
  }
}

class _QuadPainter extends CustomPainter {
  final NormalizedQuad quad;
  _QuadPainter(this.quad);

  @override
  void paint(Canvas canvas, Size size) {
    final pts = quad.corners
        .map((p) => Offset(p.x * size.width, p.y * size.height))
        .toList();

    final path = Path()
      ..moveTo(pts[0].dx, pts[0].dy)
      ..lineTo(pts[1].dx, pts[1].dy)
      ..lineTo(pts[2].dx, pts[2].dy)
      ..lineTo(pts[3].dx, pts[3].dy)
      ..close();

    canvas.drawPath(
      path,
      Paint()
        ..color = const Color(0xFFDC143C).withValues(alpha: 0.18)
        ..style = PaintingStyle.fill,
    );
    canvas.drawPath(
      path,
      Paint()
        ..color = const Color(0xFFDC143C)
        ..strokeWidth = 2.5
        ..style = PaintingStyle.stroke,
    );
  }

  @override
  bool shouldRepaint(covariant _QuadPainter oldDelegate) => oldDelegate.quad != quad;
}
