---
name: documentation
description: Analisa um projeto de software inteiro (qualquer linguagem/framework) só com base em evidências reais do código-fonte e configuração, e produz/atualiza um `INSTRUCTIONS.md` técnico-funcional completo — visão de negócio, arquitetura, APIs, integrações, variáveis de ambiente, como rodar/testar localmente, pontos de atenção de um Staff Engineer, e diagramas Mermaid de sequência/arquitetura embutidos e visíveis. Use sempre que o usuário pedir para documentar, mapear, analisar ou explicar um projeto/repositório/API/serviço como um todo, pedir um "INSTRUCTIONS.md", "documentação técnica", "onboarding técnico completo" ou diagramas de sequência/arquitetura de um projeto — mesmo sem citar "Mermaid" explicitamente.
---

# Documentação técnica e funcional de projetos (INSTRUCTIONS.md)

Atue como um **Staff Software Engineer / Architect**. Produz um único arquivo, `INSTRUCTIONS.md`, que serve como referência para qualquer engenheiro entender, executar, manter ou evoluir o projeto — baseado **exclusivamente em evidências encontradas no código-fonte**, nunca em suposição.

Esta skill absorve e substitui qualquer skill anterior de geração isolada de diagramas Mermaid de endpoint — a geração dos diagramas é uma etapa deste mesmo fluxo (ver "Diagramas Mermaid" abaixo).

## Regras obrigatórias (hard gate)

1. **Explore o projeto inteiro antes de escrever qualquer linha.** Todos os diretórios e arquivos relevantes — não só os "principais". Isso inclui: arquivos de configuração (`.env`, `.env.example`, `appsettings.*`, `application.yml/properties`, `config.*`, YAML/JSON/TOML), Dockerfile, docker-compose, manifests Kubernetes/Helm, Terraform, scripts, pipelines de CI/CD, arquivos de build e de package manager, lockfiles, migrations, configuração de testes. Esses arquivos revelam dependências e integrações que não aparecem no código de aplicação.
2. **Não faça suposições.** Não invente funcionalidades, endpoints, dependências, versões, integrações, variáveis de ambiente ou comportamento que não estejam evidenciados.
3. **Quando uma informação não puder ser determinada com segurança**, diga isso explicitamente no documento e, quando possível, indique onde ela deveria estar definida.
4. **Diferencie sempre**: o que foi identificado no código vs. o que foi inferido a partir da implementação vs. o que não pôde ser determinado.
5. **Adapte a análise à natureza real do projeto** — API REST, GraphQL, worker, consumer, producer, CLI, biblioteca, aplicação web, batch, microsserviço, monólito, lambda/serverless, orientada a eventos, ou outro. Não force um formato de API REST em um worker.
6. **Não force conceitos que não existem.** Sem API HTTP → não crie seção de endpoints fictícios, diga explicitamente que não há. Sem banco → diga que nenhum foi identificado. Sem mensageria → não inclua Kafka/RabbitMQ/etc. no diagrama.
7. **Não altere o comportamento da aplicação.** A atividade é análise e documentação — não refatore, não corrija bugs, não mude código, exceto se explicitamente solicitado.
8. **Nunca exponha secrets reais** encontrados no projeto (valores de `.env`, tokens, senhas versionadas). Se houver credencial versionada, sinalize o problema em "Pontos de atenção" sem copiar o valor.

## Fluxo de trabalho

### 1. Explorar

Liste toda a árvore do projeto (excluindo dependências instaladas: `node_modules`, `.venv`, `vendor`, `target`, etc. — essas são bibliotecas de terceiros, não código do projeto). Identifique a raiz real do código-fonte. Se for monorepo, pergunte qual serviço documentar ou gere um `INSTRUCTIONS.md` por serviço — misturar serviços destrói a utilidade do documento.

Leia, em paralelo quando possível: entry point(s), roteadores/controllers, camada de regra de negócio, camada de acesso a dados, arquivos de configuração/settings, `.env`/`.env.example`, manifestos de dependência (`requirements.txt`, `package.json`, `pom.xml`, `go.mod`, `Gemfile`, etc.), Dockerfile/compose, CI, testes, README existente (trate como ponto de partida a **verificar**, nunca como fonte de verdade — READMEs ficam desatualizados).

### 2. Verificar cada afirmação contra o código

Todo dado que for para o documento precisa de uma fonte rastreável (arquivo:linha, ou nome de arquivo de configuração). Isso vale inclusive para o que o README do projeto já afirma — confirme no código antes de repetir.

### 3. Diagramas Mermaid

Gerar dois diagramas visíveis (embutidos em blocos ` ```mermaid `) para as seções "Diagrama de sequência" e "Diagrama de arquitetura": um `sequenceDiagram` (um bloco por endpoint/fluxo de entrada, na ordem em que cruza fronteiras) e um `flowchart` (endpoints ligados às fronteiras que tocam).

**Regra de escopo:** mapeie apenas fronteiras do processo — o que sai do serviço: outra API/ACL (HTTP/gRPC), banco de dados, cache, fila/tópico, storage, e-mail, serviço gerenciado. Nunca participantes internos (classes, services, repositories, DTOs, camadas do projeto).

**Se o projeto for Python** (FastAPI, Flask, Django, DRF, aiohttp, Starlette, Tornado): use os scripts deste skill.

```bash
python scripts/scan_endpoints.py <raiz> --out inventory.json --app-name "Nome da App"
```

A varredura é estática e **não é confiável sozinha** — dispatch dinâmico, injeção de dependência (ex.: handler → use case → repositório injetado via `Depends()`/DI) e wrappers escondem chamadas. **Sempre revise o `inventory.json` linha a linha contra o código antes de gerar os `.mmd`**:
- Endpoint com `steps: []`: abra o handler. Health check de verdade → ok. Senão, a chamada foi escondida — adicione o passo manualmente com base na leitura real do código (siga a cadeia handler → use case/service → repositório/client concreto).
- `warnings[]`: arquivos que não parsearam, handlers fora do escopo varrido.
- Sistema genérico (`ExternalAPI`, `Database`): descubra o destino real no código/`.env`/settings e renomeie.
- Contagem de endpoints muito abaixo do esperado: reveja `references/detection-patterns.md`.

Editar o JSON à mão é esperado e barato. Schema de um passo:
```json
{"system": "PaymentAPI", "kind": "external_api", "operation": "POST /payments", "source": "app/services/payment.py:22"}
```
`kind` ∈ `external_api` | `database` | `cache` | `queue` | `storage`. Sistemas novos precisam existir em `systems{}` com `label` e `kind`.

Depois de revisar/corrigir o inventário:
```bash
python scripts/generate_mermaid.py inventory.json --out-dir <destino>
python scripts/check_mermaid.py <destino>/*.mmd
```
`generate_mermaid.py` aceita `--flow-style summary` (visão de contexto macro em vez de nó por endpoint — usar acima de ~20 endpoints), `--direction TB`, `--autonumber`, `--max-endpoints-per-file`. Corrija manualmente status HTTP genéricos que o gerador não conhece (ex.: `202 Accepted` em fluxo assíncrono, `204` em delete) comparando com o código real antes de embutir no documento. `check_mermaid.py` precisa retornar `[ok]` para todos os arquivos antes de seguir.

**Se o projeto não for Python** (ou os scripts não cobrirem o framework): monte os dois diagramas à mão, seguindo exatamente o mesmo formato e as mesmas convenções — ver `references/output-format.md`. A regra de escopo e o processo de verificação contra o código são os mesmos independentemente da linguagem.

Depois de gerar (por script ou à mão), copie o conteúdo dos `.mmd` para dentro do `INSTRUCTIONS.md`, em blocos ` ```mermaid ` — nunca deixe os diagramas apenas como arquivos `.mmd` soltos ou apenas descritos em prosa; eles precisam estar **visíveis** no documento final.

Convenções (detalhe completo em `references/output-format.md`):
- Fila/tópico: seta de publicação sem retorno. Banco, cache, storage, API externa: seta de resposta (`-->>`).
- Rótulo = verbo + alvo (`POST /payments`, `SELECT payments`, `Publish PaymentCreated`).
- Formas: `[( )]` banco/cache/storage, `[/ /]` fila, `[ ]` API externa.
- Middlewares e autenticação global não entram como participante — são transversais a todos os fluxos; se relevante, uma nota de texto acima do diagrama basta.

Frameworks/bibliotecas reconhecidos pelos scripts e como estender a detecção: `references/detection-patterns.md`.

### 4. Escrever o INSTRUCTIONS.md

Siga a estrutura obrigatória de seções, cada uma detalhada em `references/instructions-template.md`:

1. Visão funcional
2. Visão técnica (com sub-seção **APIs expostas**, ou o mecanismo de entrada real se não houver HTTP)
3. Estrutura de diretórios
4. Dependências do projeto (stack, bibliotecas, infraestrutura)
5. Diagrama de sequência (mermaid embutido)
6. Diagrama de arquitetura (mermaid embutido)
7. Pontos de atenção (análise crítica de Staff Engineer)
8. Como executar o projeto localmente (pré-requisitos, obtenção, instalação, configuração/env vars, banco, execução, testes, build, Docker)
9. Integrações externas identificadas
10. Entradas e saídas
11. Qualidade da análise (checklist)
12. Resumo final

### 5. Revisão interna antes de entregar

Confirme, item a item:
- [ ] Todos os diretórios e principais arquivos relevantes foram analisados.
- [ ] Linguagem e, quando possível, sua versão foram identificadas.
- [ ] Frameworks e dependências relevantes foram identificados.
- [ ] APIs foram identificadas quando existentes (ou a ausência foi declarada explicitamente).
- [ ] Integrações externas, bancos, filas/tópicos foram identificados.
- [ ] Variáveis de ambiente foram identificadas.
- [ ] Comandos de build, teste e execução local foram identificados (ou declarados como não encontrados).
- [ ] Estrutura de diretórios foi documentada com responsabilidade validada pelo conteúdo, não pelo nome.
- [ ] Pontos de atenção têm evidência real, não opinião genérica sobre a tecnologia.
- [ ] Nenhuma informação foi inventada.
- [ ] Nenhum secret foi exposto.
- [ ] Os dois diagramas Mermaid estão embutidos, visíveis, e passaram no `check_mermaid.py` (ou foram revisados manualmente com o mesmo rigor).
- [ ] A documentação é específica deste projeto — não um texto genérico sobre a tecnologia usada.

### 6. Entregar

Ao final, informe resumidamente: (1) arquivo criado/atualizado; (2) tipo de aplicação identificado; (3) stack principal; (4) principais integrações encontradas; (5) quantidade de APIs/endpoints identificados, quando aplicável; (6) principais pontos de atenção; (7) qualquer informação importante que não pôde ser determinada durante a análise.

## Referências

- `references/instructions-template.md` — o que cada seção do `INSTRUCTIONS.md` deve conter, com exemplos de formato de tabela.
- `references/detection-patterns.md` — como `scan_endpoints.py` reconhece endpoints e fronteiras, e como estender para uma biblioteca/framework novo.
- `references/output-format.md` — formato exato dos dois `.mmd`, convenções de rótulo e forma de nó, e onde visualizar.

## Limites conhecidos

- A detecção estática de endpoints/fronteiras cobre bem Python; para outras linguagens, os diagramas precisam ser montados manualmente seguindo o mesmo formato — mais lento, mas mesma qualidade se a leitura de código for cuidadosa.
- Padrões de injeção de dependência que desacoplam handler de implementação concreta (Clean Architecture, hexagonal, DI containers) escondem fronteiras do scanner estático — é normal e esperado que boa parte do `inventory.json` precise de correção manual nesses projetos.
- Chamadas montadas dinamicamente (`getattr`, mapas de handler, reflection) não são vistas por nenhuma varredura estática — precisam ser encontradas por leitura manual.
