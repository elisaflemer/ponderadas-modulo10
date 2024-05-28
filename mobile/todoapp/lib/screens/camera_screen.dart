import 'package:flutter/material.dart';
import 'package:camera/camera.dart';
import 'package:http/http.dart' as http;
import 'dart:io';
import 'package:path_provider/path_provider.dart';
import 'package:path/path.dart';
import 'package:http_parser/http_parser.dart';
import 'package:flutter_local_notifications/flutter_local_notifications.dart';
import 'package:todoapp/constants/baseUrl.dart';
import 'package:flutter_secure_storage/flutter_secure_storage.dart';

class CameraScreen extends StatefulWidget {
  final CameraDescription camera;
  final FlutterLocalNotificationsPlugin flutterLocalNotificationsPlugin;

  const CameraScreen({super.key, required this.camera, required this.flutterLocalNotificationsPlugin});

  @override
  State<CameraScreen> createState() => CameraScreenState();
}

class CameraScreenState extends State<CameraScreen> {
  late CameraController _controller;
  late Future<void> _initializeControllerFuture;
  bool _isLoading = false;
  String? _processedImagePath;

  @override
  void initState() {
    super.initState();
    _controller = CameraController(
      widget.camera,
      ResolutionPreset.high,
    );
    _initializeControllerFuture = _controller.initialize();
  }

  @override
  void dispose() {
    _controller.dispose();
    super.dispose();
  }

  Future<void> _takePicture() async {
    setState(() {
      _isLoading = true;
      _processedImagePath = null;
    });

    try {
      await _initializeControllerFuture;
      final image = await _controller.takePicture();
      await _sendPicture(File(image.path));
    } catch (e) {
      print(e);
    } finally {
      setState(() {
        _isLoading = false;
      });
    }
  }

  Future<void> _sendPicture(File image) async {
  // Create an instance of FlutterSecureStorage
  final storage = FlutterSecureStorage();
  
  // Retrieve the token from secure storage
  String? token = await storage.read(key: 'token');

  // Check if token is not null
  if (token == null) {
    print('No token found');
    return;
  }

  var url = Uri.parse(baseUrl + '/images/black-and-white/');
  var request = http.MultipartRequest('POST', url)
    ..files.add(await http.MultipartFile.fromPath(
      'file',
      image.path,
      contentType: MediaType('image', 'jpeg'),
    ))
    ..headers['Authorization'] = 'Bearer $token';

  var response = await request.send();

  if (response.statusCode == 200) {
    var responseData = await http.Response.fromStream(response);
    var bytes = responseData.bodyBytes;
    var tempDir = await getTemporaryDirectory();
    var tempFile = File('${tempDir.path}/${basename(image.path)}.png');
    await tempFile.writeAsBytes(bytes);

    setState(() {
      _processedImagePath = tempFile.path;
    });

    print('Picture processed and downloaded successfully');
  } else {
    print('Picture upload failed with status: ${response.statusCode}');
  }
}

  Future<void> _showNotification(String title, String body) async {
    const AndroidNotificationDetails androidPlatformChannelSpecifics =
        AndroidNotificationDetails(
      'your_channel_id', // id
      'Your Channel Name', // name
      channelDescription: 'This channel is used for important notifications.', // description
      importance: Importance.high,
      priority: Priority.high,
      playSound: false,
      enableVibration: true,
    );
    const NotificationDetails platformChannelSpecifics =
        NotificationDetails(android: androidPlatformChannelSpecifics);
    await widget.flutterLocalNotificationsPlugin.show(
      0,
      title,
      body,
      platformChannelSpecifics,
      payload: 'item x',
    );
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Take a Picture'),
      ),
      body: _isLoading
          ? const Center(child: CircularProgressIndicator())
          : _processedImagePath != null
              ? Column(
                  children: [
                    Expanded(child: Image.file(File(_processedImagePath!))),
                    ElevatedButton(
                      onPressed: () {
                        setState(() {
                          _processedImagePath = null;
                        });
                      },
                      child: const Text('Take Another Picture'),
                    ),
                  ],
                )
              : FutureBuilder<void>(
                  future: _initializeControllerFuture,
                  builder: (context, snapshot) {
                    if (snapshot.connectionState == ConnectionState.done) {
                      return CameraPreview(_controller);
                    } else {
                      return const Center(child: CircularProgressIndicator());
                    }
                  },
                ),
      floatingActionButton: _processedImagePath == null
          ? FloatingActionButton(
              onPressed: _takePicture,
              child: const Icon(Icons.camera),
            )
          : null,
    );
  }
}
