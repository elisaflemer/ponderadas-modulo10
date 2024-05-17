import 'package:flutter/material.dart';
import 'package:flutter/widgets.dart';
import 'dart:convert';
import 'package:http/http.dart' as http;
import 'package:flutter_secure_storage/flutter_secure_storage.dart';


class LoginScreen extends StatefulWidget {
  const LoginScreen({super.key});

  @override
  State<LoginScreen> createState() => LoginScreenState();
}

class LoginScreenState extends State<LoginScreen> {
  TextEditingController _emailController = TextEditingController();
  TextEditingController _passwordController = TextEditingController();
  String catFact = '';

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
              child: TextField(
                controller: _emailController,
                decoration: const InputDecoration(
                  border: OutlineInputBorder(),
                  labelText: 'Digite seu email',
                ),
              ),
            ),
            Padding(
              padding: const EdgeInsets.all(8.0),
              child: TextField(
                controller: _passwordController,
                decoration: const InputDecoration(
                  border: OutlineInputBorder(),
                  labelText: 'Digite sua senha',
                ),
              ),
            ),
            Padding(
              padding: const EdgeInsets.all(8.0),
              child: Text(
              catFact,

                )
            ),
            ElevatedButton(
              onPressed: () async {
                print('Email: ${_emailController.text}');
               var url = Uri.parse('https://b2c5-187-180-189-147.ngrok-free.app/api/v1/users/login');
               print('URL: $url');
                var response = await http.post(
                  url,
                  headers: <String, String>{
                    'Content-Type': 'application/json; charset=UTF-8',
                  },
                  body: jsonEncode(<String, String>{
                    'email': _emailController.text,
                    'password': _passwordController.text,
                  }),
                );

                print('Response status: ${response.statusCode}');

                // To work with the output as JSON/Map
                if (response.statusCode == 200) { // HTTP OK

                  // Save the token in the secure storage
                  var storage = const FlutterSecureStorage();
                  var token = jsonDecode(response.body)['token'];
                  await storage.write(key: 'token', value: token);
                  

                  // Navigate to the next screen
                  Navigator.pushNamed(context, '/todo');
          
                } else {
                  // Handle error or non-200 responses
                  print('Request failed with status: ${response.statusCode}.');
                }
                          },
              child: const Text("Entrar"),
            ),
          ],
        ),
      ),
    );
  }
}