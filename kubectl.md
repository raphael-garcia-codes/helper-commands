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


COMANDOS KUBECTL:
kubectl config current-context
kubectl config get-contexts
kubectl config use-context arn:aws:eks:us-west-2:665053502207:cluster/cluster-eks-hml-default
kubectl config use-context arn:aws:eks:sa-east-1:732207930936:cluster/cluster-eks-prd
kubectl get nodes
kubectl get namespaces
kubectl get pods -n open-banking
kubectl get deployments -n open-banking
kubectl exec -it loan-opf-communication-primary-87bf697d8-c7lx5 -n loans --container loan-opf-communication -- /bin/sh
kubectl get pods -n open-banking | Select-String "data-reception-bff"
kubectl port-forward pods/data-reception-bff-primary-7f5675b644-2bmcc 8080:8080 -n open-banking
helm history -n open-banking api-internal-gateway
kubectl get deploy -n open-banking api-internal-gateway
kubectl edit configmaps api-consents -n open-banking
kubectl get canary api-internal-gateway -n open-banking -w
kubectl patch virtualservice api-internal-gateway-primary --type='json' -p='[{"op": "replace", "path": "/spec/http/0/route/0/weight", "value": 0 },{"op": "replace", "path": "/spec/http/0/route/1/weight", "value": 100 }]


# Com filtro (busca um correlation ID / UUID)
kfind open-banking api-payments "7d2654c9-ca19-4a6a-91f1-22789613402a"

# Sem filtro (traz tudo, últimas 1000 linhas por container)
kfind open-banking api-payments

# Valida restart's da aplicação
kcrash open-banking api-consents

# Ver requests e limits configurados nos pods
kubectl describe pod api-consents-primary-7c5864449-45vxz -n open-banking | grep -A 6 "Limits\|Requests"

# Filtrar utilização por app
kubectl top pods -n open-banking | grep api-relying-party

# Ver consumo por container dentro do pod
kubectl top pods -n open-banking --containers | grep api-consents

# Ver memoria e cpu
ktop open-banking api-consents-payments

Se quiser, posso **organizar isso em README.md**, **gerar cheatsheet**, ou **criar versão resumida para prova/certificação (CKA/CKAD)**.







# autocomplete command
source <(kubectl completion bash);
source <(yq shell-completion bash);
# alias
alias k=kubectl;
complete -F __start_kubectl k;
# load kube_ps1 function
source ${HOME}/opt/kube-ps1/kube-ps1.sh;
# set PS1 variable
export PS1='\[\033]0;$TITLEPREFIX:$PWD\007\]\n\[\033[32m\]\u@\h \[\033[35m\]$MSYSTEM `kube_ps1` \[\033[33m\]\w\[\033[36m\]`__git_ps1`\[\033[0m\]\n$ ';

export PATH=${HOME}/opt/bin:${PATH};

export NVM_DIR="$HOME/.nvm"
[ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"  # This loads nvm
[ -s "$NVM_DIR/bash_completion" ] && \. "$NVM_DIR/bash_completion"  # This loads nvm bash_completion

alias l='aws sso login --profile Perfil_l4-732207930936'



# Busca logs em todos os pods de uma aplicação no namespace informado
# Uso: kfind <namespace> <app> [filtro]
# Exemplo: kfind open-banking api-payments "7d2654c9-ca19-4a6a-91f1-22789613402a"
kfind() {
  local namespace=$1
  local app=$2
  local filtro=$3

  if [ -z "$namespace" ] || [ -z "$app" ]; then
    echo "Uso: kfind <namespace> <app> [filtro]"
    return 1
  fi

  for pod in $(kubectl get pods -n "$namespace" --no-headers -o custom-columns=":metadata.name" | grep "$app"); do
    echo "========== POD: $pod =========="
    if [ -z "$filtro" ]; then
      kubectl logs "$pod" -n "$namespace" -c "$app" --tail=1000 2>/dev/null
    else
      kubectl logs "$pod" -n "$namespace" -c "$app" --tail=1000 2>/dev/null | grep "$filtro"
    fi
  done
}



# Investiga restarts de todos os pods de uma aplicação
# Uso: kcrash <namespace> <app>
# Exemplo: kcrash open-banking api-payments
kcrash() {
  local namespace=$1
  local app=$2

  if [ -z "$namespace" ] || [ -z "$app" ]; then
    echo "Uso: kcrash <namespace> <app>"
    return 1
  fi

  for pod in $(kubectl get pods -n "$namespace" --no-headers -o custom-columns=":metadata.name" | grep "$app"); do
    local restarts=$(kubectl get pod "$pod" -n "$namespace" --no-headers | awk '{print $4}')
    echo "========== POD: $pod | Restarts: $restarts =========="

    if [ "$restarts" -gt 0 ] 2>/dev/null; then
      echo ">>> Descrevendo eventos do pod..."
      kubectl describe pod "$pod" -n "$namespace" | grep -A 10 "Last State"

      echo ""
      echo ">>> Logs do container anterior (antes do crash)..."
      kubectl logs "$pod" -n "$namespace" -c "$app" --previous --tail=100 2>/dev/null || echo "Sem logs anteriores disponíveis"
    else
      echo "Sem restarts registrados."
    fi
    echo ""
  done
}


# Mostra configuração e consumo atual de uma aplicação
# Uso: ktop <namespace> <app>
# Exemplo: ktop open-banking api-relying-party
ktop() {
  local namespace=$1
  local app=$2

  if [ -z "$namespace" ] || [ -z "$app" ]; then
    echo "Uso: ktop <namespace> <app>"
    return 1
  fi

  echo "====== CONFIGURAÇÃO (requests/limits) ======"
  for pod in $(kubectl get pods -n "$namespace" --no-headers \
    -o custom-columns=":metadata.name" | grep "$app"); do
    echo ""
    echo "--- POD: $pod ---"
    kubectl get pod "$pod" -n "$namespace" -o json | \
      jq -r '.spec.containers[] |
        "Container: \(.name)\n  CPU    -> request: \(.resources.requests.cpu // "n/a")  |  limit: \(.resources.limits.cpu // "n/a")\n  Memory -> request: \(.resources.requests.memory // "n/a")  |  limit: \(.resources.limits.memory // "n/a")"'
  done

  echo ""
  echo "====== CONSUMO ATUAL ======"
  kubectl top pods -n "$namespace" --containers 2>/dev/null | \
    grep -E "NAME|$app" || \
    echo "⚠️  Metrics Server indisponível."
}


