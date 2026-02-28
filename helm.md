# Helm – Guia Completo de Comandos

Este documento reúne **todos os principais comandos do Helm**, organizados por categoria, com **exemplos práticos**. Os parâmetros estão representados no formato `<<param>>` para facilitar a adaptação ao seu projeto.

---

## 📦 Gerenciamento de Charts

### Criar um novo chart
Cria a estrutura básica de um chart Helm.
```bash
helm create <<chart_name>>
```

### Empacotar um chart
Gera um arquivo `.tgz` a partir do chart.
```bash
helm package <<chart_path>>
```

### Validar a estrutura do chart
Verifica se o chart está corretamente configurado.
```bash
helm lint <<chart_path>>
```

### Exibir informações do chart
Mostra detalhes como versão, valores e templates.
```bash
helm show all <<chart>>
helm show values <<chart>>
helm show chart <<chart>>
helm show readme <<chart>>
```

---

## 🚀 Instalação e Deploy

### Instalar um release
Instala um chart no cluster Kubernetes.
```bash
helm install <<release_name>> <<chart>>
```

### Instalar definindo namespace
```bash
helm install <<release_name>> <<chart>> --namespace <<namespace>>
```

### Instalar com valores customizados
```bash
helm install <<release_name>> <<chart>> -f <<values_file.yaml>>
```

### Instalar sobrescrevendo valores via CLI
```bash
helm install <<release_name>> <<chart>> --set <<key>>=<<value>>
```

### Simular instalação (dry-run)
```bash
helm install <<release_name>> <<chart>> --dry-run --debug
```

---

## 🔄 Atualização e Rollback

### Atualizar um release existente
```bash
helm upgrade <<release_name>> <<chart>>
```

### Atualizar reutilizando valores atuais
```bash
helm upgrade <<release_name>> <<chart>> --reuse-values
```

### Atualizar com valores adicionais
```bash
helm upgrade <<release_name>> <<chart>> -f <<values_file.yaml>>
```

### Listar histórico de revisões
```bash
helm history <<release_name>>
```

### Fazer rollback para uma revisão específica
```bash
helm rollback <<release_name>> <<revision>>
```

---

## 🗑️ Remoção de Releases

### Desinstalar um release
```bash
helm uninstall <<release_name>>
```

### Desinstalar de um namespace específico
```bash
helm uninstall <<release_name>> --namespace <<namespace>>
```

---

## 📋 Listagem e Consulta

### Listar releases instalados
```bash
helm list
```

### Listar releases em todos os namespaces
```bash
helm list --all-namespaces
```

### Listar releases incluindo os desinstalados
```bash
helm list --all
```

### Ver status de um release
```bash
helm status <<release_name>>
```

### Obter valores aplicados em um release
```bash
helm get values <<release_name>>
```

### Obter manifestos Kubernetes gerados
```bash
helm get manifest <<release_name>>
```

### Obter todas as informações do release
```bash
helm get all <<release_name>>
```

---

## 🌐 Repositórios (Chart Repos)

### Adicionar repositório
```bash
helm repo add <<repo_name>> <<repo_url>>
```

### Atualizar índices dos repositórios
```bash
helm repo update
```

### Listar repositórios configurados
```bash
helm repo list
```

### Remover repositório
```bash
helm repo remove <<repo_name>>
```

### Buscar charts em repositórios
```bash
helm search repo <<chart_name>>
```

### Buscar charts localmente
```bash
helm search hub <<keyword>>
```

---

## 🧪 Template e Debug

### Renderizar templates localmente
Gera os manifestos Kubernetes sem aplicar no cluster.
```bash
helm template <<release_name>> <<chart>>
```

### Renderizar com valores customizados
```bash
helm template <<release_name>> <<chart>> -f <<values_file.yaml>>
```

### Ativar modo debug
```bash
helm template <<release_name>> <<chart>> --debug
```

---

## 🔐 Plugins

### Listar plugins instalados
```bash
helm plugin list
```

### Instalar um plugin
```bash
helm plugin install <<plugin_url>>
```

### Atualizar um plugin
```bash
helm plugin update <<plugin_name>>
```

### Remover um plugin
```bash
helm plugin remove <<plugin_name>>
```

---

## ⚙️ Configuração e Ambiente

### Exibir variáveis de ambiente do Helm
```bash
helm env
```

### Ver versão do Helm
```bash
helm version
```

---

## 🧩 Dependências

### Atualizar dependências do chart
```bash
helm dependency update <<chart_path>>
```

### Listar dependências
```bash
helm dependency list <<chart_path>>
```

### Construir dependências
```bash
helm dependency build <<chart_path>>
```

---

## 📌 Dicas de Organização para Repositório GitHub

- Separar diretórios por ambiente (`dev`, `hml`, `prod`)
- Manter `values.yaml` versionados
- Criar README.md por chart
- Versionar charts com `Chart.yaml`
- Utilizar `helm lint` em pipelines CI

---

📘 **Este arquivo pode ser usado como referência completa ou documentação oficial do seu repositório Helm.**

