# Documentação da API Todo

O projeto descrito inclui dois servidores para gerenciamento de tarefas, um síncrono utilizando Flask e outro assíncrono com FastAPI, cada um operando em seu próprio ambiente Dockerizado com uma instância separada do Postgres. Ambos servidores oferecem funcionalidades para registro e login de usuários via JWT armazenados em cookies, além de permitir a criação, atualização e exclusão de tarefas.

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
