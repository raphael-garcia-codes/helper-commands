# Guia Completo de Comandos `kubectl`

Este documento reúne **comandos do kubectl**, organizados por categoria, com **exemplos práticos**.  
Os parâmetros variáveis estão representados como `<<param>>`.

⚠️ **ALERTA DE SEGURANÇA**  
Comandos que **alteram o estado do cluster** (criação, alteração ou exclusão de recursos) estão **destacados como PERIGOSOS**.  
A maioria dos comandos abaixo é apenas de **consulta/listagem**.

---

## 1. Configuração e Contexto do Cluster

### Exibe informações gerais do cluster
```bash
kubectl cluster-info
```

### Mostra a versão do cliente e do servidor Kubernetes
```bash
kubectl version
```

### Lista contextos disponíveis no kubeconfig
```bash
kubectl config get-contexts
```

### Define o contexto atual (⚠️ altera o alvo dos comandos)
```bash
kubectl config use-context <<context-name>>
```

### Exibe o contexto atualmente em uso
```bash
kubectl config current-context
```

---

## 2. Consulta e Listagem de Recursos (SEGUROS)

### Lista todos os namespaces
```bash
kubectl get namespaces
```

### Lista pods em um namespace
```bash
kubectl get pods -n <<namespace>>
```

### Lista todos os pods de todos os namespaces
```bash
kubectl get pods --all-namespaces
```

### Lista deployments
```bash
kubectl get deployments -n <<namespace>>
```

### Lista services
```bash
kubectl get services -n <<namespace>>
```

### Lista nodes do cluster
```bash
kubectl get nodes
```

### Lista recursos com mais detalhes
```bash
kubectl get pods -o wide
```

### Lista recursos em formato YAML
```bash
kubectl get pod <<pod-name>> -n <<namespace>> -o yaml
```

---

## 3. Descrição Detalhada de Recursos (SEGUROS)

### Mostra detalhes completos de um pod
```bash
kubectl describe pod <<pod-name>> -n <<namespace>>
```

### Mostra detalhes de um node
```bash
kubectl describe node <<node-name>>
```

### Mostra detalhes de um service
```bash
kubectl describe service <<service-name>> -n <<namespace>>
```

---

## 4. Logs e Debug (SEGUROS)

### Exibe logs de um pod
```bash
kubectl logs <<pod-name>> -n <<namespace>>
```

### Exibe logs de um container específico
```bash
kubectl logs <<pod-name>> -c <<container-name>> -n <<namespace>>
```

### Exibe logs em tempo real
```bash
kubectl logs -f <<pod-name>> -n <<namespace>>
```

### Executa um comando dentro de um container
```bash
kubectl exec -it <<pod-name>> -n <<namespace>> -- <<command>>
```

---

## 5. Criação e Aplicação de Recursos (⚠️ PERIGOSOS)

### Cria ou atualiza recursos a partir de um arquivo YAML
⚠️ **Altera o estado do cluster**
```bash
kubectl apply -f <<arquivo.yaml>>
```

### Cria recursos sem controle de versionamento
⚠️ **Pode sobrescrever configurações**
```bash
kubectl create -f <<arquivo.yaml>>
```

### Cria um namespace
⚠️ **Modifica o cluster**
```bash
kubectl create namespace <<namespace>>
```

---

## 6. Atualização e Escala (⚠️ PERIGOSOS)

### Escala um deployment
⚠️ **Impacta carga e disponibilidade**
```bash
kubectl scale deployment <<deployment-name>> --replicas=<<qtd>> -n <<namespace>>
```

### Edita um recurso diretamente no editor
⚠️ **Mudança direta em produção**
```bash
kubectl edit deployment <<deployment-name>> -n <<namespace>>
```

### Aplica patch em um recurso
⚠️ **Alteração pontual e imediata**
```bash
kubectl patch deployment <<deployment-name>> -n <<namespace>> -p '<<json>>'
```

---

## 7. Exclusão de Recursos (⚠️ EXTREMAMENTE PERIGOSOS)

### Remove um pod
⚠️ **Interrupção imediata**
```bash
kubectl delete pod <<pod-name>> -n <<namespace>>
```

### Remove um deployment
⚠️ **Remove aplicação inteira**
```bash
kubectl delete deployment <<deployment-name>> -n <<namespace>>
```

### Remove recursos definidos em um arquivo
⚠️ **Pode apagar múltiplos objetos**
```bash
kubectl delete -f <<arquivo.yaml>>
```

### Remove um namespace inteiro
🚨 **ALTÍSSIMO RISCO – remove TODOS os recursos**
```bash
kubectl delete namespace <<namespace>>
```

---

## 8. Port-Forward e Acesso Local (SEGUROS)

### Encaminha porta local para um pod
```bash
kubectl port-forward pod/<<pod-name>> <<porta-local>>:<<porta-pod>> -n <<namespace>>
```

### Encaminha porta para um service
```bash
kubectl port-forward svc/<<service-name>> <<porta-local>>:<<porta-service>> -n <<namespace>>
```

---

## 9. Contexto Avançado e Segurança

### Verifica permissões do usuário atual
```bash
kubectl auth can-i <<verbo>> <<recurso>> -n <<namespace>>
```

### Lista todos os recursos disponíveis na API
```bash
kubectl api-resources
```

### Lista versões da API
```bash
kubectl api-versions
```

---

## 10. Dry-Run e Validação (RECOMENDADO)

### Simula criação sem aplicar no cluster
```bash
kubectl apply -f <<arquivo.yaml>> --dry-run=client
```

### Valida estrutura do manifesto
```bash
kubectl apply -f <<arquivo.yaml>> --validate=true
```

---

## Convenção de Risco

- ✅ **Seguro**: apenas leitura / consulta
- ⚠️ **Perigoso**: altera recursos existentes
- 🚨 **Crítico**: pode causar indisponibilidade ou perda de dados

---

📌 **Sugestão para o GitHub**  
Você pode dividir este guia em arquivos:
- `01-consulta.md`
- `02-debug.md`
- `03-alteracoes.md`
- `04-exclusoes.md`

Se quiser, posso **organizar isso em README.md**, **gerar cheatsheet**, ou **criar versão resumida para prova/certificação (CKA/CKAD)**.

