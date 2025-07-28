import 'package:flutter/material.dart';

// Esto es para cualquier entrada de texto que se haga

class UserPass extends StatefulWidget {
  final controller;
  final String field_indicator;
  final bool obscureText;
  const UserPass({
    super.key,
    required this.controller,
    required this.field_indicator,
    required this.obscureText
  });

  @override
  State<UserPass> createState() => _UserPassState();

}

class _UserPassState extends State<UserPass> {
  late bool _obscure;

  @override
  void initState() {
    super.initState();
    _obscure = widget.obscureText;
  }


  @override
  Widget build(BuildContext context) {
    return Padding(
      padding: const EdgeInsets.symmetric(horizontal: 25),
      child: TextField(
        controller: widget.controller,
        obscureText: _obscure,
        decoration: InputDecoration(
          enabledBorder: OutlineInputBorder(
            borderSide: BorderSide(color: Theme.of(context).colorScheme.primary),
          ),
          focusedBorder: OutlineInputBorder(
            borderSide: BorderSide(color: Theme.of(context).colorScheme.secondary)
          ),
          fillColor: Colors.white,
          filled: true,
          hintText: widget.field_indicator,
          suffixIcon: widget.field_indicator.toLowerCase().contains('contraseña')
            ? IconButton(
              icon: Icon(
                _obscure ? Icons.visibility_off : Icons.visibility,
              ),
              onPressed: () {
                setState(() {
                  _obscure = !_obscure;
                });
              },
            )
            : null
        ),
      ),
    );
  }
}