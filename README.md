# Ponderada 3

Este projeto é um processador de imagens que permite que os usuários façam login, capturem fotos usando a câmera do celular e processem essas fotos para convertê-las em preto e branco. O sistema é composto por um backend assíncrono desenvolvido com FastAPI, utilizando microsserviços para autenticação e processamento de imagens. O frontend é desenvolvido em Flutter, e a arquitetura será refatorada para seguir o padrão MVC até a entrega final.

## Vídeos Demonstrativos
### Frontend

### Backend

## Instruções de Configuração e Execução
### Pré-requisitos

- Docker e Docker Compose instalados
- Flutter instalado

### Passos para Executar o Projeto

1. Clone o repositório do projeto:
2. Lance os containers com `docker-compose up --build` na pasta `<caminho-do-repositorio>/src/backend`
3. Instale as dependências do Flutter: `flutter pub get`
4. Conecte um dispositivo ou inicie um emulador Android.
5. Execute o aplicativo Flutter: `flutter run`

## Arquitetura do Frontend
O frontend do projeto é desenvolvido em Flutter e segue uma arquitetura organizada em camadas, utilizando o padrão MVC (Model-View-Controller). A estrutura de diretórios é projetada para manter a separação de responsabilidades, facilitando a manutenção e escalabilidade do código.

### Estrutura de Diretórios
A estrutura de diretórios do projeto Flutter é a seguinte:

```
lib/
├── constants/
│   └── baseUrl.dart
├── controllers/
│   ├── login_controller.dart
│   └── signup_controller.dart
├── models/
│   └── user.dart
├── screens/
│   ├── camera_screen.dart
│   ├── login_screen.dart
│   └── signup_screen.dart
├── services/
│   └── api_service.dart
├── widgets/
│   └── custom_text_field.dart
└── main.dart
```

### Descrição dos Componentes

1. **Constants**
constants/baseUrl.dart: Este arquivo contém a definição da URL base da API, centralizando a configuração do endpoint para facilitar mudanças futuras.

2. **Controllers**
controllers/login_controller.dart: Controlador responsável por gerenciar a lógica de autenticação do usuário, incluindo login e armazenamento seguro do token.
controllers/signup_controller.dart: Controlador responsável por gerenciar a lógica de registro de novos usuários.

3. **Models**
models/user.dart: Define a estrutura de dados do usuário. Utiliza a biblioteca json_serializable para facilitar a serialização e desserialização de objetos JSON.

4. **Screens**
screens/camera_screen.dart: Tela que permite ao usuário capturar fotos utilizando a câmera do dispositivo. Após a captura, a foto é enviada para o backend para ser processada em preto e branco.
screens/login_screen.dart: Tela de login do usuário. Coleta as credenciais e chama o controlador de login para autenticação.
screens/signup_screen.dart: Tela de registro de novos usuários. Coleta as informações necessárias e chama o controlador de registro para criar um novo usuário.

5. **Services**
services/api_service.dart: Serviço responsável por fazer as chamadas HTTP para o backend. Inclui métodos para login, registro e envio de imagens.

6. **Widgets**
widgets/custom_text_field.dart: Contém widgets reutilizáveis para a interface do usuário, como campos de texto personalizados.

7. **Main**
main.dart: Ponto de entrada da aplicação Flutter. Configura a inicialização do aplicativo e define as rotas principais.

### Descrição Adicional dos Componentes
#### Secure Storage
O flutter_secure_storage é utilizado para armazenar tokens de autenticação de forma segura no dispositivo. Após o login, o token JWT é salvo no armazenamento seguro, permitindo que a aplicação autentique as requisições subsequentes sem que o usuário precise realizar login novamente.

#### Local Notifications
A biblioteca flutter_local_notifications é usada para enviar notificações locais ao usuário. Após o processamento bem-sucedido de uma imagem, o aplicativo envia uma notificação para informar o usuário que a imagem foi processada e salva.

### Fluxo de Trabalho
1. Login/Registro: O usuário se registra ou faz login através das telas de registro e login. As credenciais são enviadas para o backend, que valida as informações e retorna um token JWT.
2. Armazenamento do Token: Após a autenticação bem-sucedida, o token JWT é armazenado de forma segura utilizando o flutter_secure_storage.
3. Captura de Imagem: O usuário pode capturar uma imagem utilizando a tela da câmera. A imagem capturada é então enviada para o backend para processamento.
4. Processamento de Imagem: O backend processa a imagem, convertendo-a para preto e branco, e retorna a imagem processada.
5. Notificação Local: Após o processamento da imagem, uma notificação local é enviada ao usuário informando que a imagem foi processada e salva no dispositivo.

Essa arquitetura modular e bem definida facilita a manutenção e a escalabilidade do aplicativo, assegurando que cada componente tenha responsabilidades claras e bem definidas.

## Arquitetura do Backend
O backend do projeto é desenvolvido com FastAPI e utiliza uma arquitetura de microsserviços para gerenciar autenticação, processamento de imagens e logs. A estrutura do projeto é organizada para garantir a separação de responsabilidades e facilitar a manutenção.

### Estrutura de Diretórios

 ```
fastapi/
├── gateway/
│   ├── Dockerfile
│   └── nginx.conf
├── image_processor/
│   ├── models/
│   ├── routes/
│   ├── services/
│   ├── __init__.py
│   ├── database.py
│   ├── Dockerfile
│   ├── main.py
│   └── requirements.txt
├── init-db/
├── logs/
│   ├── models/
│   ├── routes/
│   ├── services/
│   ├── public_key.pem
│   ├── __init__.py
│   ├── database.py
│   ├── Dockerfile
│   ├── main.py
│   └── requirements.txt
└── users/
    ├── models/
    ├── routes/
    ├── services/
    │   ├── private_key.pem
    │   ├── public_key.pem
    ├── __init__.py
    ├── database.py
    ├── Dockerfile
    ├── main.py
    └── requirements.txt
```

### Componentes Principais
1. **Gateway**
nginx.conf: Configuração do Nginx para redirecionar as requisições aos microsserviços.
Dockerfile: Configuração do contêiner Docker para o gateway.

2. **Image Processor**
models/: Modelos de dados para o processamento de imagens.
routes/: Rotas da API para processamento de imagens.
services/: Lógica de negócios para processamento de imagens.
database.py: Configuração do banco de dados.
main.py: Inicialização do serviço de processamento de imagens.
Dockerfile: Configuração do contêiner Docker.
requirements.txt: Dependências do serviço.

3. **Logs**
models/: Modelos de dados para logs.
routes/: Rotas da API para gerenciamento de logs.
services/: Lógica de negócios e autenticação para logs.
public_key.pem: Chave pública para verificação de JWT.
database.py: Configuração do banco de dados.
main.py: Inicialização do serviço de logs.
Dockerfile: Configuração do contêiner Docker.
requirements.txt: Dependências do serviço.

4. **Users**
models/: Modelos de dados para autenticação de usuários.
routes/: Rotas da API para autenticação de usuários.
services/: Lógica de negócios e autenticação de usuários.
private_key.pem: Chave privada para assinatura de JWT.
public_key.pem: Chave pública para verificação de JWT.
database.py: Configuração do banco de dados.
main.py: Inicialização do serviço de autenticação de usuários.
Dockerfile: Configuração do contêiner Docker.
requirements.txt: Dependências do serviço.