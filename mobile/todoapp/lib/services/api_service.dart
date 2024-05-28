// services/api_service.dart
import 'dart:convert';
import 'package:http/http.dart' as http;
import 'package:flutter_secure_storage/flutter_secure_storage.dart';
import 'package:todoapp/constants/baseUrl.dart';
import 'package:todoapp/models/user.dart';

class ApiService {
  static const storage = FlutterSecureStorage();

  static Future<http.Response> login(User user) async {
    var url = Uri.parse(baseUrl + '/users/login');
    var response = await http.post(
      url,
      headers: <String, String>{
        'Content-Type': 'application/json; charset=UTF-8',
      },
      body: jsonEncode(user.toJson()),
    );

    if (response.statusCode == 200) {
      var token = jsonDecode(response.body)['access_token'];
      await storage.write(key: 'token', value: token);
    }

    return response;
  }

  static Future<http.Response> register(User user) async {
    var url = Uri.parse(baseUrl + '/users/register');
    var response = await http.post(
      url,
      headers: <String, String>{
        'Content-Type': 'application/json; charset=UTF-8',
      },
      body: jsonEncode(user.toJson()),
    );

    return response;
  }
}
