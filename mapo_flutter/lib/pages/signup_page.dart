import 'package:flutter/material.dart';
import 'package:mapo_flutter/components/entry_boxes.dart';
import 'package:mapo_flutter/components/titles.dart';

class SignupPage extends StatefulWidget {
  SignupPage({super.key});

  @override
  State<SignupPage> createState() => _SignupPageState();
}

class _SignupPageState extends State<SignupPage> {
  final userController = TextEditingController();
  final passController = TextEditingController();
  final confirmController = TextEditingController();

  bool passwordCheck (String pwd) {
    final numRegex = RegExp(r'\d');
    final specialRegex = RegExp(r'[!@#\$%^&*(),.?":{}|<>]');
    return numRegex.hasMatch(pwd) && specialRegex.hasMatch(pwd);
  }

  String _message = '';

  void confirmPassword() {
    String user = userController.text.toLowerCase();
    String password = passController.text.trim();
    String pswd_2 = confirmController.text.trim();

    if (user == '') {
      setState(() {
        _message = 'El usuario no puede estar vacío';
      });

    } else if (!passwordCheck(password) || password.length < 8) {
      setState(() {
        _message = 'No cumples con los requerimientos de caracteres o de largo. Revísa tu contraseña de nuevo!';
      });
    } else if (password != pswd_2) {
      setState(() {
        _message = 'Las contraseñas no coinciden :(';
      });
    } else {
      setState(() {
        _message = 'Registro Exitoso!';
      });
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: Column(mainAxisAlignment: MainAxisAlignment.center, children: [
        Icon(Icons.abc, size: 50),
        const SizedBox(height: 10),
        Center(child: SecondaryTitles(text: 'Registrate a Mapo!')),
        const SizedBox(height: 10),
        UserPass(controller: userController, field_indicator: 'usuario', obscureText: false),
        const SizedBox(height: 10),
        UserPass(controller: passController, field_indicator: 'contraseña', obscureText: true),
        const SizedBox(height: 10),
        UserPass(controller: confirmController, field_indicator: 'repite contraseña', obscureText: true),
        Divider(height: 20, thickness: 2, color: Theme.of(context).colorScheme.primary, indent: 25, endIndent: 25,),
        ElevatedButton(onPressed: confirmPassword, child: const Text('Registrate')),
        const SizedBox(height: 10,),
        MainTitles(text: _message),
        ElevatedButton(onPressed: () {
          Navigator.pop(context);
        }, child: const Text('Regresa a Iniciar Sesión!'))

      ],),
    );
  }
}