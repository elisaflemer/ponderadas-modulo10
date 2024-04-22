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

## Demo
[Screencast from 2024-04-22 01-47-03.webm](https://github.com/elisaflemer/ponderadas-modulo10/assets/99259251/7ce4dba8-00e2-4b16-bfae-4e6a81e011e2)
