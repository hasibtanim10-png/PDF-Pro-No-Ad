import 'package:flutter/material.dart';
import 'package:pdfrx/pdfrx.dart';
import 'package:provider/provider.dart';
import 'package:share_plus/share_plus.dart';
import '../converters/pdf_converter_service.dart';
import '../l10n/app_localizations.dart';
import '../models/bookmark_item.dart';
import '../models/pdf_document_item.dart';
import '../providers/app_provider.dart';
import '../screens/converter_screen.dart';

class PdfReaderScreen extends StatefulWidget {
  final PdfDocumentItem documentItem;
  final int initialPage;

  const PdfReaderScreen({
    super.key,
    required this.documentItem,
    this.initialPage = 1,
  });

  @override
  State<PdfReaderScreen> createState() => _PdfReaderScreenState();
}

class _PdfReaderScreenState extends State<PdfReaderScreen> {
  late PdfDocumentItem _doc;
  final PdfViewerController _controller = PdfViewerController();
  late final PdfTextSearcher _textSearcher;

  int _currentPage = 1;
  int _totalPages = 0;
  bool _fitPageMode = false;
  bool _showSearchBar = false;
  final TextEditingController _searchCtrl = TextEditingController();

  @override
  void initState() {
    super.initState();
    _doc = widget.documentItem;
    _currentPage = widget.initialPage;
    _textSearcher = PdfTextSearcher(_controller)..addListener(_onSearchChanged);
  }

  void _onSearchChanged() {
    if (mounted) setState(() {});
  }

  @override
  void dispose() {
    _textSearcher.removeListener(_onSearchChanged);
    _textSearcher.dispose();
    _searchCtrl.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    final l10n = AppLocalizations.of(context);

    return Scaffold(
      backgroundColor: Colors.black,
      appBar: AppBar(
        backgroundColor: const Color(0xFF0A0A0A),
        title: Text(
          _doc.name,
          maxLines: 1,
          overflow: TextOverflow.ellipsis,
          style: const TextStyle(fontSize: 16),
        ),
        actions: [
          IconButton(
            tooltip: 'Search text',
            icon: Icon(_showSearchBar ? Icons.search_off : Icons.search),
            onPressed: () {
              setState(() {
                _showSearchBar = !_showSearchBar;
                if (!_showSearchBar) {
                  _searchCtrl.clear();
                  _textSearcher.resetTextSearch();
                }
              });
            },
          ),
          IconButton(
            tooltip: _fitPageMode ? 'Fit to Width' : 'Fit to Page',
            icon: Icon(_fitPageMode ? Icons.fit_screen : Icons.width_full_outlined),
            onPressed: _toggleFitMode,
          ),
          PopupMenuButton<String>(
            icon: const Icon(Icons.more_vert),
            color: const Color(0xFF161616),
            onSelected: (value) => _handleMenuAction(value, l10n),
            itemBuilder: (_) => [
              PopupMenuItem(value: 'share', child: Text(l10n.share)),
              PopupMenuItem(value: 'bookmark', child: Text(l10n.bookmark)),
              PopupMenuItem(value: 'rename', child: Text(l10n.rename)),
              PopupMenuItem(value: 'jpg', child: Text(l10n.convertToJpg)),
              PopupMenuItem(value: 'png', child: Text(l10n.convertToPng)),
              PopupMenuItem(
                value: 'delete',
                child: Text(l10n.delete, style: const TextStyle(color: Color(0xFFDC143C))),
              ),
            ],
          ),
        ],
      ),
      body: Column(
        children: [
          if (_showSearchBar) _buildSearchBanner(),
          Expanded(
            child: Stack(
              children: [
                PdfViewer.file(
                  _doc.path,
                  controller: _controller,
                  params: PdfViewerParams(
                    backgroundColor: Colors.black,
                    maxScale: 6.0,
                    minScale: 0.5,
                    pagePaintCallbacks: [
                      _textSearcher.pageTextMatchPaintCallback,
                    ],
                    onPageChanged: (pageNumber) {
                      if (pageNumber != null && mounted) {
                        setState(() => _currentPage = pageNumber);
                      }
                    },
                    onViewerReady: (document, controller) {
                      if (mounted) {
                        setState(() => _totalPages = document.pages.length);
                      }
                      if (widget.initialPage > 1 &&
                          widget.initialPage <= document.pages.length) {
                        controller.goToPage(pageNumber: widget.initialPage);
                      }
                    },
                  ),
                ),
                Positioned(
                  bottom: 16,
                  left: 16,
                  right: 16,
                  child: _buildPageHud(),
                ),
              ],
            ),
          ),
        ],
      ),
    );
  }

  Widget _buildSearchBanner() {
    final matches = _textSearcher.matches.length;
    final currentIdx = _textSearcher.currentIndex;

    return Container(
      color: const Color(0xFF141414),
      padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 6),
      child: Row(
        children: [
          Expanded(
            child: TextField(
              controller: _searchCtrl,
              autofocus: true,
              decoration: const InputDecoration(
                hintText: 'Find text in PDF...',
                isDense: true,
                border: OutlineInputBorder(),
              ),
              onChanged: (q) => _textSearcher.startTextSearch(q, caseInsensitive: true),
            ),
          ),
          const SizedBox(width: 8),
          Text(
            matches == 0 ? '0/0' : '${(currentIdx ?? 0) + 1}/$matches',
            style: const TextStyle(fontSize: 12, color: Colors.white70),
          ),
          IconButton(
            icon: const Icon(Icons.keyboard_arrow_up),
            onPressed: matches > 0 ? () => _textSearcher.goToPrevMatch() : null,
          ),
          IconButton(
            icon: const Icon(Icons.keyboard_arrow_down),
            onPressed: matches > 0 ? () => _textSearcher.goToNextMatch() : null,
          ),
        ],
      ),
    );
  }

  Widget _buildPageHud() {
    return Center(
      child: Container(
        padding: const EdgeInsets.symmetric(horizontal: 14, vertical: 6),
        decoration: BoxDecoration(
          color: const Color(0xFF121212).withValues(alpha: 0.92),
          borderRadius: BorderRadius.circular(24),
          border: Border.all(color: const Color(0xFFDC143C).withValues(alpha: 0.6)),
        ),
        child: Row(
          mainAxisSize: MainAxisSize.min,
          children: [
            IconButton(
              icon: const Icon(Icons.chevron_left, size: 20),
              constraints: const BoxConstraints(),
              padding: const EdgeInsets.all(4),
              onPressed: _currentPage > 1
                  ? () => _controller.goToPage(pageNumber: _currentPage - 1)
                  : null,
            ),
            InkWell(
              onTap: _promptJumpToPage,
              child: Padding(
                padding: const EdgeInsets.symmetric(horizontal: 10),
                child: Text(
                  'Page $_currentPage of ${_totalPages == 0 ? '?' : _totalPages}',
                  style: const TextStyle(fontWeight: FontWeight.w600, fontSize: 13),
                ),
              ),
            ),
            IconButton(
              icon: const Icon(Icons.chevron_right, size: 20),
              constraints: const BoxConstraints(),
              padding: const EdgeInsets.all(4),
              onPressed: _currentPage < _totalPages
                  ? () => _controller.goToPage(pageNumber: _currentPage + 1)
                  : null,
            ),
            const SizedBox(width: 8),
            IconButton(
              tooltip: 'Bookmark current page',
              icon: const Icon(Icons.bookmark_add_outlined, color: Color(0xFFDC143C), size: 20),
              constraints: const BoxConstraints(),
              padding: const EdgeInsets.all(4),
              onPressed: _bookmarkCurrentPage,
            ),
          ],
        ),
      ),
    );
  }

  void _toggleFitMode() {
    setState(() => _fitPageMode = !_fitPageMode);
    if (_controller.isReady) {
      _controller.setZoom(
        _controller.centerPosition,
        _fitPageMode ? 0.85 : 1.0,
      );
    }
  }

  Future<void> _promptJumpToPage() async {
    if (_totalPages <= 1) return;
    final ctrl = TextEditingController(text: '$_currentPage');
    final page = await showDialog<int>(
      context: context,
      builder: (ctx) => AlertDialog(
        backgroundColor: const Color(0xFF141414),
        title: Text('Jump to Page (1–$_totalPages)'),
        content: TextField(
          controller: ctrl,
          keyboardType: TextInputType.number,
          autofocus: true,
        ),
        actions: [
          TextButton(onPressed: () => Navigator.pop(ctx), child: const Text('Cancel')),
          FilledButton(
            onPressed: () => Navigator.pop(ctx, int.tryParse(ctrl.text)),
            child: const Text('Go'),
          ),
        ],
      ),
    );
    if (page != null && page >= 1 && page <= _totalPages) {
      _controller.goToPage(pageNumber: page);
    }
  }

  Future<void> _bookmarkCurrentPage() async {
    final provider = context.read<AppProvider>();
    await provider.addBookmark(
      BookmarkItem(
        filePath: _doc.path,
        fileName: _doc.name,
        pageNumber: _currentPage,
        label: 'Page $_currentPage',
        createdAt: DateTime.now(),
      ),
    );
    if (mounted) {
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content: Text('Bookmarked Page $_currentPage of ${_doc.name}')),
      );
    }
  }

  Future<void> _handleMenuAction(String action, AppLocalizations l10n) async {
    final provider = context.read<AppProvider>();

    switch (action) {
      case 'share':
        await Share.shareXFiles([XFile(_doc.path)], text: _doc.name);

      case 'bookmark':
        await _bookmarkCurrentPage();

      case 'rename':
        final ctrl = TextEditingController(
          text: _doc.name.replaceAll(RegExp(r'\.pdf$', caseSensitive: false), ''),
        );
        final newName = await showDialog<String>(
          context: context,
          builder: (ctx) => AlertDialog(
            backgroundColor: const Color(0xFF141414),
            title: Text(l10n.rename),
            content: TextField(controller: ctrl, autofocus: true),
            actions: [
              TextButton(onPressed: () => Navigator.pop(ctx), child: Text(l10n.cancel)),
              FilledButton(
                onPressed: () => Navigator.pop(ctx, ctrl.text),
                child: Text(l10n.save),
              ),
            ],
          ),
        );
        if (newName != null && newName.trim().isNotEmpty) {
          final updatedPath = await provider.fileService.renamePdf(_doc.path, newName);
          if (updatedPath != null && mounted) {
            setState(() {
              _doc = PdfDocumentItem(
                path: updatedPath,
                name: updatedPath.split('/').last,
                sizeBytes: _doc.sizeBytes,
                modifiedAt: DateTime.now(),
              );
            });
            await provider.refreshAll();
          }
        }

      case 'jpg':
        if (!mounted) return;
        Navigator.push(
          context,
          MaterialPageRoute(
            builder: (_) => ConverterScreen(
              initialMode: ConverterMode.pdfToImage,
              preselectedPdfPath: _doc.path,
              initialFormat: OutputImageFormat.jpg,
            ),
          ),
        );

      case 'png':
        if (!mounted) return;
        Navigator.push(
          context,
          MaterialPageRoute(
            builder: (_) => ConverterScreen(
              initialMode: ConverterMode.pdfToImage,
              preselectedPdfPath: _doc.path,
              initialFormat: OutputImageFormat.png,
            ),
          ),
        );

      case 'delete':
        final confirmed = await showDialog<bool>(
          context: context,
          builder: (ctx) => AlertDialog(
            backgroundColor: const Color(0xFF141414),
            title: Text(l10n.delete),
            content: Text('Move "${_doc.name}" to Recycle Bin?'),
            actions: [
              TextButton(
                onPressed: () => Navigator.pop(ctx, false),
                child: Text(l10n.cancel),
              ),
              FilledButton(
                onPressed: () => Navigator.pop(ctx, true),
                child: Text(l10n.confirm),
              ),
            ],
          ),
        );
        if (confirmed == true) {
          await provider.fileService.moveToBin(_doc);
          await provider.refreshAll();
          if (mounted) Navigator.pop(context);
        }
    }
  }
}
