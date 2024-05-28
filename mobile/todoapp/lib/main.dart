import 'package:flutter/material.dart';
import 'package:camera/camera.dart';
import 'package:todoapp/screens/login_screen.dart';
import 'package:todoapp/screens/signup_screen.dart';
import 'package:todoapp/screens/camera_screen.dart';
import 'package:flutter_local_notifications/flutter_local_notifications.dart';
import 'package:permission_handler/permission_handler.dart'; // Add this line

void main() async {
  WidgetsFlutterBinding.ensureInitialized();
  
  // Initialize camera
  final cameras = await availableCameras();
  final firstCamera = cameras.first;
  
  // Initialize notification plugin
  final FlutterLocalNotificationsPlugin flutterLocalNotificationsPlugin = FlutterLocalNotificationsPlugin();
  const AndroidInitializationSettings initializationSettingsAndroid = AndroidInitializationSettings('@mipmap/ic_launcher');
  final InitializationSettings initializationSettings = InitializationSettings(android: initializationSettingsAndroid);
  await flutterLocalNotificationsPlugin.initialize(initializationSettings);

  // Create the notification channel
  const AndroidNotificationChannel channel = AndroidNotificationChannel(
    'your_channel_id', // id
    'Your Channel Name', // name
    description: 'This channel is used for important notifications.', // description
    importance: Importance.high,
  );

  await flutterLocalNotificationsPlugin
      .resolvePlatformSpecificImplementation<AndroidFlutterLocalNotificationsPlugin>()
      ?.createNotificationChannel(channel);

  // Request notification permission for Android 13+
  if (await Permission.notification.isDenied) {
    await Permission.notification.request();
  }

  runApp(MyApp(camera: firstCamera, flutterLocalNotificationsPlugin: flutterLocalNotificationsPlugin));
}

class MyApp extends StatelessWidget {
  final CameraDescription camera;
  final FlutterLocalNotificationsPlugin flutterLocalNotificationsPlugin;

  const MyApp({super.key, required this.camera, required this.flutterLocalNotificationsPlugin});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Flutter Demo',
      theme: ThemeData(
        colorScheme: ColorScheme.fromSeed(seedColor: Colors.greenAccent),
        useMaterial3: true,
      ),
      initialRoute: '/login',
      routes: {
        '/login': (context) => const LoginScreen(),
        '/signup': (context) => const SignUpScreen(),
        '/camera': (context) => CameraScreen(camera: camera, flutterLocalNotificationsPlugin: flutterLocalNotificationsPlugin),
      },
    );
  }
}
