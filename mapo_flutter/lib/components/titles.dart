import 'package:flutter/material.dart';

// Este archivo es para cualquier preset que se haga relacionado con texto, ya sean títulos, subtítulos, párrafos, etc.

class MainTitles extends StatelessWidget {
  final String text;
  const MainTitles({
    super.key,
    required this.text,
  });

  @override
  Widget build(BuildContext context) {
    return Padding(
      padding: const EdgeInsets.symmetric(horizontal: 25),
      child: Text(
        text,
        textAlign: TextAlign.center,
        style: Theme.of(context).textTheme.headlineLarge,
      ),
    );
  }
}

class SecondaryTitles extends StatelessWidget {
  final String text;
  const SecondaryTitles({
    super.key,
    required this.text,
  });

  @override
  Widget build(BuildContext context) {
    return Padding(
      padding: const EdgeInsets.symmetric(horizontal: 25),
      child: Text(
        text,
        textAlign: TextAlign.center,
        style: Theme.of(context).textTheme.headlineMedium,
      ),
    );
  }
}