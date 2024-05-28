// controllers/login_controller.dart
import 'package:flutter/material.dart';
import 'package:todoapp/models/user.dart';
import 'package:todoapp/services/api_service.dart';

class LoginController {
  final TextEditingController emailController = TextEditingController();
  final TextEditingController passwordController = TextEditingController();

  Future<void> login(BuildContext context) async {
    var user = User(email: emailController.text, password: passwordController.text);
    var response = await ApiService.login(user);

    if (response.statusCode == 200) {
      Navigator.pushNamed(context, '/camera');
    } else {
      print('Request failed with status: ${response.statusCode}.');
    }
  }
}