# 📦 Guia Completo de Comandos Docker e Docker Compose

Este documento reúne **exemplos práticos dos principais comandos Docker e Docker Compose**, com foco em uso cotidiano para desenvolvimento, testes e produção.

Os parâmetros são apresentados no formato `<<param>>` para facilitar a adaptação ao seu projeto.

---

## 🐳 Docker – Comandos Básicos

### Verificar versão do Docker
Verifica a versão instalada do Docker.
```bash
docker --version
```

### Exibir informações do ambiente Docker
Mostra detalhes do daemon, containers, imagens e sistema.
```bash
docker info
```

---

## 📦 Gerenciamento de Imagens

### Listar imagens locais
Exibe todas as imagens disponíveis no host.
```bash
docker images
```

### Baixar uma imagem do Docker Hub
Faz o download de uma imagem específica.
```bash
docker pull <<imagem>>:<<tag>>
```

### Construir uma imagem a partir de um Dockerfile
Cria uma imagem usando o Dockerfile do diretório atual.
```bash
docker build -t <<nome_imagem>>:<<tag>> <<path>>
```

### Remover uma imagem
Remove uma imagem local.
```bash
docker rmi <<imagem>>
```

---

## 📦 Gerenciamento de Containers

### Criar e executar um container
Cria e inicia um container.
```bash
docker run --name <<nome_container>> -p <<porta_host>>:<<porta_container>> -d <<imagem>>
```

### Executar container em modo interativo
Usado para testes e debug.
```bash
docker run -it <<imagem>> <<comando>>
```

### Listar containers em execução
Mostra apenas containers ativos.
```bash
docker ps
```

### Listar todos os containers
Inclui containers parados.
```bash
docker ps -a
```

### Iniciar um container parado
```bash
docker start <<container>>
```

### Parar um container em execução
```bash
docker stop <<container>>
```

### Reiniciar um container
```bash
docker restart <<container>>
```

### Remover um container
```bash
docker rm <<container>>
```

---

## 🔍 Inspeção e Logs

### Ver logs do container
Exibe logs de saída do container.
```bash
docker logs <<container>>
```

### Acompanhar logs em tempo real
```bash
docker logs -f <<container>>
```

### Inspecionar container ou imagem
Mostra detalhes em JSON.
```bash
docker inspect <<container_ou_imagem>>
```

---

## 🧠 Execução de Comandos Internos

### Executar comando dentro de um container em execução
```bash
docker exec -it <<container>> <<comando>>
```

### Acessar terminal do container
```bash
docker exec -it <<container>> /bin/bash
```

---

## 💾 Volumes

### Criar volume
```bash
docker volume create <<nome_volume>>
```

### Listar volumes
```bash
docker volume ls
```

### Remover volume
```bash
docker volume rm <<volume>>
```

### Usar volume em container
```bash
docker run -v <<volume>>:<<path_container>> <<imagem>>
```

---

## 🌐 Redes

### Listar redes
```bash
docker network ls
```

### Criar rede
```bash
docker network create <<nome_rede>>
```

### Conectar container à rede
```bash
docker network connect <<rede>> <<container>>
```

---

## 🧹 Limpeza

### Remover containers parados
```bash
docker container prune
```

### Remover imagens não utilizadas
```bash
docker image prune
```

### Limpeza geral
Remove containers, imagens, volumes e redes não utilizados.
```bash
docker system prune -a
```

---

# 🐙 Docker Compose

## 📄 Comandos Básicos

### Subir serviços definidos no docker-compose.yml
Cria e inicia todos os serviços.
```bash
docker-compose up
```

### Subir serviços em segundo plano
```bash
docker-compose up -d
```

### Parar serviços
```bash
docker-compose stop
```

### Parar e remover containers, redes e volumes
```bash
docker-compose down
```

### Remover tudo incluindo volumes
```bash
docker-compose down -v
```

---

## 🔍 Gerenciamento

### Listar serviços
```bash
docker-compose ps
```

### Ver logs de todos os serviços
```bash
docker-compose logs
```

### Logs de um serviço específico
```bash
docker-compose logs <<servico>>
```

### Acompanhar logs em tempo real
```bash
docker-compose logs -f
```

---

## 🧠 Execução de Comandos

### Executar comando em um serviço
```bash
docker-compose exec <<servico>> <<comando>>
```

### Acessar shell do serviço
```bash
docker-compose exec <<servico>> sh
```

---

## 🔄 Build e Atualização

### Construir imagens dos serviços
```bash
docker-compose build
```

### Recriar containers
```bash
docker-compose up --build
```

---

## 🧹 Limpeza no Compose

### Remover containers órfãos
```bash
docker-compose up --remove-orphans
```

---

## ✅ Boas Práticas

- Use `.env` para variáveis de ambiente
- Versione apenas arquivos essenciais
- Utilize tags fixas de imagem
- Prefira volumes nomeados

---

📌 **Sugestão:** Salve este arquivo como `docker-comandos.md` no seu repositório GitHub para fácil consulta.

