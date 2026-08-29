---
name: mermaid-endpoint-flows
description: Varre um projeto Python inteiro, identifica todos os endpoints HTTP expostos e mapeia as fronteiras que cada um atravessa (outras APIs/ACLs, banco de dados, Redis, RabbitMQ, Kafka, S3, e-mail), gerando dois arquivos Mermaid — um diagrama de sequência e um fluxograma. Use sempre que o usuário pedir para mapear, documentar ou desenhar endpoints, fluxos, integrações, dependências externas ou fronteiras de um projeto/API/microserviço em Python (FastAPI, Flask, Django, DRF, aiohttp), ou pedir diagrama Mermaid, diagrama de sequência, fluxograma, C4 de contexto ou ".mmd" a partir de código Python — mesmo que não cite a palavra "Mermaid" explicitamente.
---

# Mapeamento de endpoints e fronteiras em Mermaid

Produz **dois arquivos** a partir de um projeto Python:

| Arquivo | Conteúdo |
|---|---|
| `<app>-sequence.mmd` | `sequenceDiagram`: um bloco por endpoint, na ordem em que as fronteiras são chamadas |
| `<app>-flow.mmd` | `flowchart`: cada endpoint ligado às fronteiras que toca |

## Regra de escopo (a mais importante)

Mapeie **apenas fronteiras do processo** — o que sai do serviço:

- outra API / ACL / integração HTTP ou gRPC
- banco de dados (PostgreSQL, MySQL, MongoDB…)
- cache (Redis, Memcached)
- fila / tópico (RabbitMQ, Kafka, SQS, Celery)
- storage (S3/MinIO), e-mail, serviços gerenciados

**Nunca** coloque classes, objetos, services, repositories, DTOs, camadas internas ou funções do projeto como participantes/nós. Um `PaymentService` que só orquestra não aparece; o `httpx.post` que ele faz por dentro, sim. Se o diagrama tem uma caixa que não é um processo separado rodando fora da aplicação, ela não pertence ali.

## Fluxo de trabalho

### 1. Localizar a raiz do projeto

Confirme o diretório antes de varrer. Se houver monorepo (`backend/`, `services/*`), pergunte qual serviço mapear ou gere um par de arquivos por serviço — misturar serviços num diagrama só destrói a leitura de fronteiras.

### 2. Varrer

```bash
python scripts/scan_endpoints.py <raiz> --out inventory.json --app-name "Minha API"
```

Opções úteis:

| Flag | Quando usar |
|---|---|
| `--app-name` | nome da caixa da aplicação (default: `title=` do FastAPI ou o nome da pasta) |
| `--path-filter '^/api/v1'` | projeto grande demais; recorta por rota |
| `--include-consumers` | também tratar consumers de fila / tasks Celery como entradas |
| `--include-tests` | raro; só se as rotas estiverem em pastas com nome de teste |
| `--keep-tx` | manter passos `COMMIT`/`ROLLBACK` no fluxo |

Saída: `inventory.json` com `endpoints[]` (método, path, handler, arquivo, passos ordenados) e `systems{}`.

### 3. Revisar o inventário — esta etapa não é opcional

A varredura é estática: ela acerta a maior parte, mas dispatch dinâmico, injeção de dependência e wrappers escondem chamadas. Antes de gerar os diagramas, **leia o inventário e confira o código**:

1. **Endpoints sem nenhum passo** (`steps: []`): abra o handler. Health check de verdade? Ótimo. Senão, a chamada foi escondida por algum wrapper — adicione o passo à mão.
2. **`warnings[]`**: arquivos que não parsearam e handlers não encontrados (rota registrada apontando para fora do escopo varrido).
3. **Nomes genéricos**: um sistema chamado `ExternalAPI` ou `Database` significa que o analisador não achou a URL/driver. Descubra o destino real no código ou no `.env`/settings e renomeie no JSON — o nome do parceiro (`Payment API`, `CRM ACL`) é o que dá valor ao diagrama.
4. **Contagem de endpoints** contra o que o time espera. Faltando muitos? Veja `references/detection-patterns.md` para o que é reconhecido e como estender.
5. **Ordem dos passos**: reflete a ordem de leitura do código, não o tempo de execução. Em handlers `async` com `gather`, reordene se fizer diferença para o entendimento.

Editar o `inventory.json` na mão é esperado e barato. Schema de um passo:

```json
{"system": "PaymentAPI", "kind": "external_api", "operation": "POST /payments", "source": "app/services/payment.py:22"}
```

`kind` ∈ `external_api` | `database` | `cache` | `queue` | `storage` — define a forma do nó no fluxograma. Sistemas novos precisam existir em `systems{}` com `label` e `kind`.

### 4. Gerar os dois arquivos

```bash
python scripts/generate_mermaid.py inventory.json --out-dir <destino>
```

| Flag | Efeito |
|---|---|
| `--flow-style summary` | fluxograma macro: uma caixa da API ligada às fronteiras (visão de contexto), em vez de um nó por endpoint |
| `--direction TB` | orientação do fluxograma |
| `--autonumber` | numera as mensagens da sequência |
| `--max-endpoints-per-file 25` | acima disso o diagrama de sequência é dividido em `-sequence-1.mmd`, `-2`… |

Acima de ~20 endpoints o fluxograma por endpoint fica ilegível. Nesse caso gere os dois estilos: o `summary` como visão de contexto e o detalhado dividido por área (`--path-filter` + `--prefix`).

### 5. Validar

```bash
python scripts/check_mermaid.py <destino>/*.mmd
```

Pega aspas desbalanceadas, participante usado sem declarar e caractere reservado solto. Se der erro, corrija o `.mmd` e rode de novo.

### 6. Entregar

Apresente os dois arquivos ao usuário e escreva um resumo curto **do que o mapeamento revelou**, não do que os scripts fizeram: quantos endpoints, quais fronteiras existem, quais endpoints concentram integrações, quais não tocam nada externo e quais dependem de um sistema que aparece uma vez só (candidato a acoplamento acidental).

## Formato de saída

Templates completos e comentados em `references/output-format.md`. Estrutura mínima:

```
sequenceDiagram
    participant Client
    participant API as Minha API
    participant PaymentAPI as Payment API
    participant PostgreSQL as PostgreSQL

    Note over Client,API: POST /payment
    Client->>API: POST /payment
    API->>PaymentAPI: POST /payments
    PaymentAPI-->>API: resposta
    API->>PostgreSQL: INSERT payments
    PostgreSQL-->>API: resposta
    API-->>Client: 201 Created
```

```
flowchart LR
    Client([Client])
    subgraph APP["Minha API"]
        EP1["POST /payment"]
    end
    PaymentAPI["Payment API"]
    PostgreSQL[("PostgreSQL")]
    EP1 -->|POST /payments| PaymentAPI
    EP1 -->|INSERT payments| PostgreSQL
```

Convenções que mantêm os arquivos consistentes entre execuções:

- Fila e tópico recebem seta sem retorno (publicação é assíncrona); banco, cache, storage e API externa recebem `-->>` de resposta.
- Rótulo de operação = verbo + alvo: `POST /payments`, `SELECT payments`, `GET customer`, `Publish PaymentCreated`.
- Formas: `[( )]` banco/cache/storage, `[/ /]` fila, `[ ]` API externa.
- Paths ficam como estão no código, com `{param}` / `<param>`.

## Frameworks reconhecidos

FastAPI (incluindo `APIRouter` aninhado e prefixo vindo de constante como `settings.API_V1_STR`), Flask e Quart (rotas e blueprints com `url_prefix`), Django (`urls.py` com `path`/`re_path`), DRF (`router.register`), aiohttp (`add_get`/`add_post`), Starlette e Tornado parcialmente.

Detecção de fronteiras, tipagem de clients e como adicionar uma biblioteca nova: `references/detection-patterns.md`.

## Limites conhecidos

- Chamadas montadas dinamicamente (`getattr(client, verb)`, mapas de handlers) não são vistas.
- Um client recebido só via injeção de dependência sem construtor rastreável vira `ExternalAPI` genérico.
- A profundidade de cadeia de chamadas é 8 níveis; funções com nome duplicado em muitos módulos são ignoradas para não inventar fluxo.
- Middlewares e autenticação global não entram: eles valem para todos os endpoints e poluiriam os dois diagramas. Se o time quiser esse detalhe, acrescente uma nota no topo do `.mmd` em vez de um participante.
