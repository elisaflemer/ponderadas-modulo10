// screens/login_screen.dart
import 'package:flutter/material.dart';
import 'package:todoapp/controllers/login_controller.dart';
import 'package:todoapp/widgets/custom_text_field.dart';

class LoginScreen extends StatefulWidget {
  const LoginScreen({super.key});

  @override
  State<LoginScreen> createState() => LoginScreenState();
}

class LoginScreenState extends State<LoginScreen> {
  final LoginController _controller = LoginController();

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Login'),
      ),
      body: Center(
        child: Column(
          children: <Widget>[
            Padding(
              padding: const EdgeInsets.all(8.0),
              child: CustomTextField(
                controller: _controller.emailController,
                labelText: 'Digite seu email',
              ),
            ),
            Padding(
              padding: const EdgeInsets.all(8.0),
              child: CustomTextField(
                controller: _controller.passwordController,
                labelText: 'Digite sua senha',
                obscureText: true,
              ),
            ),
            ElevatedButton(
              onPressed: () async {
                await _controller.login(context);
              },
              child: const Text("Entrar"),
            ),
            ElevatedButton(
              onPressed: () {
                Navigator.pushNamed(context, '/signup');
              },
              child: const Text("Cadastrar"),
              style: ElevatedButton.styleFrom(
                backgroundColor: Colors.green,
                textStyle: const TextStyle(fontSize: 16),
              ),
            ),
          ],
        ),
      ),
    );
  }
}