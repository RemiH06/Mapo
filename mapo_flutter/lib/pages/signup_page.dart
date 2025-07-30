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

  String _message = '';

  void confirm_password() {
    String password = passController.text.trim();
    String pswd_2 = confirmController.text.trim();

    if (password == pswd_2) {
      setState(() {
        _message = 'Registro Exitoso!';
      });
    } else {
      setState(() {
        _message = 'Las contraseñas no coinciden :(';
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
        ElevatedButton(onPressed: confirm_password, child: const Text('Registrate')),
        const SizedBox(height: 10,),
        MainTitles(text: _message),
        ElevatedButton(onPressed: () {
          Navigator.pop(context);
        }, child: const Text('Regresa a Iniciar Sesión!'))

      ],),
    );
  }
}