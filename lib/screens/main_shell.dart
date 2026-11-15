import 'package:flutter/material.dart';
import '../l10n/app_localizations.dart';
import 'bookmarks_screen.dart';
import 'documents_screen.dart';
import 'home_screen.dart';
import 'me_screen.dart';
import 'tools_screen.dart';

class MainShell extends StatefulWidget {
  const MainShell({super.key});

  @override
  State<MainShell> createState() => _MainShellState();
}

class _MainShellState extends State<MainShell> {
  int _currentIndex = 0;

  final List<Widget> _screens = const [
    HomeScreen(),
    DocumentsScreen(),
    ToolsScreen(),
    MeScreen(),
    BookmarksScreen(),
  ];

  @override
  Widget build(BuildContext context) {
    final l10n = AppLocalizations.of(context);

    return Scaffold(
      appBar: AppBar(
        backgroundColor: Colors.black,
        title: Row(
          children: [
            Container(
              padding: const EdgeInsets.all(6),
              decoration: BoxDecoration(
                color: const Color(0xFFDC143C),
                borderRadius: BorderRadius.circular(8),
              ),
              child: const Icon(Icons.picture_as_pdf, color: Colors.white, size: 18),
            ),
            const SizedBox(width: 10),
            Text(
              l10n.appName,
              style: const TextStyle(fontWeight: FontWeight.w800, letterSpacing: 0.3),
            ),
          ],
        ),
      ),
      body: IndexedStack(
        index: _currentIndex,
        children: _screens,
      ),
      bottomNavigationBar: NavigationBar(
        selectedIndex: _currentIndex,
        backgroundColor: const Color(0xFF080808),
        indicatorColor: const Color(0xFFDC143C).withValues(alpha: 0.24),
        onDestinationSelected: (idx) => setState(() => _currentIndex = idx),
        destinations: [
          NavigationDestination(
            icon: const Icon(Icons.home_outlined),
            selectedIcon: const Icon(Icons.home, color: Color(0xFFDC143C)),
            label: l10n.home,
          ),
          NavigationDestination(
            icon: const Icon(Icons.folder_copy_outlined),
            selectedIcon: const Icon(Icons.folder_copy, color: Color(0xFFDC143C)),
            label: l10n.documents,
          ),
          NavigationDestination(
            icon: const Icon(Icons.grid_view_outlined),
            selectedIcon: const Icon(Icons.grid_view_rounded, color: Color(0xFFDC143C)),
            label: l10n.tools,
          ),
          NavigationDestination(
            icon: const Icon(Icons.person_outline),
            selectedIcon: const Icon(Icons.person, color: Color(0xFFDC143C)),
            label: l10n.me,
          ),
          NavigationDestination(
            icon: const Icon(Icons.bookmarks_outlined),
            selectedIcon: const Icon(Icons.bookmarks, color: Color(0xFFDC143C)),
            label: l10n.bookmarks,
          ),
        ],
      ),
    );
  }
}
