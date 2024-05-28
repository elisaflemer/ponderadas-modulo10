// widgets/custom_text_field.dart
import 'package:flutter/material.dart';

class CustomTextField extends StatelessWidget {
  final TextEditingController controller;
  final String labelText;
  final bool obscureText;

  const CustomTextField({
    required this.controller,
    required this.labelText,
    this.obscureText = false,
    Key? key,
  }) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return TextField(
      controller: controller,
      decoration: InputDecoration(
        border: OutlineInputBorder(),
        labelText: labelText,
      ),
      obscureText: obscureText,
    );
  }
}