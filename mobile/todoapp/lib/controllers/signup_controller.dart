// controllers/signup_controller.dart
import 'package:flutter/material.dart';
import 'package:todoapp/models/user.dart';
import 'package:todoapp/services/api_service.dart';

class SignUpController {
  final TextEditingController emailController = TextEditingController();
  final TextEditingController passwordController = TextEditingController();
  final TextEditingController confirmPasswordController = TextEditingController();

  Future<void> signUp(BuildContext context) async {
    if (passwordController.text != confirmPasswordController.text) {
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content: Text('Passwords do not match')),
      );
      return;
    }

    var user = User(email: emailController.text, password: passwordController.text);
    var response = await ApiService.register(user);

    if (response.statusCode == 200) {
      Navigator.pushNamed(context, '/login');
    } else {
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content: Text('Sign-up failed: ${response.body}')),
      );
    }
  }
}