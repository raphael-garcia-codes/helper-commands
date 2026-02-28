# 📜 Guia Completo de Comandos Shell (Bash)

Este arquivo reúne os **principais comandos de shell script (Bash/Linux)** organizados por categoria.  
Cada comando contém:
- Uma **breve explicação em português**
- Um **exemplo genérico**, onde os parâmetros são representados por `<<param>>`

> 📌 Objetivo: servir como **repositório de referência** para estudos, automação e escrita de scripts.

---

## 🗂️ 1. Navegação e Sistema de Arquivos

### `pwd`
Exibe o diretório atual.
```sh
pwd
```

### `ls`
Lista arquivos e diretórios.
```sh
ls <<opcoes>> <<diretorio>>
```

### `cd`
Altera o diretório atual.
```sh
cd <<caminho>>
```

### `tree`
Exibe a estrutura de diretórios em forma de árvore.
```sh
tree <<diretorio>>
```

---

## 📁 2. Manipulação de Arquivos e Diretórios

### `touch`
Cria um arquivo vazio.
```sh
touch <<arquivo>>
```

### `mkdir`
Cria um diretório.
```sh
mkdir <<opcoes>> <<diretorio>>
```

### `rm`
Remove arquivos ou diretórios.
```sh
rm <<opcoes>> <<arquivo_ou_diretorio>>
```

### `cp`
Copia arquivos ou diretórios.
```sh
cp <<opcoes>> <<origem>> <<destino>>
```

### `mv`
Move ou renomeia arquivos e diretórios.
```sh
mv <<origem>> <<destino>>
```

### `ln`
Cria links simbólicos ou físicos.
```sh
ln <<opcoes>> <<origem>> <<link>>
```

---

## 📄 3. Visualização de Arquivos

### `cat`
Exibe o conteúdo de um arquivo.
```sh
cat <<arquivo>>
```

### `less`
Visualiza arquivos com paginação.
```sh
less <<arquivo>>
```

### `head`
Exibe as primeiras linhas de um arquivo.
```sh
head <<opcoes>> <<arquivo>>
```

### `tail`
Exibe as últimas linhas de um arquivo.
```sh
tail <<opcoes>> <<arquivo>>
```

---

## 🔍 4. Busca e Filtros de Texto

### `grep`
Busca padrões em arquivos ou saída de comandos.
```sh
grep <<opcoes>> "<<padrao>>" <<arquivo>>
```

### `find`
Localiza arquivos e diretórios.
```sh
find <<caminho>> <<opcoes>>
```

### `sed`
Edita texto em fluxo (stream editor).
```sh
sed <<opcoes>> '<<expressao>>' <<arquivo>>
```

### `awk`
Processa e manipula texto estruturado.
```sh
awk '<<script>>' <<arquivo>>
```

---

## 🔐 5. Permissões e Propriedade

### `chmod`
Altera permissões de arquivos.
```sh
chmod <<permissao>> <<arquivo>>
```

### `chown`
Altera o dono do arquivo.
```sh
chown <<usuario>>:<<grupo>> <<arquivo>>
```

### `chgrp`
Altera o grupo do arquivo.
```sh
chgrp <<grupo>> <<arquivo>>
```

---

## ⚙️ 6. Processos e Sistema

### `ps`
Lista processos em execução.
```sh
ps <<opcoes>>
```

### `top`
Exibe processos em tempo real.
```sh
top <<opcoes>>
```

### `htop`
Visualização interativa de processos.
```sh
htop
```

### `kill`
Encerra processos.
```sh
kill <<sinal>> <<pid>>
```

### `uptime`
Mostra o tempo de atividade do sistema.
```sh
uptime
```

---

## 🌐 7. Rede

### `ping`
Testa conectividade com um host.
```sh
ping <<host>>
```

### `curl`
Realiza requisições HTTP.
```sh
curl <<opcoes>> <<url>>
```

### `wget`
Baixa arquivos da internet.
```sh
wget <<opcoes>> <<url>>
```

### `netstat`
Exibe conexões de rede.
```sh
netstat <<opcoes>>
```

### `ss`
Exibe sockets ativos.
```sh
ss <<opcoes>>
```

---

## 📦 8. Compactação e Arquivamento

### `tar`
Cria ou extrai arquivos compactados.
```sh
tar <<opcoes>> <<arquivo.tar>> <<origem>>
```

### `zip`
Compacta arquivos em formato ZIP.
```sh
zip <<opcoes>> <<arquivo.zip>> <<arquivos>>
```

### `unzip`
Extrai arquivos ZIP.
```sh
unzip <<arquivo.zip>>
```

---

## 🧠 9. Variáveis, Entrada e Saída

### `echo`
Exibe texto ou variáveis.
```sh
echo "<<texto>>"
```

### `read`
Lê entrada do usuário.
```sh
read <<variavel>>
```

### `export`
Define variável de ambiente.
```sh
export <<variavel>>=<<valor>>
```

---

## 🔁 10. Estruturas de Controle (Shell Script)

### `if`
Executa comandos com base em condição.
```sh
if [ <<condicao>> ]; then
  <<comandos>>
fi
```

### `for`
Executa loop iterativo.
```sh
for <<variavel>> in <<lista>>; do
  <<comandos>>
done
```

### `while`
Executa loop enquanto condição for verdadeira.
```sh
while [ <<condicao>> ]; do
  <<comandos>>
done
```

### `case`
Estrutura de múltiplas condições.
```sh
case <<variavel>> in
  <<padrao>>)
    <<comandos>>
    ;;
esac
```

---

## 🛠️ 11. Utilitários Diversos

### `date`
Exibe ou formata data e hora.
```sh
date <<formato>>
```

### `watch`
Executa comando periodicamente.
```sh
watch <<opcoes>> <<comando>>
```

### `history`
Exibe histórico de comandos.
```sh
history
```

### `alias`
Cria atalhos para comandos.
```sh
alias <<nome>>='<<comando>>'
```

---

## ✅ Conclusão

Este guia serve como **base sólida para scripts Bash**, estudos e automação de tarefas.  
Você pode expandir este arquivo adicionando:
- Exemplos reais
- Boas práticas
- Tratamento de erros (`set -e`, `trap`)
- Scripts completos

---

📌 **Sugestão de nome do arquivo:** `shellscript-comandos.md`

