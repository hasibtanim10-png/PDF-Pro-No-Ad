class BookmarkItem {
  final int? id;
  final String filePath;
  final String fileName;
  final int? pageNumber;
  final String? label;
  final DateTime createdAt;

  const BookmarkItem({
    this.id,
    required this.filePath,
    required this.fileName,
    this.pageNumber,
    this.label,
    required this.createdAt,
  });

  bool get isPageBookmark => pageNumber != null;

  Map<String, dynamic> toMap() => {
        'id': id,
        'file_path': filePath,
        'file_name': fileName,
        'page_number': pageNumber,
        'label': label,
        'created_at': createdAt.toIso8601String(),
      };

  factory BookmarkItem.fromMap(Map<String, dynamic> map) => BookmarkItem(
        id: map['id'] as int?,
        filePath: map['file_path'] as String,
        fileName: map['file_name'] as String,
        pageNumber: map['page_number'] as int?,
        label: map['label'] as String?,
        createdAt: DateTime.tryParse(map['created_at'] as String? ?? '') ??
            DateTime.now(),
      );
}
