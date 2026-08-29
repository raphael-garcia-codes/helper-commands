# O que o analisador enxerga (e como ensinar coisas novas)

Índice: [Como funciona](#como-funciona) · [Endpoints](#endpoints-reconhecidos) · [Fronteiras](#fronteiras-reconhecidas) · [Rótulos](#como-os-rotulos-sao-montados) · [Estender](#estender-a-deteccao) · [Diagnóstico](#diagnostico-de-resultados-ruins)

## Como funciona

`scan_endpoints.py` roda em três fases sobre a AST de cada arquivo `.py`:

1. **Imports e constantes** — monta o mapa de módulos importados e de constantes string do projeto (é assim que `prefix=settings.API_V1_STR` vira `/api/v1`).
2. **Tipagem de variáveis** — descobre o que cada variável é a partir do construtor: `redis.Redis()`, `boto3.client("s3")`, `psycopg2.connect()`, `httpx.AsyncClient(base_url=...)`, `conn.cursor()`, `connection.channel()`. Roda duas vezes para propagar entre módulos. É essa fase que evita confundir `cache.get(...)` com `dict.get(...)`.
3. **Rotas e efeitos** — encontra endpoints, e para cada handler segue a cadeia de chamadas internas (até 8 níveis) coletando as chamadas que cruzam fronteira, na ordem do código.

Uma chamada vira fronteira se: a variável já foi tipada por um construtor conhecido **ou** o módulo de origem é de uma biblioteca conhecida **ou** o nome da variável casa com o padrão da regra (`session`, `cursor`, `channel`, `client`…). O método chamado também precisa fazer sentido para aquele sistema.

## Endpoints reconhecidos

| Framework | Padrões |
|---|---|
| FastAPI / Starlette | `@app.get/post/put/patch/delete/websocket`, `@router.*`, `APIRouter(prefix=)`, `include_router(..., prefix=)` aninhado, `add_api_route` |
| Flask / Quart | `@app.route(..., methods=[...])`, `@bp.route`, `Blueprint(url_prefix=)`, `add_url_rule` |
| Django | `urls.py` com `path()` / `re_path()` / `url()`; método fica `ANY` |
| DRF | `router.register("recurso", ViewSet)` → expande em list/create/retrieve/update/destroy |
| aiohttp | `app.router.add_get/add_post/...` |

Rotas registradas com string montada em runtime não são vistas. Se um `methods=` tem vários verbos, cada verbo vira um endpoint separado.

## Fronteiras reconhecidas

| Sistema | Bibliotecas | Exemplos de chamada |
|---|---|---|
| API externa / ACL | requests, httpx, aiohttp, urllib3, zeep, grpc | `client.post(url)`, `requests.get(...)` |
| PostgreSQL / MySQL / SQLite / SQL Server / Oracle | SQLAlchemy, SQLModel, psycopg2/3, asyncpg, pymysql, aiomysql, sqlite3, databases, tortoise, peewee, Django ORM | `session.execute("SELECT ...")`, `cur.execute(...)`, `Order.objects.filter(...)`, `session.add(...)` |
| Redis / Memcached | redis, redis.asyncio, aioredis, pymemcache | `redis_client.get/setex/hset/publish` |
| RabbitMQ | pika, aio_pika, kombu, aiormq | `channel.basic_publish(routing_key=...)` |
| Kafka | kafka-python, aiokafka, confluent_kafka | `producer.send("topic", ...)` |
| SQS / SNS / DynamoDB / S3 / SES | boto3, aioboto3, minio | `s3.put_object(Bucket=...)`, `sqs.send_message(...)` |
| MongoDB | pymongo, motor, beanie | `collection.insert_one(...)` |
| Elasticsearch / OpenSearch | elasticsearch, opensearch-py | `es.search(index=...)` |
| Celery | celery | `task.delay(...)`, `apply_async(...)` |
| E-mail | smtplib, emails, sendgrid | `message.send(...)` |

O dialeto SQL sai do driver importado, da URL de conexão (`postgresql+psycopg://…`), do `ENGINE` do Django ou, em último caso, da menção mais frequente no código. Sem nenhum sinal, o rótulo é `Database` — vale renomear à mão.

## Como os rótulos são montados

- **SQL**: se há string literal, usa verbo + tabela (`SELECT payments`); senão, mapeia o método (`filter`→SELECT, `add`/`create`→INSERT, `save`→UPSERT, `delete`→DELETE) e tenta a entidade (`Order.objects` → `order`).
- **HTTP**: verbo + path da URL; o nome do sistema vem do host (`https://payment.internal/...` → `PaymentAPI` → rótulo `Payment API`), do `base_url` do client, ou do nome da variável (`crm_client` → `CrmAPI`).
- **Fila**: `Publish <routing_key|topic|queue>`.
- **Cache**: método + chave sem a parte variável (`GET customer:{id}` → `GET customer`).

Passos idênticos consecutivos são colapsados; entre dois passos do mesmo sistema com o mesmo verbo, fica o rótulo mais específico. `COMMIT`/`ROLLBACK`/`EXECUTE` sozinhos são descartados (use `--keep-tx` para manter).

## Estender a detecção

Tudo fica no topo de `scripts/scan_endpoints.py`.

**Biblioteca nova** — acrescente uma entrada em `RULES` (a ordem importa: regras mais específicas primeiro, porque `.get(` é ambíguo):

```python
dict(system="Vault", kind="external_api",
     roots={"hvac"},                      # módulos importados
     var_re=r"(vault|secrets)",           # nomes de variável plausíveis
     attrs={"read", "write", "list"}),    # métodos que cruzam a fronteira
```

**Construtor novo** — acrescente em `CTORS` para que a variável seja tipada e todas as chamadas sobre ela sejam capturadas, mesmo em outro módulo:

```python
({"Client"}, {"hvac"}, "Vault", "external_api"),
```

`system` pode ser `"__SQL__"` (resolve para o dialeto detectado) ou `"__HTTP__"` (nome derivado da URL). `kind` define a forma do nó no fluxograma.

## Diagnóstico de resultados ruins

| Sintoma | Causa provável | O que fazer |
|---|---|---|
| Poucos endpoints | rotas montadas dinamicamente, ou raiz errada (monorepo) | conferir a raiz; registrar os endpoints à mão no JSON |
| Endpoint sem passos | client injetado por DI, wrapper genérico, ou de fato não há integração | abrir o handler; se houver chamada, acrescentar o passo |
| `ExternalAPI` genérico | URL vem de config em runtime | achar a URL no settings/`.env` e renomear em `systems{}` |
| Passos demais e repetidos | camada de repositório muito fina, `refresh`/`commit` | usar o padrão sem `--keep-tx` e enxugar o JSON |
| Fronteira que não existe | falso positivo (`.get()` de dicionário com nome parecido) | remover o passo do JSON e, se recorrente, apertar o `var_re` da regra |
