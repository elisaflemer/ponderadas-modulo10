import 'package:flutter/material.dart';

class TaskTile extends StatefulWidget {
  final Map task;
  final Function(String) onEdit;
  final Function onDelete;

  TaskTile({required this.task, required this.onEdit, required this.onDelete});

  @override
  _TaskTileState createState() => _TaskTileState();
}

class _TaskTileState extends State<TaskTile> {
  late TextEditingController _controller;

  @override
  void initState() {
    super.initState();
    _controller = TextEditingController(text: widget.task['title']);
  }

  @override
  Widget build(BuildContext context) {
    return ListTile(
      title: TextField(
        controller: _controller,
        onSubmitted: (newTitle) {
          widget.onEdit(newTitle);
        },
      ),
      trailing: IconButton(
        icon: Icon(Icons.delete),
        onPressed: () {
          widget.onDelete();
        },
      ),
    );
  }

  @override
  void dispose() {
    _controller.dispose();
    super.dispose();
  }
}
