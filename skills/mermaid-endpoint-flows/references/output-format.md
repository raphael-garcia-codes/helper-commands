# Formato dos dois arquivos

Os exemplos abaixo são a saída real do gerador para um serviço de pagamentos com quatro endpoints. Use-os como referência quando precisar editar um `.mmd` à mão.

## 1. Diagrama de sequência — `<app>-sequence.mmd`

Um bloco por endpoint, separado por uma `Note`. Participantes declarados uma vez no topo, na ordem em que aparecem.

```mermaid
sequenceDiagram
    participant Client as Client
    participant API as Minha API
    participant PaymentAPI as Payment API
    participant PostgreSQL as PostgreSQL
    participant Redis as Redis
    participant RabbitMQ as RabbitMQ

    Note over Client,API: POST /payment
    Client->>API: POST /payment
    API->>PaymentAPI: POST /payments
    PaymentAPI-->>API: resposta
    API->>PostgreSQL: INSERT payments
    PostgreSQL-->>API: resposta
    API->>Redis: GET customer
    Redis-->>API: resposta
    API->>RabbitMQ: Publish PaymentCreated
    API-->>Client: 201 Created

    Note over Client,API: GET /customers/{customer_id}
    Client->>API: GET /customers/{customer_id}
    API->>PostgreSQL: SELECT payments
    PostgreSQL-->>API: resposta
    API-->>Client: 200 OK

    Note over Client,API: GET /health
    Client->>API: GET /health
    API-->>Client: 200 OK
```

Regras:

- Publicação em fila **não** tem seta de volta; banco, cache, storage e API externa têm.
- Resposta ao cliente default: `201 Created` para POST, `204 No Content` para DELETE, `200 OK` no resto. Ajuste à mão quando o código disser outra coisa (`202 Accepted` em fluxo assíncrono é comum).
- Endpoint sem fronteira aparece mesmo assim — a ausência de integração é informação.
- Texto de mensagem não vai entre aspas, então `;` e `#` precisam ser removidos.

## 2. Fluxograma por endpoint — `<app>-flow.mmd`

Padrão do gerador. Mostra o recorte de cada endpoint dentro da aplicação.

```mermaid
flowchart LR
    Client([Client])

    subgraph APP["Minha API"]
        direction TB
        EP1["POST /payment"]
        EP2["GET /customers/{customer_id}"]
        EP3["PUT /customers/{customer_id}/cache"]
        EP4["GET /health"]
    end

    PaymentAPI["Payment API"]
    PostgreSQL[("PostgreSQL")]
    Redis[("Redis")]
    RabbitMQ[/"RabbitMQ"/]

    Client --> EP1
    EP1 -->|POST /payments| PaymentAPI
    EP1 -->|INSERT payments| PostgreSQL
    EP1 -->|GET customer| Redis
    EP1 -->|Publish PaymentCreated| RabbitMQ
    Client --> EP2
    EP2 -->|SELECT payments| PostgreSQL
    Client --> EP3
    EP3 -->|SETEX customer| Redis
    Client --> EP4

    classDef db fill:#e8f4ea,stroke:#4a7c59;
    classDef queue fill:#fdf3e0,stroke:#b8860b;
    classDef api fill:#eef2fb,stroke:#4a5fa5;
    class PostgreSQL,Redis db;
    class RabbitMQ queue;
    class PaymentAPI api;
```

## 3. Fluxograma resumo — `--flow-style summary`

Visão de contexto, útil quando há muitos endpoints ou quando o público é arquitetura/gestão.

```mermaid
flowchart LR
    APP["Minha API"]
    PaymentAPI["Payment API"]
    PostgreSQL[("PostgreSQL")]
    Redis[("Redis")]
    RabbitMQ[/"RabbitMQ"/]

    APP -->|1 endpoint| PaymentAPI
    APP -->|2 endpoints| PostgreSQL
    APP -->|2 endpoints| Redis
    APP -->|1 endpoint| RabbitMQ
```

## Escapes que quebram o Mermaid

| Situação | Solução aplicada pelo gerador |
|---|---|
| Aspas duplas no rótulo | viram `&quot;` |
| `#` em qualquer texto | vira `num ` |
| `;` em mensagem de sequência | vira `,` |
| `{param}` no path | preservado — é válido dentro de rótulo com aspas e em mensagem |
| ID de nó com hífen, ponto ou espaço | normalizado para `[A-Za-z0-9_]` |

Depois de qualquer edição manual, rode `python scripts/check_mermaid.py arquivo.mmd`.

## Onde visualizar

Os `.mmd` renderizam direto no GitHub/GitLab (bloco ```` ```mermaid ````), no VS Code com a extensão Markdown Preview Mermaid, e em https://mermaid.live. Para embutir em documentação, cole o conteúdo dentro de um bloco `mermaid` no Markdown.
