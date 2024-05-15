# Documentação da API Todo

Esta ponderada consistia em criar um aplicativo de lista de tarefas com backend dockerizado e uma interface mobile feita com Flutter para Android. A API seguiu os padrões de maturidade de Richardson, foi desenvolvida com FASTAPI e está assíncrona. Por ora, a única função dessa API é gerenciar uma tabela de tasks. A arquitetura não seguiu nenhum padrão específico devido à simplicidade do sistema, mas, em iterações posteriores, se recomendaria implementar uma organização MVC. O código-fonte está disponível na pasta `fastapi` e é executável via docker-compose. 

Já a interface está disponível no caminho `mobile/todoapp`. Ela possui duas telas: uma de boas-vindas e uma com a lista de afazeres. Essa lista busca as tarefas da API e permite que, ao clicar em qualquer uma delas, seja possível editá-las ou deletá-las. Também existe um botão flutuante para que se possa adicionar tarefas novas. Tudo isso tem como entrypoint of arquivo main.dart.

## Demo

[Screencast from 05-05-2024 23:06:32.webm](https://github.com/elisaflemer/ponderadas-modulo10/assets/99259251/42914c75-58f3-4f58-b6ca-4c1fc8ef1833)

## Como executar

### FastAPI

1. Entre na pasta `fastapi`
2. Execute o seguinte comando: `docker compose up`
   
### Flutter

1. Entre na pasta `mobile/todoapp/lib`,
2. Certifique-se de ter o Android Studio instalado com um emulador configurado para Android.
3. Execute o arquivo `main.dart` no emulador.

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
