# Ponderada 4

Nesta ponderada, foi desenvolvido um sistema assíncrono de microsserviços com armazenamento de observabilidade de logs com o ELK stack. Para tanto, utilizou-se do sistema de logs do Encontro 11 como base. Essse sistema, inicialmente, realizava o log de apenas um container, contendo dois serviços dentro de si (Usuarios e Produtos), utilizando Filebeat, Elastic Search e Kibana. Nesse caso, os logs de cada servico eram salvos em um arquivo de log, atraves d abiblioteca logging, que entao alimentava o filebeat, elastic search e kiaban.

Nesta aplicaçao, a fim de adicionar logs de microsservicos em containrs diferentes e de um gateway em nginx, comecamos separando usuarios e produtos em microsserivos diferentes e ciando o microsserivoc wishlisht, que associa produtos a usuarios. Criamos um pNesta ponderada, desenvolvemos um sistema assíncrono de microsserviços com armazenamento e observabilidade de logs utilizando a ELK stack. Usamos o sistema de logs do Encontro 11 como base, que originalmente registrava logs de apenas um container contendo dois serviços (Usuários e Produtos) usando Filebeat, Elasticsearch e Kibana. Nesse sistema inicial, os logs de cada serviço eram salvos em um arquivo de log através da biblioteca logging, que então alimentava o Filebeat, Elasticsearch e Kibana.

Para esta aplicação, aprimoramos o sistema separando os serviços de Usuários e Produtos em microsserviços distintos e adicionamos um novo microsserviço chamado Wishlist, que associa produtos a usuários. Também substituímos o banco de dados SQLite por PostgreSQL, em um container separado, para que todos os serviços pudessem acessá-lo. Cada microsserviço criou seu próprio objeto logger. Além disso, implementamos um gateway utilizando nginx.

Por fim, configuramos o Filebeat para procurar os arquivos de logs de todos os containers rodando no Docker. Dessa forma, conseguimos acessar o standard output, que inclui a biblioteca logging, de todos os microsserviços e também do gateway.

## Como Rodar
Para rodar o sistema, siga os passos abaixo:

1. Navegue até a pasta `<raiz-do-projeto>/ponderada4`.

2. Execute o comando:
```
docker-compose up

```
Isso iniciará todos os microsserviços, o banco de dados PostgreSQL, o gateway nginx e a stack ELK para observabilidade dos logs.

## Como Acessar os Logs no Kibana
Para acessar os logs no Kibana, siga os passos abaixo:

1. Abra o navegador e acesse `http://localhost:5601` para abrir o Kibana.
2. No Kibana, vá para "Management" no menu lateral.
3. Selecione "Index Patterns".
4. Clique em "Create index pattern".
5. No campo "Index pattern", digite filebeat-* e clique em "Next step".
6. No campo "Time Filter field name", selecione @timestamp e clique em "Create index pattern".
   
Agora você poderá visualizar os logs dos microsserviços no Kibana. Utilize as funcionalidades de busca e filtragem para analisar os logs conforme necessário.




https://github.com/elisaflemer/ponderadas-modulo10/assets/99259251/acebe0d8-84a4-4879-bf2a-8b103777f321

