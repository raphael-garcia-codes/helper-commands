
# 📘 Guia Completo de Comandos CLI do Node.js

Este documento reúne os principais comandos utilizados no **Node.js**, **npm** e **npx** via linha de comando, com exemplos práticos.  
Os parâmetros variáveis são representados por `<<param>>`.

---

## 🔹 Node.js (node)

### Executar um arquivo JavaScript
Executa um arquivo JavaScript usando o interpretador do Node.js.
```bash
node <<arquivo.js>>
```

### Executar código JavaScript diretamente no terminal
Permite executar código JavaScript inline.
```bash
node -e "<<codigo_js>>"
```

### Iniciar o REPL do Node.js
Abre o modo interativo (Read-Eval-Print Loop).
```bash
node
```

### Exibir versão do Node.js
Mostra a versão instalada do Node.js.
```bash
node -v
```

---

## 🔹 npm (Node Package Manager)

### Inicializar um projeto
Cria o arquivo `package.json` de forma interativa.
```bash
npm init
```

### Inicializar projeto com valores padrão
Cria o `package.json` automaticamente.
```bash
npm init -y
```

### Instalar dependências do projeto
Instala todas as dependências listadas no `package.json`.
```bash
npm install
```

### Instalar um pacote
Instala um pacote no projeto.
```bash
npm install <<pacote>>
```

### Instalar pacote como dependência de desenvolvimento
```bash
npm install <<pacote>> --save-dev
```

### Instalar pacote globalmente
```bash
npm install -g <<pacote>>
```

### Remover um pacote
```bash
npm uninstall <<pacote>>
```

### Atualizar pacotes
Atualiza dependências do projeto.
```bash
npm update
```

### Listar pacotes instalados
```bash
npm list
```

### Listar pacotes globais
```bash
npm list -g --depth=0
```

### Executar script definido no package.json
```bash
npm run <<script>>
```

### Executar script padrão
```bash
npm start
```

### Executar testes
```bash
npm test
```

### Limpar cache do npm
```bash
npm cache clean --force
```

### Ver informações de um pacote
```bash
npm info <<pacote>>
```

---

## 🔹 npx

### Executar pacote sem instalar
Executa um pacote diretamente do repositório.
```bash
npx <<pacote>>
```

### Executar versão específica de um pacote
```bash
npx <<pacote>>@<<versao>>
```

### Executar script local
```bash
npx <<script>>
```

---

## 🔹 Gerenciamento de Versões e Diagnóstico

### Ver versões de Node, npm e dependências
```bash
npm version
```

### Ver configuração atual do npm
```bash
npm config list
```

### Definir configuração do npm
```bash
npm config set <<chave>> <<valor>>
```

### Auditar vulnerabilidades
Analisa falhas de segurança nas dependências.
```bash
npm audit
```

### Corrigir vulnerabilidades automaticamente
```bash
npm audit fix
```

---

## 🔹 Utilitários

### Ver ajuda de um comando
```bash
npm help <<comando>>
```

### Abrir documentação de um pacote no navegador
```bash
npm docs <<pacote>>
```

### Ver dependências desatualizadas
```bash
npm outdated
```

---

📌 **Observação**:  
Este arquivo foi criado para fins de estudo e referência rápida.  
Recomenda-se cautela ao usar comandos que alteram dependências ou o ambiente global.
