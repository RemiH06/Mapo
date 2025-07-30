import 'package:flutter/material.dart';
import 'package:mapo_flutter/components/titles.dart';
import 'package:mapo_flutter/components/entry_boxes.dart';
import 'dart:convert';
import 'package:flutter/services.dart' show rootBundle;
import 'package:mapo_flutter/pages/signup_page.dart';

class LoginPage extends StatefulWidget {
  LoginPage({super.key});

  @override
  State<LoginPage> createState() => _LoginPageState(); 

}

class _LoginPageState extends State<LoginPage> {
  // Controllers para usuario y contraseña
  final userController = TextEditingController();
  final passController = TextEditingController();

  Map<String, String> _users = {};
  String _message = '';

  @override
  void initState() {
    super.initState();
    _loadUsers();
  }

  Future<void> _loadUsers() async {
    final String jsonText = await rootBundle.loadString('assets/usuarios_fake.json');
    final Map<String, dynamic> jsonMap = json.decode(jsonText);
    setState(() {
      _users = jsonMap.map((key,value) => MapEntry(key, value.toString()));
    });
  }

  void _checkLogin() {
    String usuario = userController.text.trim();
    String password = passController.text.trim();

    if (_users.containsKey(usuario) && _users[usuario] == password) {
      setState(() {
        _message = 'Login Exitoso';
      });
    } else {
      setState(() {
        _message = 'Usuario o Contraseña Incorrecta :(';
      });
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: Column(mainAxisAlignment: MainAxisAlignment.center, children: [
        Icon(Icons.map, size: 50,),
        const SizedBox(height: 20),
        Center(child: MainTitles(text: 'Mapo'),),
        const SizedBox(height: 20),
        UserPass(controller: userController, field_indicator: 'usuario', obscureText: false),
        Divider(height: 20, thickness: 2, color: Theme.of(context).colorScheme.primary, indent: 25, endIndent: 25,),
        UserPass(controller: passController, field_indicator: 'contraseña', obscureText: true),
        const SizedBox(height: 20,),
        Row(mainAxisAlignment: MainAxisAlignment.center ,children: [
          ElevatedButton(onPressed: _checkLogin, child: const Icon(Icons.login)),
          const SizedBox(width: 10),
          ElevatedButton(
            onPressed: () {
              Navigator.push(context, MaterialPageRoute(builder: (context) => SignupPage()));
            }, 
            child: const Text('No te has registrado? Hazlo Aquí!'))
        ],),
        const SizedBox(height: 10),
        MainTitles(text: _message)
      ],),
    );
  }
}