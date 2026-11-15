import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import '../l10n/app_localizations.dart';
import '../models/pdf_document_item.dart';
import '../providers/app_provider.dart';
import '../widgets/pdf_list_tile.dart';

class DocumentsScreen extends StatelessWidget {
  const DocumentsScreen({super.key});

  @override
  Widget build(BuildContext context) {
    final l10n = AppLocalizations.of(context);
    final provider = context.watch<AppProvider>();
    final docs = provider.filteredDocuments;

    return Column(
      children: [
        Padding(
          padding: const EdgeInsets.fromLTRB(14, 10, 14, 6),
          child: Row(
            children: [
              Expanded(
                child: TextField(
                  onChanged: provider.setSearchQuery,
                  decoration: InputDecoration(
                    hintText: l10n.searchHint,
                    prefixIcon: const Icon(Icons.search),
                    filled: true,
                    fillColor: const Color(0xFF121212),
                    isDense: true,
                    border: OutlineInputBorder(
                      borderRadius: BorderRadius.circular(12),
                      borderSide: BorderSide.none,
                    ),
                  ),
                ),
              ),
              const SizedBox(width: 8),
              PopupMenuButton<SortField>(
                tooltip: l10n.sortBy,
                icon: const Icon(Icons.sort_rounded),
                color: const Color(0xFF161616),
                onSelected: provider.setSort,
                itemBuilder: (_) => [
                  PopupMenuItem(value: SortField.name, child: Text(l10n.sortName)),
                  PopupMenuItem(value: SortField.date, child: Text(l10n.sortDate)),
                  PopupMenuItem(value: SortField.size, child: Text(l10n.sortSize)),
                ],
              ),
            ],
          ),
        ),
        Padding(
          padding: const EdgeInsets.symmetric(horizontal: 14, vertical: 4),
          child: Row(
            children: [
              Expanded(
                child: OutlinedButton.icon(
                  icon: const Icon(Icons.create_new_folder_outlined, size: 18),
                  label: Text(l10n.addFolder),
                  onPressed: () async {
                    await provider.fileService.authorizeNewFolder();
                    await provider.refreshAll();
                  },
                ),
              ),
              const SizedBox(width: 8),
              Expanded(
                child: OutlinedButton.icon(
                  icon: const Icon(Icons.file_open_outlined, size: 18),
                  label: Text(l10n.openPdf),
                  onPressed: () async {
                    await provider.fileService.importExternalPdfs();
                    await provider.refreshAll();
                  },
                ),
              ),
            ],
          ),
        ),
        Expanded(
          child: RefreshIndicator(
            color: const Color(0xFFDC143C),
            onRefresh: provider.refreshAll,
            child: docs.isEmpty
                ? ListView(
                    children: [
                      const SizedBox(height: 80),
                      Center(
                        child: Padding(
                          padding: const EdgeInsets.all(24),
                          child: Text(
                            l10n.noDocuments,
                            textAlign: TextAlign.center,
                            style: const TextStyle(color: Colors.white60),
                          ),
                        ),
                      ),
                    ],
                  )
                : ListView.builder(
                    itemCount: docs.length,
                    itemBuilder: (_, index) => PdfListTile(item: docs[index]),
                  ),
          ),
        ),
      ],
    );
  }
}
