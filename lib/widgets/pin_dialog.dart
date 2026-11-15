import 'package:flutter/material.dart';

Future<String?> showPinPromptDialog(
  BuildContext context, {
  required String title,
  String? subtitle,
}) async {
  final controller = TextEditingController();
  return showDialog<String>(
    context: context,
    barrierDismissible: false,
    builder: (ctx) => AlertDialog(
      backgroundColor: const Color(0xFF121212),
      title: Text(title),
      content: Column(
        mainAxisSize: MainAxisSize.min,
        children: [
          if (subtitle != null) ...[
            Text(subtitle, style: const TextStyle(color: Colors.white70)),
            const SizedBox(height: 12),
          ],
          TextField(
            controller: controller,
            keyboardType: TextInputType.number,
            obscureText: true,
            maxLength: 6,
            autofocus: true,
            decoration: const InputDecoration(
              labelText: '4–6 Digit PIN',
              border: OutlineInputBorder(),
            ),
          ),
        ],
      ),
      actions: [
        TextButton(
          onPressed: () => Navigator.pop(ctx, null),
          child: const Text('Cancel'),
        ),
        FilledButton(
          onPressed: () {
            final text = controller.text.trim();
            if (text.length >= 4) {
              Navigator.pop(ctx, text);
            }
          },
          child: const Text('Confirm'),
        ),
      ],
    ),
  );
}
