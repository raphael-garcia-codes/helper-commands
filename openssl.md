# OpenSSL – Catálogo Completo de Comandos (Cheat Sheet)

Este documento reúne os principais comandos do **OpenSSL**, organizados por categoria, com explicações em português e exemplos usando parâmetros genéricos no formato `<<param>>`.

---

## 1. Geração e Manipulação de Chaves Privadas

### Gerar chave privada RSA
Gera uma chave privada RSA com tamanho definido.
```bash
openssl genrsa -out <<arquivo_chave_privada>> <<tamanho_bits>>
```

### Gerar chave privada RSA protegida por senha
Gera uma chave privada RSA criptografada com AES.
```bash
openssl genrsa -aes256 -out <<arquivo_chave_privada>> <<tamanho_bits>>
```

### Gerar chave privada ECC
Cria uma chave privada usando criptografia de curva elíptica.
```bash
openssl ecparam -name <<nome_curva>> -genkey -noout -out <<arquivo_chave_privada>>
```

### Remover senha de chave privada
Remove a proteção por senha de uma chave privada.
```bash
openssl rsa -in <<chave_com_senha>> -out <<chave_sem_senha>>
```

---

## 2. Extração de Chave Pública

### Extrair chave pública de uma chave privada
```bash
openssl rsa -in <<chave_privada>> -pubout -out <<chave_publica>>
```

### Extrair chave pública de certificado
```bash
openssl x509 -in <<certificado>> -pubkey -noout > <<chave_publica>>
```

---

## 3. CSR – Certificate Signing Request

### Criar CSR
```bash
openssl req -new -key <<chave_privada>> -out <<arquivo_csr>>
```

### Criar CSR sem interação
```bash
openssl req -new -key <<chave_privada>> -out <<arquivo_csr>> -subj "<<subject_dn>>"
```

### Visualizar CSR
```bash
openssl req -in <<arquivo_csr>> -text -noout
```

---

## 4. Certificados X.509

### Criar certificado autoassinado
```bash
openssl req -x509 -new -nodes -key <<chave_privada>> -sha256 -days <<dias_validade>> -out <<certificado>>
```

### Visualizar certificado
```bash
openssl x509 -in <<certificado>> -text -noout
```

### Ver data de expiração
```bash
openssl x509 -in <<certificado>> -noout -enddate
```

### Converter DER para PEM
```bash
openssl x509 -inform DER -in <<certificado_der>> -out <<certificado_pem>>
```

---

## 5. PKCS#12 (PFX)

### Criar arquivo PFX
```bash
openssl pkcs12 -export -out <<arquivo_pfx>> -inkey <<chave_privada>> -in <<certificado>>
```

### Extrair chave privada do PFX
```bash
openssl pkcs12 -in <<arquivo_pfx>> -nocerts -out <<chave_privada>>
```

---

## 6. Criptografia Simétrica

### Criptografar arquivo com AES
```bash
openssl enc -aes-256-cbc -salt -in <<arquivo_entrada>> -out <<arquivo_saida>>
```

### Descriptografar arquivo AES
```bash
openssl enc -aes-256-cbc -d -in <<arquivo_criptografado>> -out <<arquivo_original>>
```

---

## 7. Hashes e Assinaturas

### Gerar hash SHA-256
```bash
openssl dgst -sha256 <<arquivo>>
```

### Assinar arquivo
```bash
openssl dgst -sha256 -sign <<chave_privada>> -out <<assinatura>> <<arquivo>>
```

### Verificar assinatura
```bash
openssl dgst -sha256 -verify <<chave_publica>> -signature <<assinatura>> <<arquivo>>
```

---

## 8. TLS / SSL

### Testar conexão SSL/TLS
```bash
openssl s_client -connect <<host>>:<<porta>>
```

### Mostrar cadeia de certificados
```bash
openssl s_client -connect <<host>>:<<porta>> -showcerts
```

---

## 9. Utilidades

### Gerar número aleatório
```bash
openssl rand <<quantidade_bytes>>
```

### Gerar Base64
```bash
openssl rand -base64 <<quantidade_bytes>>
```

### Ver versão do OpenSSL
```bash
openssl version
```

---

📌 Documento ideal para uso como **README.md** ou **cheat sheet técnico**.
