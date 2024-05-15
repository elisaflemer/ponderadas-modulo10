import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';
import '../widgets/task_tile.dart';

class TodoListScreen extends StatefulWidget {
  @override
  _TodoListScreenState createState() => _TodoListScreenState();
}

class _TodoListScreenState extends State<TodoListScreen> {
  List tasks = [];

  @override
  void initState() {
    super.initState();
    fetchTasks();
  }

  Future<void> fetchTasks() async {
    final response = await http.get(Uri.parse('http://localhost:8000/api/v1/tasks'));

    if (response.statusCode == 200) {
      setState(() {
        tasks = json.decode(response.body);
      });
    } else {
      throw Exception('Failed to load tasks');
    }
  }

  Future<void> _addTask() async {
    final response = await http.post(
      Uri.parse('http://localhost:8000/api/v1/tasks'),
      headers: {'Content-Type': 'application/json'},
      body: json.encode({'title': 'New Task'}),
    );

    if (response.statusCode == 201) {
      setState(() {
        tasks.add(json.decode(response.body));
      });
    } else {
      throw Exception('Failed to add task');
    }
  }

  Future<void> _editTask(int index, String newTitle) async {
    final task = tasks[index];
    final response = await http.put(
      Uri.parse('http://localhost:8000/api/v1/tasks/${task['id']}'),
      headers: {'Content-Type': 'application/json'},
      body: json.encode({'title': newTitle}),
    );

    if (response.statusCode == 200) {
      setState(() {
        tasks[index]['title'] = newTitle;
      });
    } else {
      throw Exception('Failed to edit task');
    }
  }

  Future<void> _deleteTask(int index) async {
    final task = tasks[index];
    final response = await http.delete(
      Uri.parse('http://localhost:8000/api/v1/tasks/${task['id']}'),
    );

    if (response.statusCode == 200) {
      setState(() {
        tasks.removeAt(index);
      });
    } else {
      throw Exception('Failed to delete task');
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text('Todo List'),
      ),
      body: ListView.builder(
        itemCount: tasks.length,
        itemBuilder: (context, index) {
          return TaskTile(
            task: tasks[index],
            onEdit: (newTitle) => _editTask(index, newTitle),
            onDelete: () => _deleteTask(index),
          );
        },
      ),
      floatingActionButton: FloatingActionButton(
        onPressed: _addTask,
        child: Icon(Icons.add),
      ),
    );
  }
}
