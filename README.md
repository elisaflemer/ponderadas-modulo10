# Aplicação de Lista de Tarefas: Visão Geral e Configuração

## Visão Geral da Aplicação
Esta aplicação de Lista de Tarefas consiste em um frontend em Flutter e um backend em FastAPI. O backend é projetado de forma assíncrona e monolítica, utilizando PostgreSQL para armazenamento de dados e Docker Compose para orquestração de contêineres. O mecanismo de autenticação utiliza JWTs (JSON Web Tokens) com chaves públicas e privadas, garantindo comunicação segura e armazenamento de tokens.

### Frontend: Flutter
O frontend é construído usando Flutter, um framework popular para a construção de aplicativos móveis multiplataforma. Ele inclui funcionalidades para adicionar, editar e excluir tarefas, com gerenciamento de estado para garantir que a interface do usuário permaneça sincronizada com o backend.

#### Componentes Principais
- LoginScreen: A tela de início, que realiza a requisição de login com email e senha e salva o token recebido de forma segura. 
- TodoListScreen: A tela principal que exibe a lista de tarefas.
- TaskTile: Um widget que representa uma única tarefa, incluindo opções para editar e excluir a tarefa.

#### Executando o Frontend

1. Clonar o repositório: Clone o repositório do projeto a partir do seu sistema de controle de versão.

```
git clone https://github.com/elisaflemer/ponderadas-modulo10/tree/main
cd ponderadas-modulo10/mobile/todoapp
```

2. Instalar dependências: Certifique-se de ter o Flutter instalado. Em seguida, execute:

```
flutter pub get
```

3. Executar o aplicativo: Conecte um dispositivo ou inicie um emulador e execute:

```
flutter run
```

### Backend: FastAPI
O backend é implementado usando FastAPI, um framework web moderno e rápido para a construção de APIs com Python 3.7+. O banco de dados utilizado é o PostgreSQL, e o Docker Compose é usado para gerenciar os serviços.

#### Componentes Principais
- FastAPI: Lida com os endpoints e a lógica da API.
- PostgreSQL: O banco de dados usado para armazenar tarefas.
- Docker Compose: Gerencia a aplicação de múltiplos contêineres, garantindo que o backend e o banco de dados funcionem juntos perfeitamente.

O FastAPI suporta operações assíncronas, que são usadas para lidar com requisições de API de forma eficiente. A natureza assíncrona garante que a aplicação possa lidar com múltiplas requisições simultaneamente, melhorando o desempenho e a capacidade de resposta.

#### Executando o Backend

1. Clone este repositório.

```
git clone https://github.com/elisaflemer/ponderadas-modulo10/tree/main
cd ponderadas-modulo10/fastapi
```

2. Configurar o ambiente: Certifique-se de ter o Docker e Docker Compose instalados.

3. Executar o Docker Compose: No diretório do projeto, execute:

```
docker-compose up --build
```

### Autenticação com JWT
A autenticação é feita usando JWTs (JSON Web Tokens), com chaves pública e privada para assinar e verificar os tokens. Os tokens JWT são armazenados de forma segura no dispositivo móvel usando Flutter Secure Storage.

### Armazenamento Seguro
Os tokens JWT são armazenados no dispositivo móvel de forma segura, utilizando a biblioteca flutter_secure_storage no Flutter. Isso garante que os tokens de autenticação estejam protegidos contra acessos não autorizados.

## Demo


https://github.com/elisaflemer/ponderadas-modulo10/assets/99259251/c7b9e0d9-25df-48c8-aa4a-e7bbf32d3251



================================================================================================================================================
# Ponderadas anteriores 

## Teste de Escalabilidade

O teste de escalabilidade, descrito no código Python com asyncio e aiohttp, é um experimento para comparar o desempenho dos dois servidores em condições de carga simultânea. O código gera uma série de solicitações HTTP para cada servidor, executando operações de cadastro, login e criação de tarefas. O objetivo é medir e comparar o tempo médio de resposta para grupos de solicitações enviadas aos dois servidores. O teste inclui:

- Registro de usuário com nome e senha gerados aleatoriamente.
- Login do usuário para obter um JWT.
- Criação de uma tarefa usando o JWT.
- Os tempos médios por grupo para cada servidor são calculados e comparados para determinar qual servidor responde mais rapidamente sob carga.
  
### Resultado

```
Starting the requests...
Total time for all request groups: 12.28 seconds
Average time per group for Server 1: 3.0701 seconds
Average time per group for Server 2: 2.5598 seconds
Server 2 (Async) is faster.
```

## Como executar

### FastAPI

1. Entre na pasta `fastapi`
2. Execute o seguinte comando: `docker compose up`
   
### Flask

1. Entre na pasta `flask`
2. Execute o seguinte comando: `docker compose up`

### Teste de escalabilidade

1. Volte para a pasta raiz
2. Execute o seguinte comando: `python3 performance_test.py`

## Demo

[Screencast from 2024-04-29 10-15-41.webm](https://github.com/elisaflemer/ponderadas-modulo10/assets/99259251/83d687f1-99a3-4c08-af8f-d6d9269aa328)
