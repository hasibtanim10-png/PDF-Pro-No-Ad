class ManagedEntry {
  final int? id;
  final String originalPath;
  final String storedPath;
  final String fileName;
  final int sizeBytes;
  final DateTime movedAt;

  const ManagedEntry({
    this.id,
    required this.originalPath,
    required this.storedPath,
    required this.fileName,
    required this.sizeBytes,
    required this.movedAt,
  });

  Map<String, dynamic> toMap() => {
        'id': id,
        'original_path': originalPath,
        'stored_path': storedPath,
        'file_name': fileName,
        'size_bytes': sizeBytes,
        'moved_at': movedAt.toIso8601String(),
      };

  factory ManagedEntry.fromMap(Map<String, dynamic> map) => ManagedEntry(
        id: map['id'] as int?,
        originalPath: map['original_path'] as String,
        storedPath: map['stored_path'] as String,
        fileName: map['file_name'] as String,
        sizeBytes: map['size_bytes'] as int? ?? 0,
        movedAt: DateTime.tryParse(map['moved_at'] as String? ?? '') ??
            DateTime.now(),
      );
}
