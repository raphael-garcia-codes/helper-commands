# CLI do .NET / C# — Guia Completo de Comandos

Este arquivo documenta os principais comandos utilizados para desenvolvimento em **C# via linha de comando**, usando o **.NET CLI (`dotnet`)**.  
Os parâmetros estão representados no formato `<<param>>` para facilitar estudo e referência.

---

## 🔧 Instalação e Informações Básicas

### Exibe a versão instalada do SDK do .NET
```bash
dotnet --version
```

### Lista todos os SDKs instalados
```bash
dotnet --list-sdks
```

### Lista todos os runtimes instalados
```bash
dotnet --list-runtimes
```

### Exibe ajuda geral do CLI
```bash
dotnet --help
```

---

## 📦 Criação de Projetos e Soluções

### Cria uma nova solução
```bash
dotnet new sln -n <<NomeDaSolucao>>
```

### Cria um novo projeto de console
```bash
dotnet new console -n <<NomeDoProjeto>>
```

### Cria um projeto Web API
```bash
dotnet new webapi -n <<NomeDoProjeto>>
```

### Cria um projeto de biblioteca de classes
```bash
dotnet new classlib -n <<NomeDoProjeto>>
```

### Lista templates disponíveis
```bash
dotnet new list
```

---

## 📁 Gerenciamento de Soluções

### Adiciona um projeto à solução
```bash
dotnet sln <<Solucao.sln>> add <<CaminhoDoProjeto.csproj>>
```

### Remove um projeto da solução
```bash
dotnet sln <<Solucao.sln>> remove <<CaminhoDoProjeto.csproj>>
```

### Lista projetos da solução
```bash
dotnet sln <<Solucao.sln>> list
```

---

## 📚 Gerenciamento de Dependências (NuGet)

### Adiciona um pacote NuGet ao projeto
```bash
dotnet add package <<NomeDoPacote>> --version <<Versao>>
```

### Remove um pacote NuGet
```bash
dotnet remove package <<NomeDoPacote>>
```

### Lista pacotes instalados
```bash
dotnet list package
```

### Restaura dependências
```bash
dotnet restore
```

---

## ⚙️ Build, Run e Testes

### Compila o projeto
```bash
dotnet build
```

### Compila em modo Release
```bash
dotnet build -c Release
```

### Executa a aplicação
```bash
dotnet run
```

### Executa em ambiente específico
```bash
dotnet run --environment <<Ambiente>>
```

### Executa testes automatizados
```bash
dotnet test
```

---

## 🚀 Publicação e Deploy

### Publica a aplicação
```bash
dotnet publish
```

### Publica em modo Release
```bash
dotnet publish -c Release
```

### Publica para runtime específico
```bash
dotnet publish -r <<runtime>> --self-contained <<true|false>>
```

---

## 🧹 Manutenção e Utilitários

### Limpa arquivos de build
```bash
dotnet clean
```

### Verifica ferramentas instaladas globalmente
```bash
dotnet tool list -g
```

### Instala ferramenta global
```bash
dotnet tool install -g <<NomeDaFerramenta>>
```

### Atualiza ferramenta global
```bash
dotnet tool update -g <<NomeDaFerramenta>>
```

### Remove ferramenta global
```bash
dotnet tool uninstall -g <<NomeDaFerramenta>>
```

---

## 🛠️ Ferramentas e Diagnóstico

### Executa análise de código
```bash
dotnet format
```

### Gera cobertura de testes (exemplo)
```bash
dotnet test /p:CollectCoverage=true
```

### Cria arquivo de lock de dependências
```bash
dotnet restore --use-lock-file
```

---

## 📌 Observações Finais

- Todos os comandos devem ser executados no diretório correto do projeto ou solução.
- Este arquivo pode ser expandido com comandos específicos de ferramentas como EF Core, Docker, Azure, etc.

---

📘 **Autor:** Raphael Garcia  
📂 **Uso:** Referência rápida para estudos, projetos e concursos
