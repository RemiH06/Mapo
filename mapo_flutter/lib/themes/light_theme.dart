import 'package:flutter/material.dart';

// Este es un demo para un light theme que podamos usar
// Más abajo habría que incluir un theme para dark mode (creo que Flutter puede generarlos automáticamente en base a tu light theme pero igual no sé si quieran uno custom made)
class AppTheme {
  static final ThemeData lightTheme = ThemeData(
    brightness: Brightness.light,
    primaryColor: Color.fromARGB(255, 214, 212, 160),
    colorScheme: ColorScheme.fromSeed(
      seedColor: Color.fromARGB(255, 230, 170, 206),
      primary: Color.fromARGB(255, 214, 113, 160),
      secondary: Color.fromARGB(255, 158, 46, 113),
    ),
    scaffoldBackgroundColor: Color.fromARGB(255, 214, 212, 160),
    textTheme: const TextTheme(
      headlineLarge: TextStyle(fontSize: 56, fontWeight: FontWeight.w900),
      headlineMedium: TextStyle(fontSize: 32, fontWeight: FontWeight.normal),
      bodyMedium: TextStyle(fontSize: 16, fontWeight: FontWeight.w700),

    ),
    elevatedButtonTheme: ElevatedButtonThemeData(
      style: ElevatedButton.styleFrom(
        backgroundColor: Color.fromARGB(255, 102, 16, 242),
        foregroundColor: Color.fromARGB(255, 255, 255, 255),
      )
    )
  );
}