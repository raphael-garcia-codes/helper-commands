# Go CLI – Guia Completo de Comandos

Este documento reúne **todos os principais comandos da CLI do Go (golang)**, com exemplos práticos.
Os parâmetros variáveis estão descritos no formato `<<param>>`.

---

## go version
Exibe a versão instalada do Go.
```bash
go version
```

---

## go env
Exibe ou define variáveis de ambiente do Go.
```bash
go env
go env <<VAR>>
go env <<VAR>>=<<valor>>
```

---

## go help
Exibe ajuda geral ou de um comando específico.
```bash
go help
go help <<comando>>
```

---

## go mod init
Inicializa um novo módulo Go.
```bash
go mod init <<module_name>>
```

---

## go mod tidy
Remove dependências não utilizadas e adiciona as necessárias.
```bash
go mod tidy
```

---

## go mod download
Baixa dependências do módulo.
```bash
go mod download
```

---

## go mod graph
Exibe o grafo de dependências.
```bash
go mod graph
```

---

## go mod vendor
Cria diretório vendor com dependências.
```bash
go mod vendor
```

---

## go get
Baixa ou atualiza dependências.
```bash
go get <<package>>
go get <<package>>@<<version>>
```

---

## go list
Lista pacotes ou módulos.
```bash
go list
go list ./...
```

---

## go build
Compila pacotes ou projetos.
```bash
go build
go build <<package>>
go build -o <<output>> <<package>>
```

---

## go install
Compila e instala binários.
```bash
go install <<package>>
go install <<package>>@<<version>>
```

---

## go run
Compila e executa o código.
```bash
go run <<file.go>>
go run <<package>>
```

---

## go test
Executa testes.
```bash
go test
go test ./...
go test -v
go test -run <<TestName>>
```

---

## go test -cover
Executa testes com cobertura.
```bash
go test -cover
go test -coverprofile=<<file>>
```

---

## go fmt
Formata o código-fonte.
```bash
go fmt
go fmt ./...
```

---

## go vet
Analisa possíveis erros no código.
```bash
go vet
go vet ./...
```

---

## go clean
Remove arquivos gerados.
```bash
go clean
go clean -modcache
```

---

## go doc
Exibe documentação de pacotes.
```bash
go doc <<package>>
go doc <<package>>.<<symbol>>
```

---

## go generate
Executa comandos definidos em diretivas go:generate.
```bash
go generate
go generate ./...
```

---

## go tool
Executa ferramentas do Go.
```bash
go tool
go tool <<toolname>>
```

---

## go tool compile
Compila arquivos manualmente (uso avançado).
```bash
go tool compile <<file.go>>
```

---

## go tool cover
Analisa cobertura de testes.
```bash
go tool cover -func=<<coverprofile>>
go tool cover -html=<<coverprofile>>
```

---

## go work init
Inicializa workspace (Go 1.18+).
```bash
go work init <<module_paths>>
```

---

## go work use
Adiciona módulos ao workspace.
```bash
go work use <<module_path>>
```

---

## go work sync
Sincroniza dependências do workspace.
```bash
go work sync
```

---

## go bug
Abre página para reportar bugs.
```bash
go bug
```

---

## go fix
Atualiza código para novas versões do Go.
```bash
go fix <<package>>
```

---

## go clean -i
⚠️ **Perigoso**: remove binários instalados.
```bash
go clean -i
```

---

## go env -w
⚠️ **Perigoso**: altera variáveis de ambiente globalmente.
```bash
go env -w <<VAR>>=<<valor>>
```

---

## go mod edit
Edita manualmente o go.mod.
```bash
go mod edit -module <<name>>
go mod edit -require <<pkg>>@<<version>>
```

---

## go mod why
Explica por que um módulo é necessário.
```bash
go mod why <<module>>
```

---

## go mod verify
Verifica integridade das dependências.
```bash
go mod verify
```

---

## go mod init + build (exemplo completo)
Exemplo de fluxo básico:
```bash
go mod init <<module>>
go mod tidy
go build
go run main.go
```

---

## Observações Finais
- A maioria dos comandos é segura (leitura/compilação).
- ⚠️ Comandos destacados alteram o ambiente ou removem arquivos.
- Ideal para uso em automações, CI/CD e desenvolvimento local.

---

📌 **Sugestão**: versionar este arquivo como `go-cli.md` no seu repositório GitHub.
