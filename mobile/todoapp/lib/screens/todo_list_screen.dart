import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';
import '../widgets/task_tile.dart';
import 'package:flutter_secure_storage/flutter_secure_storage.dart';

class TodoListScreen extends StatefulWidget {
  @override
  _TodoListScreenState createState() => _TodoListScreenState();
}

class _TodoListScreenState extends State<TodoListScreen> {
  List tasks = [];
  bool _isAddingTask = false;
  TextEditingController _newTaskController = TextEditingController();
  final String baseUrl = 'https://efeb-187-180-189-147.ngrok-free.app/api/v1/tasks';
  final storage = FlutterSecureStorage();

  @override
  void initState() {
    super.initState();
    fetchTasks();
  }

  Future<String?> getToken() async {
    String? token = await storage.read(key: 'token');
    if (token == null) {
      print('No token found');
      return null;
    }
    return token;
  }

  Future<void> fetchTasks() async {
    print('Fetching tasks');
    String? token = await getToken();
    if (token == null) return;

    final response = await http.get(
      Uri.parse('$baseUrl/'),
      headers: {
        'Authorization': 'Bearer $token',
      },
    );

    if (response.statusCode == 200) {
      var decoded = json.decode(response.body);
      print(decoded);
      setState(() {
        tasks = decoded;
      });
    } else {
      print('Failed to load tasks with status code: ${response.statusCode}');
      throw Exception('Failed to load tasks');
    }
  }

  Future<void> _addTask() async {
    if (_newTaskController.text.isEmpty) {
      setState(() {
        _isAddingTask = false;
      });
      return;
    }

    String? token = await getToken();
    if (token == null) return;

    final response = await http.post(
      Uri.parse('$baseUrl/'),
      headers: {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer $token',
      },
      body: json.encode({'title': _newTaskController.text}),
    );

    if (response.statusCode == 201) {
      print('Task added');
      var newTask = json.decode(response.body);
      setState(() {
        tasks.add(newTask);
        _isAddingTask = false;
        _newTaskController.clear();
      });
    } else {
      throw Exception('Failed to add task');
    }
  }

  Future<void> _editTask(int index, String newTitle) async {
    final task = tasks[index];
    String? token = await getToken();
    if (token == null) return;
    final response = await http.put(
      Uri.parse('$baseUrl/${task['id']}'),
      headers: {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer $token',
      },
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
    print('Deleting task at index: $index');
    final task = tasks[index];
    String? token = await getToken();
    if (token == null) return;

    final response = await http.delete(
      Uri.parse('$baseUrl/${task['id']}'),
      headers: {
        'Authorization': 'Bearer $token',
      },
    );

    if (response.statusCode == 204) {
      setState(() {
        tasks.removeAt(index);
      });
      print('Task deleted successfully');
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
      body: Column(
        children: [
          if (_isAddingTask)
            Padding(
              padding: const EdgeInsets.all(8.0),
              child: Row(
                children: [
                  Expanded(
                    child: TextField(
                      controller: _newTaskController,
                      autofocus: true,
                      decoration: InputDecoration(
                        hintText: "Enter task title",
                        border: OutlineInputBorder(),
                      ),
                      onSubmitted: (value) {
                        _addTask();
                      },
                    ),
                  ),
                  IconButton(
                    icon: Icon(Icons.add),
                    onPressed: _addTask,
                  ),
                ],
              ),
            ),
          Expanded(
            child: ListView.builder(
              itemCount: tasks.length,
              itemBuilder: (context, index) {
                return TaskTile(
                  key: ValueKey(tasks[index]['id']),
                  task: tasks[index],
                  onEdit: (newTitle) => _editTask(index, newTitle),
                  onDelete: () => _deleteTask(index),
                );
              },
            ),
          ),
        ],
      ),
      floatingActionButton: FloatingActionButton(
        onPressed: () {
          setState(() {
            _isAddingTask = true;
          });
        },
        child: Icon(Icons.add),
      ),
    );
  }
}
