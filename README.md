# Documentação da API Todo

A API Todo é um serviço RESTful projetado para gerenciamento de tarefas. Este serviço é construído com Flask e integra autenticação de usuário, gerenciamento de tarefas e tratamento de erros. Ele foi testado com o Insomnia para testes e interações da API.

Esta API adere ao Nível 2 do Modelo de Maturidade Richardson. Ela aproveita os verbos HTTP de maneira apropriada e emprega cabeçalhos e códigos de resposta HTTP de forma eficaz.

A API utiliza JWT (JSON Web Token) para autenticação de usuários. O token é armazenado em cookies e usado para autenticar as requisições à API.

## Acesso às Rotas
### Rotas abertas:
- Registro de usuário (/user-register)
- Login de usuário (/user-login)
- Criação de token (/api/v1/token)
  
### Rotas que exigem autenticação:
Todas as rotas que gerenciam conteúdos de tarefas e dados de usuário, como /api/v1/users e /api/v1/tasks, requerem um token JWT válido fornecido no cookie de requisição.

## Como executar

1. Clone este repositório
2. Na pasta raiz, execute `pip install -r requirements.txt` para instalar as dependências
3. Na pasta `build`, inicie o banco de dados com o comando `docker compose up`
4. Para criar as tabelas, volte à pasta raiz e execute `python src/main.py create_db`
5. Por fim, para rodar a API, execute `python -m flask --app src.main run`

## Checkpoint 2

O servidor síncrono foi Dockerizado em duas imagens: uma para o Flask e uma para o banco em Postgres. A imagem do Flask roda um entrypoint em bash que cria o banco e então inicia o servidor. Isso só é feito após lançar o container de banco.

O docker-compose lança ambos os containers e seta as variáveis de ambiente necessárias. Esse arquivo se encontra na pasta `build`. Já o Dockerfile está na pasta raiz.

## Demo

https://github.com/elisaflemer/ponderadas-modulo10/assets/99259251/33079ba3-e998-4dd5-843e-a45a1fdaf1ee

