import 'dart:async';
import 'dart:io';
import 'package:camera/camera.dart';
import 'package:file_picker/file_picker.dart';
import 'package:flutter/material.dart';
import 'package:path/path.dart' as p;
import 'package:path_provider/path_provider.dart';
import 'package:permission_handler/permission_handler.dart';
import 'package:provider/provider.dart';
import '../converters/pdf_converter_service.dart';
import '../models/scanned_page.dart';
import '../providers/app_provider.dart';
import 'crop_filter_screen.dart';
import 'document_processor.dart';

class ScannerScreen extends StatefulWidget {
  const ScannerScreen({super.key});

  @override
  State<ScannerScreen> createState() => _ScannerScreenState();
}

class _ScannerScreenState extends State<ScannerScreen> {
  CameraController? _cameraController;
  bool _cameraReady = false;
  bool _flashOn = false;
  bool _autoCapture = false;
  bool _isBusy = false;
  Timer? _autoCaptureTimer;

  final List<ScannedPage> _sessionPages = [];

  @override
  void initState() {
    super.initState();
    _autoCapture = context.read<AppProvider>().autoCaptureDefault;
    _initCamera();
  }

  Future<void> _initCamera() async {
    final status = await Permission.camera.request();
    if (!status.isGranted) return;

    try {
      final cameras = await availableCameras();
      if (cameras.isEmpty) return;
      final back = cameras.firstWhere(
        (c) => c.lensDirection == CameraLensDirection.back,
        orElse: () => cameras.first,
      );
      final ctrl = CameraController(
        back,
        ResolutionPreset.high,
        enableAudio: false,
        imageFormatGroup: ImageFormatGroup.jpeg,
      );
      await ctrl.initialize();
      if (!mounted) return;
      setState(() {
        _cameraController = ctrl;
        _cameraReady = true;
      });
      if (_autoCapture) _startAutoCaptureTimer();
    } catch (_) {}
  }

  void _startAutoCaptureTimer() {
    _autoCaptureTimer?.cancel();
    _autoCaptureTimer = Timer.periodic(const Duration(seconds: 4), (_) {
      if (_autoCapture && _cameraReady && !_isBusy && mounted) {
        _captureFromCamera();
      }
    });
  }

  @override
  void dispose() {
    _autoCaptureTimer?.cancel();
    _cameraController?.dispose();
    super.dispose();
  }

  Future<void> _toggleFlash() async {
    if (_cameraController == null || !_cameraReady) return;
    final next = !_flashOn;
    await _cameraController!.setFlashMode(next ? FlashMode.torch : FlashMode.off);
    setState(() => _flashOn = next);
  }

  Future<void> _captureFromCamera({int? replaceIndex}) async {
    if (_cameraController == null || !_cameraReady || _isBusy) return;
    setState(() => _isBusy = true);
    try {
      final xFile = await _cameraController!.takePicture();
      await _ingestImageFile(xFile.path, replaceIndex: replaceIndex);
    } finally {
      if (mounted) setState(() => _isBusy = false);
    }
  }

  Future<void> _importFromGallery() async {
    final res = await FilePicker.platform.pickFiles(
      type: FileType.image,
      allowMultiple: true,
    );
    if (res == null) return;
    setState(() => _isBusy = true);
    try {
      for (final f in res.files) {
        if (f.path != null) {
          await _ingestImageFile(f.path!);
        }
      }
    } finally {
      if (mounted) setState(() => _isBusy = false);
    }
  }

  Future<void> _ingestImageFile(String sourcePath, {int? replaceIndex}) async {
    final cacheDir = await getTemporaryDirectory();
    final id = DateTime.now().microsecondsSinceEpoch.toString();
    final rawCopy = p.join(cacheDir.path, 'scan_raw_$id.jpg');
    final procOut = p.join(cacheDir.path, 'scan_proc_$id.jpg');
    await File(sourcePath).copy(rawCopy);

    final detectedQuad = await DocumentProcessor.detectDocumentCorners(rawCopy);
    await DocumentProcessor.processPage(
      rawImagePath: rawCopy,
      outputImagePath: procOut,
      quad: detectedQuad,
      filter: ScanFilterType.enhancedDocument,
    );

    final page = ScannedPage(
      id: id,
      rawImagePath: rawCopy,
      processedImagePath: procOut,
      quad: detectedQuad,
    );

    if (!mounted) return;
    setState(() {
      if (replaceIndex != null && replaceIndex < _sessionPages.length) {
        _sessionPages[replaceIndex] = page;
      } else {
        _sessionPages.add(page);
      }
    });
  }

  Future<void> _exportSessionToPdf() async {
    if (_sessionPages.isEmpty) return;
    final provider = context.read<AppProvider>();
    final nameCtrl = TextEditingController(
      text: 'Scan_${DateTime.now().year}${DateTime.now().month.toString().padLeft(2, '0')}${DateTime.now().day.toString().padLeft(2, '0')}_${DateTime.now().hour}${DateTime.now().minute}',
    );
    final chosenName = await showDialog<String>(
      context: context,
      builder: (ctx) => AlertDialog(
        backgroundColor: const Color(0xFF141414),
        title: const Text('Export Scanned PDF'),
        content: TextField(
          controller: nameCtrl,
          decoration: const InputDecoration(labelText: 'PDF Filename'),
        ),
        actions: [
          TextButton(onPressed: () => Navigator.pop(ctx), child: const Text('Cancel')),
          FilledButton(
            onPressed: () => Navigator.pop(ctx, nameCtrl.text),
            child: const Text('Export PDF'),
          ),
        ],
      ),
    );
    if (chosenName == null) return;

    setState(() => _isBusy = true);
    try {
      final outDir = await provider.fileService.getAppPdfDirectory();
      final converter = PdfConverterService();
      final savedPath = await converter.convertImagesToPdf(
        imagePaths: _sessionPages.map((e) => e.processedImagePath).toList(),
        outputFileName: chosenName,
        outputFolder: outDir.path,
      );
      await provider.refreshAll();
      if (!mounted) return;
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content: Text('Saved PDF: ${p.basename(savedPath)}')),
      );
      Navigator.pop(context);
    } finally {
      if (mounted) setState(() => _isBusy = false);
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: Colors.black,
      appBar: AppBar(
        backgroundColor: const Color(0xFF0A0A0A),
        title: Text('Document Scanner (${_sessionPages.length})'),
        actions: [
          IconButton(
            tooltip: 'Toggle Flash',
            icon: Icon(_flashOn ? Icons.flash_on : Icons.flash_off),
            onPressed: _toggleFlash,
          ),
          IconButton(
            tooltip: 'Auto-Capture',
            icon: Icon(
              _autoCapture ? Icons.hdr_auto : Icons.hdr_auto_outlined,
              color: _autoCapture ? const Color(0xFFDC143C) : Colors.white,
            ),
            onPressed: () {
              setState(() => _autoCapture = !_autoCapture);
              if (_autoCapture) {
                _startAutoCaptureTimer();
              } else {
                _autoCaptureTimer?.cancel();
              }
            },
          ),
          if (_sessionPages.isNotEmpty)
            TextButton(
              onPressed: _isBusy ? null : _exportSessionToPdf,
              child: const Text(
                'SAVE PDF',
                style: TextStyle(color: Color(0xFFDC143C), fontWeight: FontWeight.bold),
              ),
            ),
        ],
      ),
      body: Column(
        children: [
          Expanded(
            flex: 3,
            child: Stack(
              fit: StackFit.expand,
              children: [
                if (_cameraReady && _cameraController != null)
                  CameraPreview(_cameraController!)
                else
                  const Center(
                    child: Text(
                      'Camera preview unavailable.\nUse Gallery Import below to scan images.',
                      textAlign: TextAlign.center,
                      style: TextStyle(color: Colors.white60),
                    ),
                  ),
                IgnorePointer(
                  child: Container(
                    margin: const EdgeInsets.all(24),
                    decoration: BoxDecoration(
                      border: Border.all(
                        color: const Color(0xFFDC143C).withValues(alpha: 0.7),
                        width: 2,
                      ),
                      borderRadius: BorderRadius.circular(12),
                    ),
                  ),
                ),
                if (_isBusy)
                  Container(
                    color: Colors.black54,
                    child: const Center(
                      child: CircularProgressIndicator(color: Color(0xFFDC143C)),
                    ),
                  ),
              ],
            ),
          ),
          if (_sessionPages.isNotEmpty)
            SizedBox(
              height: 126,
              child: ReorderableListView.builder(
                scrollDirection: Axis.horizontal,
                padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 8),
                itemCount: _sessionPages.length,
                onReorder: (oldIndex, newIndex) {
                  setState(() {
                    if (newIndex > oldIndex) newIndex -= 1;
                    final item = _sessionPages.removeAt(oldIndex);
                    _sessionPages.insert(newIndex, item);
                  });
                },
                itemBuilder: (context, index) {
                  final page = _sessionPages[index];
                  return Container(
                    key: ValueKey(page.id),
                    width: 88,
                    margin: const EdgeInsets.only(right: 8),
                    decoration: BoxDecoration(
                      border: Border.all(color: const Color(0xFFDC143C)),
                      borderRadius: BorderRadius.circular(8),
                    ),
                    child: Stack(
                      fit: StackFit.expand,
                      children: [
                        GestureDetector(
                          onTap: () async {
                            final updated = await Navigator.push<ScannedPage>(
                              context,
                              MaterialPageRoute(
                                builder: (_) => CropFilterScreen(page: page),
                              ),
                            );
                            if (updated != null && mounted) setState(() {});
                          },
                          child: ClipRRect(
                            borderRadius: BorderRadius.circular(7),
                            child: Image.file(
                              File(page.processedImagePath),
                              key: ValueKey(page.processedImagePath),
                              fit: BoxFit.cover,
                            ),
                          ),
                        ),
                        Positioned(
                          top: 2,
                          left: 4,
                          child: CircleAvatar(
                            radius: 10,
                            backgroundColor: Colors.black87,
                            child: Text(
                              '${index + 1}',
                              style: const TextStyle(fontSize: 10, color: Colors.white),
                            ),
                          ),
                        ),
                        Positioned(
                          top: 0,
                          right: 0,
                          child: InkWell(
                            onTap: () => setState(() => _sessionPages.removeAt(index)),
                            child: const CircleAvatar(
                              radius: 11,
                              backgroundColor: Color(0xFFDC143C),
                              child: Icon(Icons.close, size: 13, color: Colors.white),
                            ),
                          ),
                        ),
                        Positioned(
                          bottom: 2,
                          right: 2,
                          child: InkWell(
                            onTap: () => _captureFromCamera(replaceIndex: index),
                            child: const CircleAvatar(
                              radius: 11,
                              backgroundColor: Colors.black87,
                              child: Icon(Icons.refresh, size: 13, color: Colors.white),
                            ),
                          ),
                        ),
                      ],
                    ),
                  );
                },
              ),
            ),
          Container(
            padding: const EdgeInsets.symmetric(horizontal: 24, vertical: 14),
            color: const Color(0xFF0A0A0A),
            child: Row(
              mainAxisAlignment: MainAxisAlignment.spaceAround,
              children: [
                IconButton.filledTonal(
                  tooltip: 'Import from Gallery',
                  icon: const Icon(Icons.photo_library_outlined),
                  onPressed: _isBusy ? null : _importFromGallery,
                ),
                GestureDetector(
                  onTap: _isBusy ? null : () => _captureFromCamera(),
                  child: Container(
                    width: 68,
                    height: 68,
                    decoration: BoxDecoration(
                      shape: BoxShape.circle,
                      border: Border.all(color: Colors.white, width: 3),
                      color: const Color(0xFFDC143C),
                    ),
                    child: const Icon(Icons.camera_alt, color: Colors.white, size: 30),
                  ),
                ),
                IconButton.filledTonal(
                  tooltip: 'Edit Last Page',
                  icon: const Icon(Icons.tune),
                  onPressed: _sessionPages.isEmpty
                      ? null
                      : () async {
                          final updated = await Navigator.push<ScannedPage>(
                            context,
                            MaterialPageRoute(
                              builder: (_) => CropFilterScreen(page: _sessionPages.last),
                            ),
                          );
                          if (updated != null && mounted) setState(() {});
                        },
                ),
              ],
            ),
          ),
        ],
      ),
    );
  }
}
