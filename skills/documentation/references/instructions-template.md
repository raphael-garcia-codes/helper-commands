# Template e regras de seção do INSTRUCTIONS.md

Este arquivo detalha, seção a seção, o que colocar no `INSTRUCTIONS.md`. O `SKILL.md` traz o fluxo de trabalho; aqui está o conteúdo esperado de cada seção.

Regra transversal: cada seção só existe se houver evidência. Se algo não se aplica ao projeto (sem API HTTP, sem banco, sem mensageria), **diga isso explicitamente** em vez de omitir a seção ou inventar conteúdo.

---

## Cabeçalho

Uma linha dizendo que o documento é referência técnica/funcional gerada por análise do código-fonte, mais o nome do projeto e, se houver, o remoto git.

## Visão funcional

Responde "o que o sistema faz", não "quais classes existem". Cobrir:
- Objetivo da aplicação e problema que resolve (com evidência: docstring, descrição do OpenAPI, README, nome dos módulos).
- Lista de funcionalidades principais, cada uma com referência a arquivo:linha do handler ou use case correspondente.
- Regras de negócio relevantes encontradas no código (validações, condições de erro, transformação de dados) — cite a linha exata.
- Um ou dois exemplos concretos de fluxo, em prosa.

Não liste classes/métodos aqui — isso vai na Visão técnica.

## Visão técnica

Responde "como o sistema funciona por dentro":
- Tipo de aplicação (API REST, GraphQL, worker, consumer, producer, CLI, biblioteca, web app, batch, microsserviço, monólito, lambda/serverless, orientada a eventos, outro) — deduza da estrutura real, não do nome da pasta.
- Arquitetura identificada (camadas, padrões — Clean Architecture, MVC, hexagonal, o que for real) com um diagrama de diretórios em bloco de código.
- Fluxo de execução típico, em prosa, citando arquivos reais.
- Comunicação entre componentes (DI, filas internas, event bus).
- Sub-seções conforme aplicável ao projeto, cada uma dizendo "não identificado" quando não houver evidência: Bancos de dados, Cache, Filas/Tópicos, Serviços externos, Storage, Autenticação/Autorização, Observabilidade (logs/métricas/tracing), Resiliência (retry/circuit breaker/timeout), Tratamento de erros, Processamento assíncrono, Jobs agendados.

### APIs expostas (sub-seção de Visão técnica)

Se houver API HTTP: tabela `Método | Endpoint | Descrição | Autenticação | Entrada | Saída`, um endpoint por linha, todos confirmados no código (roteador + handler + use case, não apenas o roteador). Se a autenticação da rota não puder ser confirmada por um dependency/middleware real, escreva "Nenhuma identificada" — nunca assuma que existe.

Se não houver API HTTP: escreva literalmente "Não foram identificadas APIs HTTP expostas por este projeto." e documente o mecanismo de entrada real (tópico Kafka consumido, fila RabbitMQ consumida, cron, CLI, arquivo processado, evento recebido).

## Estrutura de diretórios

Árvore em bloco de código com os diretórios/arquivos relevantes reais (não um exemplo genérico), seguida de uma tabela `Diretório | Responsabilidade`. A responsabilidade é validada lendo o conteúdo, nunca inferida só pelo nome.

## Dependências do projeto

- **Stack principal**: linguagem, versão (se determinável — diga explicitamente quando não for), framework e versão, runtime, imagem-base/SO se houver Dockerfile.
- **Bibliotecas**: tabela `Tecnologia/Biblioteca | Versão | Finalidade`, só as que têm peso arquitetural/funcional (framework web, ORM, driver de banco, cliente HTTP, cliente de mensageria, SDKs de cloud, libs de auth/logging/observabilidade/testes/serialização/validação/config). Não listar toda dependência transitiva do lockfile.
- **Infraestrutura**: Docker, Docker Compose, Kubernetes, Helm, Terraform, cloud provider, CI/CD (GitHub Actions/Jenkins/ArgoCD/etc.) — cada um "identificado" com arquivo de evidência ou "não identificado".

## Diagrama de sequência / Diagrama de arquitetura

Ver `SKILL.md`, seção "Diagramas Mermaid" — gerados com os scripts deste skill (Python) ou montados à mão seguindo o mesmo formato (outras linguagens). Sempre embutidos como blocos ` ```mermaid ` renderizáveis, nunca apenas descritos em prosa. Inclua uma frase dizendo como foram gerados/revisados e o que foi omitido de propósito (middlewares, auth global — são transversais).

## Pontos de atenção

Tabela `Ponto | Evidência | Impacto | Prioridade (Alta/Média/Baixa) | Sugestão`. Cada linha precisa de uma evidência real (arquivo:linha ou trecho). Categorias a considerar, só quando houver achado real: riscos técnicos, fragilidades arquiteturais, gargalos, escalabilidade, acoplamento excessivo, duplicação, complexidade desnecessária, tratamento de erros falho, observabilidade insuficiente, segurança (configuração sensível, secret exposto, dependência desatualizada), cobertura de testes, single point of failure, idempotência, concorrência, transação, performance, débito técnico.

Não transforme toda escolha de implementação diferente do "ideal" em um ponto de atenção — só o que tem justificativa técnica concreta.

## Como executar o projeto localmente

Sub-seções: Pré-requisitos, Obtendo o projeto, Instalação, Configuração (tabela de variáveis de ambiente — nunca copiar valores reais de secret, só sinalizar em Pontos de atenção se houver secret versionado), Banco de dados, Execução, Testes, Build, Docker. Cada uma só com comandos realmente encontrados no projeto (scripts, README, Makefile, package.json, CI) — nunca um comando genérico inventado para a tecnologia.

## Integrações externas identificadas

Tabela `Sistema | Tipo | Finalidade | Direção`, uma linha por integração real encontrada no código (não repetir os exemplos deste template).

## Entradas e saídas

Prosa curta listando entradas (HTTP, fila consumida, arquivo, CLI, cron, evento, webhook) e saídas (resposta HTTP, banco, fila publicada, API externa, arquivo, storage, logs, eventos) realmente identificadas.

## Qualidade da análise (checklist)

Checklist com `[x]` feito, `[ ]` não identificado/não aplicável, `[~]` parcial (com nota do porquê). Ver lista completa no `SKILL.md`.

## Resumo final

Sete itens numerados: arquivo criado/atualizado; tipo de aplicação; stack principal; principais integrações; quantidade de APIs/endpoints (se aplicável); principais pontos de atenção; informações que não puderam ser determinadas.
