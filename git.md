# Guia Completo de Comandos Git (com exemplos)

Este documento reúne **os principais comandos do Git**, organizados por categoria, com:
- Explicação breve em português
- Exemplos práticos
- Parâmetros genéricos no formato `<<param>>`

---

## 1. Configuração Inicial

### git config
Configura opções globais ou locais do Git.
```bash
git config --global user.name "<<nome_do_usuario>>"
git config --global user.email "<<email_do_usuario>>"
git config --list
```

---

## 2. Criação e Inicialização de Repositórios

### git init
Inicializa um novo repositório Git.
```bash
git init
git init <<diretorio>>
```

### git clone
Clona um repositório remoto para a máquina local.
```bash
git clone <<url_do_repositorio>>
git clone <<url>> <<diretorio_destino>>
```

---

## 3. Status e Histórico

### git status
Mostra o estado atual do repositório.
```bash
git status
git status -s
```

### git log
Exibe o histórico de commits.
```bash
git log
git log --oneline
git log --graph --all
```

---

## 4. Controle de Arquivos

### git add
Adiciona arquivos à área de stage.
```bash
git add <<arquivo>>
git add .
```

### git restore
Restaura arquivos modificados.
```bash
git restore <<arquivo>>
git restore --staged <<arquivo>>
```

### git rm
Remove arquivos do repositório.
```bash
git rm <<arquivo>>
git rm -r <<diretorio>>
```

---

## 5. Commits

### git commit
Cria um commit com as alterações em stage.
```bash
git commit -m "<<mensagem_do_commit>>"
git commit --amend
```

---

## 6. Branches

### git branch
Lista, cria ou remove branches.
```bash
git branch
git branch <<nome_branch>>
git branch -d <<nome_branch>>
```

### git checkout
Troca de branch ou restaura arquivos.
```bash
git checkout <<nome_branch>>
git checkout -b <<nova_branch>>
```

### git switch
Alternativa moderna ao checkout para branches.
```bash
git switch <<nome_branch>>
git switch -c <<nova_branch>>
```

---

## 7. Merge e Rebase

### git merge
Mescla branches.
```bash
git merge <<branch_origem>>
```

### git rebase
Reaplica commits em outra base.
```bash
git rebase <<branch_base>>
git rebase --continue
git rebase --abort
```

---

## 8. Repositórios Remotos

### git remote
Gerencia repositórios remotos.
```bash
git remote -v
git remote add origin <<url>>
```

### git fetch
Busca alterações do remoto sem mesclar.
```bash
git fetch
git fetch <<remote>>
```

### git pull
Busca e mescla alterações do remoto.
```bash
git pull
git pull <<remote>> <<branch>>
```

### git push
Envia commits para o repositório remoto.
```bash
git push
git push -u origin <<branch>>
```

---

## 9. Diferenças e Inspeção

### git diff
Mostra diferenças entre versões.
```bash
git diff
git diff <<commit1>> <<commit2>>
```

### git show
Exibe detalhes de um commit.
```bash
git show <<hash_commit>>
```

---

## 10. Stash

### git stash
Salva alterações temporariamente.
```bash
git stash
git stash list
git stash apply
git stash drop
```

---

## 11. Reset e Revert

### git reset
Desfaz commits ou alterações.
```bash
git reset --soft <<commit>>
git reset --mixed <<commit>>
git reset --hard <<commit>>
```

### git revert
Cria um novo commit desfazendo outro.
```bash
git revert <<hash_commit>>
```

---

## 12. Tags

### git tag
Cria e gerencia tags.
```bash
git tag
git tag <<nome_tag>>
git tag -a <<nome_tag>> -m "<<mensagem>>"
```

---

## 13. Limpeza e Manutenção

### git clean
Remove arquivos não rastreados.
```bash
git clean -n
git clean -f
```

### git gc
Otimiza o repositório.
```bash
git gc
```

---

## 14. Ajuda

### git help
Exibe ajuda de comandos.
```bash
git help
git help <<comando>>
```

---

## Observação Final
Este arquivo pode ser usado como **material de estudo**, **consulta rápida** ou **base para documentação interna** em projetos versionados com Git.
