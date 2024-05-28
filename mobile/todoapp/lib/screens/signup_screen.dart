// screens/signup_screen.dart
import 'package:flutter/material.dart';
import 'package:todoapp/controllers/signup_controller.dart';
import 'package:todoapp/widgets/custom_text_field.dart';

class SignUpScreen extends StatefulWidget {
  const SignUpScreen({super.key});

  @override
  State<SignUpScreen> createState() => SignUpScreenState();
}

class SignUpScreenState extends State<SignUpScreen> {
  final SignUpController _controller = SignUpController();

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Sign Up'),
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
            Padding(
              padding: const EdgeInsets.all(8.0),
              child: CustomTextField(
                controller: _controller.confirmPasswordController,
                labelText: 'Confirme sua senha',
                obscureText: true,
              ),
            ),
            ElevatedButton(
              onPressed: () async {
                await _controller.signUp(context);
              },
              child: const Text("Cadastrar"),
            ),
          ],
        ),
      ),
    );
  }
}