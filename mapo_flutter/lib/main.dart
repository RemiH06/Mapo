import 'package:flutter/material.dart';
import 'package:mapo_flutter/themes/light_theme.dart';
import 'pages/login_page.dart';

void main() {
  runApp(const MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Mapo',
      theme: AppTheme.lightTheme,
      home: LoginPage(),
    );
  }
}