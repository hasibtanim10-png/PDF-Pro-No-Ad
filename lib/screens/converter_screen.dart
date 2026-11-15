import 'dart:io';
import 'package:file_picker/file_picker.dart';
import 'package:flutter/material.dart';
import 'package:path/path.dart' as p;
import 'package:provider/provider.dart';
import 'package:share_plus/share_plus.dart';
import '../converters/pdf_converter_service.dart';
import '../providers/app_provider.dart';

enum ConverterMode { pdfToImage, imagesToPdf }

class ConverterScreen extends StatefulWidget {
  final ConverterMode initialMode;
  final String? preselectedPdfPath;
  final OutputImageFormat initialFormat;

  const ConverterScreen({
    super.key,
    required this.initialMode,
    this.preselectedPdfPath,
    this.initialFormat = OutputImageFormat.jpg,
  });

  @override
  State<ConverterScreen> createState() => _ConverterScreenState();
}

class _ConverterScreenState extends State<ConverterScreen> {
  final PdfConverterService _converter = PdfConverterService();
  late ConverterMode _mode;
  late OutputImageFormat _format;
  ConversionQuality _quality = ConversionQuality.high;

  String? _selectedPdfPath;
  int _pdfTotalPages = 0;
  bool _convertAllPages = true;
  final TextEditingController _pageRangeCtrl = TextEditingController(text: '1');

  final List<String> _selectedImages = [];
  final TextEditingController _outPdfNameCtrl = TextEditingController(text: 'Merged_Images');

  String? _customOutputFolder;
  bool _isConverting = false;
  String _progressText = '';
  List<String> _generatedFiles = [];

  @override
  void initState() {
    super.initState();
    _mode = widget.initialMode;
    _format = widget.initialFormat;
    if (widget.preselectedPdfPath != null) {
      _loadPdf(widget.preselectedPdfPath!);
    }
  }

  Future<void> _loadPdf(String path) async {
    final count = await _converter.getPageCount(path);
    if (mounted) {
      setState(() {
        _selectedPdfPath = path;
        _pdfTotalPages = count;
        _generatedFiles = [];
      });
    }
  }

  List<int> _parsePageSelection(String input, int maxPages) {
    final result = <int>{};
    for (final part in input.split(',')) {
      final trimmed = part.trim();
      if (trimmed.contains('-')) {
        final bounds = trimmed.split('-');
        if (bounds.length == 2) {
          final start = int.tryParse(bounds[0].trim()) ?? 1;
          final end = int.tryParse(bounds[1].trim()) ?? maxPages;
          for (int i = start; i <= end; i++) {
            if (i >= 1 && i <= maxPages) {
              result.add(i);
            }
          }
        }
      } else {
        final single = int.tryParse(trimmed);
        if (single != null && single >= 1 && single <= maxPages) {
          result.add(single);
        }
      }
    }
    return result.toList()..sort();
  }

  Future<void> _runConversion() async {
    setState(() {
      _isConverting = true;
      _generatedFiles = [];
    });
    try {
      if (_mode == ConverterMode.pdfToImage && _selectedPdfPath != null) {
        final pages = _convertAllPages
            ? null
            : _parsePageSelection(_pageRangeCtrl.text, _pdfTotalPages);
        final files = await _converter.convertPdfToImages(
          pdfPath: _selectedPdfPath!,
          format: _format,
          pages: pages,
          quality: _quality,
          outputFolder: _customOutputFolder,
          onProgress: (cur, tot) {
            if (mounted) {
              setState(() => _progressText = 'Rendering page $cur of $tot...');
            }
          },
        );
        if (mounted) setState(() => _generatedFiles = files);
      } else if (_mode == ConverterMode.imagesToPdf && _selectedImages.isNotEmpty) {
        final provider = context.read<AppProvider>();
        final outPdf = await _converter.convertImagesToPdf(
          imagePaths: _selectedImages,
          outputFileName: _outPdfNameCtrl.text,
          quality: _quality,
          outputFolder: _customOutputFolder,
          onProgress: (cur, tot) {
            if (mounted) {
              setState(() => _progressText = 'Embedding image $cur of $tot...');
            }
          },
        );
        await provider.refreshAll();
        if (mounted) setState(() => _generatedFiles = [outPdf]);
      }
    } finally {
      if (mounted) {
        setState(() {
          _isConverting = false;
          _progressText = '';
        });
      }
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: Colors.black,
      appBar: AppBar(
        backgroundColor: const Color(0xFF0A0A0A),
        title: Text(_mode == ConverterMode.pdfToImage ? 'PDF to Image' : 'Images to PDF'),
      ),
      body: ListView(
        padding: const EdgeInsets.all(16),
        children: [
          SegmentedButton<ConverterMode>(
            segments: const [
              ButtonSegment(value: ConverterMode.pdfToImage, label: Text('PDF → JPG/PNG')),
              ButtonSegment(value: ConverterMode.imagesToPdf, label: Text('Images → PDF')),
            ],
            selected: {_mode},
            onSelectionChanged: (s) => setState(() {
              _mode = s.first;
              _generatedFiles = [];
            }),
          ),
          const SizedBox(height: 16),
          if (_mode == ConverterMode.pdfToImage) ...[
            OutlinedButton.icon(
              icon: const Icon(Icons.picture_as_pdf),
              label: Text(
                _selectedPdfPath == null
                    ? 'Select Source PDF'
                    : '${p.basename(_selectedPdfPath!)} ($_pdfTotalPages pages)',
              ),
              onPressed: () async {
                final res = await FilePicker.platform.pickFiles(
                  type: FileType.custom,
                  allowedExtensions: ['pdf'],
                );
                if (res != null && res.files.single.path != null) {
                  await _loadPdf(res.files.single.path!);
                }
              },
            ),
            const SizedBox(height: 12),
            SegmentedButton<OutputImageFormat>(
              segments: const [
                ButtonSegment(value: OutputImageFormat.jpg, label: Text('JPG')),
                ButtonSegment(value: OutputImageFormat.png, label: Text('PNG')),
              ],
              selected: {_format},
              onSelectionChanged: (s) => setState(() => _format = s.first),
            ),
            SwitchListTile(
              title: const Text('Convert All Pages'),
              value: _convertAllPages,
              activeThumbColor: const Color(0xFFDC143C),
              onChanged: (v) => setState(() => _convertAllPages = v),
            ),
            if (!_convertAllPages)
              TextField(
                controller: _pageRangeCtrl,
                decoration: const InputDecoration(
                  labelText: 'Selected Pages (e.g. 1, 3-5)',
                  border: OutlineInputBorder(),
                ),
              ),
          ] else ...[
            OutlinedButton.icon(
              icon: const Icon(Icons.add_photo_alternate),
              label: Text('Select Images (${_selectedImages.length} selected)'),
              onPressed: () async {
                final res = await FilePicker.platform.pickFiles(
                  type: FileType.image,
                  allowMultiple: true,
                );
                if (res != null) {
                  setState(() {
                    _selectedImages.addAll(
                      res.files.where((f) => f.path != null).map((f) => f.path!),
                    );
                  });
                }
              },
            ),
            const SizedBox(height: 12),
            TextField(
              controller: _outPdfNameCtrl,
              decoration: const InputDecoration(
                labelText: 'Output PDF Name',
                border: OutlineInputBorder(),
              ),
            ),
          ],
          const SizedBox(height: 12),
          DropdownButtonFormField<ConversionQuality>(
            initialValue: _quality,
            decoration: const InputDecoration(
              labelText: 'Output Quality',
              border: OutlineInputBorder(),
            ),
            items: ConversionQuality.values
                .map((q) => DropdownMenuItem(value: q, child: Text(q.label)))
                .toList(),
            onChanged: (q) {
              if (q != null) setState(() => _quality = q);
            },
          ),
          const SizedBox(height: 12),
          OutlinedButton.icon(
            icon: const Icon(Icons.folder_open),
            label: Text(
              _customOutputFolder == null
                  ? 'Output Folder: Default (PDFProConverted)'
                  : 'Output: $_customOutputFolder',
              maxLines: 1,
              overflow: TextOverflow.ellipsis,
            ),
            onPressed: () async {
              final dir = await FilePicker.platform.getDirectoryPath();
              if (dir != null) setState(() => _customOutputFolder = dir);
            },
          ),
          const SizedBox(height: 18),
          FilledButton.icon(
            icon: const Icon(Icons.bolt),
            label: Text(_isConverting ? _progressText : 'Start Conversion'),
            onPressed: _isConverting ? null : _runConversion,
          ),
          if (_generatedFiles.isNotEmpty) ...[
            const SizedBox(height: 20),
            Row(
              mainAxisAlignment: MainAxisAlignment.spaceBetween,
              children: [
                Text(
                  'Converted Files (${_generatedFiles.length})',
                  style: const TextStyle(fontWeight: FontWeight.bold, fontSize: 16),
                ),
                FilledButton.tonalIcon(
                  icon: const Icon(Icons.share),
                  label: const Text('Share All'),
                  onPressed: () => Share.shareXFiles(
                    _generatedFiles.map((path) => XFile(path)).toList(),
                  ),
                ),
              ],
            ),
            const SizedBox(height: 10),
            _selectedPdfPath == null
                    ? 'Select Source PDF'
                    : '${p.basename(_selectedPdfPath!)} ($_pdfTotalPages pages)',
              ),
              onPressed: () async {
                final res = await FilePicker.platform.pickFiles(
                  type: FileType.custom,
                  allowedExtensions: ['pdf'],
                );
                if (res != null && res.files.single.path != null) {
                  await _loadPdf(res.files.single.path!);
                }
              },
            ),
            const SizedBox(height: 12),
            SegmentedButton<OutputImageFormat>(
              segments: const [
                ButtonSegment(value: OutputImageFormat.jpg, label: Text('JPG')),
                ButtonSegment(value: OutputImageFormat.png, label: Text('PNG')),
              ],
              selected: {_format},
              onSelectionChanged: (s) => setState(() => _format = s.first),
            ),
            SwitchListTile(
              title: const Text('Convert All Pages'),
              value: _convertAllPages,
              activeThumbColor: const Color(0xFFDC143C),
              onChanged: (v) => setState(() => _convertAllPages = v),
            ),
            if (!_convertAllPages)
              TextField(
                controller: _pageRangeCtrl,
                decoration: const InputDecoration(
                  labelText: 'Selected Pages (e.g. 1, 3-5)',
                  border: OutlineInputBorder(),
                ),
              ),
          ] else ...[
            OutlinedButton.icon(
              icon: const Icon(Icons.add_photo_alternate),
              label: Text('Select Images (${_selectedImages.length} selected)'),
              onPressed: () async {
                final res = await FilePicker.platform.pickFiles(
                  type: FileType.image,
                  allowMultiple: true,
                );
                if (res != null) {
                  setState(() {
                    _selectedImages.addAll(
                      res.files.where((f) => f.path != null).map((f) => f.path!),
                    );
                  });
                }
              },
            ),
            const SizedBox(height: 12),
            TextField(
              controller: _outPdfNameCtrl,
              decoration: const InputDecoration(
                labelText: 'Output PDF Name',
                border: OutlineInputBorder(),
              ),
            ),
          ],
          const SizedBox(height: 12),
          DropdownButtonFormField<ConversionQuality>(
            initialValue: _quality,
            decoration: const InputDecoration(
              labelText: 'Output Quality',
              border: OutlineInputBorder(),
            ),
            items: ConversionQuality.values
                .map((q) => DropdownMenuItem(value: q, child: Text(q.label)))
                .toList(),
            onChanged: (q) {
              if (q != null) setState(() => _quality = q);
            },
          ),
          const SizedBox(height: 12),
          OutlinedButton.icon(
            icon: const Icon(Icons.folder_open),
            label: Text(
              _customOutputFolder == null
                  ? 'Output Folder: Default (PDFProConverted)'
                  : 'Output: $_customOutputFolder',
              maxLines: 1,
              overflow: TextOverflow.ellipsis,
            ),
            onPressed: () async {
              final dir = await FilePicker.platform.getDirectoryPath();
              if (dir != null) setState(() => _customOutputFolder = dir);
            },
          ),
          const SizedBox(height: 18),
          FilledButton.icon(
            icon: const Icon(Icons.bolt),
            label: Text(_isConverting ? _progressText : 'Start Conversion'),
            onPressed: _isConverting ? null : _runConversion,
          ),
          if (_generatedFiles.isNotEmpty) ...[
            const SizedBox(height: 20),
            Row(
              mainAxisAlignment: MainAxisAlignment.spaceBetween,
              children: [
                Text(
                  'Converted Files (${_generatedFiles.length})',
                  style: const TextStyle(fontWeight: FontWeight.bold, fontSize: 16),
                ),
                FilledButton.tonalIcon(
                  icon: const Icon(Icons.share),
                  label: const Text('Share All'),
                  onPressed: () => Share.shareXFiles(
                    _generatedFiles.map((path) => XFile(path)).toList(),
                  ),
                ),
              ],
            ),
            const SizedBox(height: 10),
            ..._generatedFiles.map(
              (filePath) => Card(
                color: const Color(0xFF121212),
                child: ListTile(
                  leading: filePath.endsWith('.pdf')
                      ? const Icon(Icons.picture_as_pdf, color: Color(0xFFDC143C))
                      : Image.file(File(filePath), width: 44, height: 44, fit: BoxFit.cover),
                  title: Text(p.basename(filePath), maxLines: 1, overflow: TextOverflow.ellipsis),
                  trailing: IconButton(
                    icon: const Icon(Icons.share),
                    onPressed: () => Share.shareXFiles([XFile(filePath)]),
                  ),
                ),
              ),
            ),
          ],
        ],
      ),
    );
  }
}
