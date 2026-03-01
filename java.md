# 📌 Guia Completo de Comandos Java via Linha de Comando (CLI)

Este arquivo reúne **os principais comandos da CLI do Java (JDK)**, com exemplos práticos e parâmetros genéricos descritos como `<<param>>`. O objetivo é servir como **material de referência rápida** para uso em projetos, estudos e automações.

---

## ☕ java – Executar aplicações Java
Executa uma aplicação Java ou um arquivo `.jar`.

```bash
java <<opcoes>> <<ClassePrincipal>> <<args>>
```

```bash
java -Xmx512m Main arg1 arg2
```

```bash
java -jar <<arquivo.jar>>
```

---

## ☕ javac – Compilar código Java
Compila arquivos `.java` em bytecode `.class`.

```bash
javac <<opcoes>> <<arquivo.java>>
```

```bash
javac Main.java
```

```bash
javac -d <<diretorio>> *.java
```

---

## ☕ jar – Criar, listar e extrair arquivos JAR
Manipula arquivos `.jar` (empacotamento de aplicações).

```bash
jar <<opcoes>> <<arquivo.jar>> <<arquivos>>
```

```bash
jar cf app.jar *.class
```

```bash
jar tf app.jar
```

```bash
jar xf app.jar
```

---

## ☕ javadoc – Gerar documentação
Gera documentação HTML a partir dos comentários do código.

```bash
javadoc <<opcoes>> <<pacotes|arquivos>>
```

```bash
javadoc -d docs *.java
```

---

## ☕ jshell – REPL do Java
Ambiente interativo para testar código Java.

```bash
jshell <<opcoes>>
```

```bash
jshell
```

```bash
jshell script.jsh
```

---

## ☕ jdeps – Análise de dependências
Analisa dependências entre classes e módulos.

```bash
jdeps <<opcoes>> <<arquivo.jar|classe>>
```

```bash
jdeps app.jar
```

---

## ☕ jlink – Criar runtime Java customizado
Gera uma distribuição Java mínima contendo apenas os módulos necessários.

```bash
jlink <<opcoes>>
```

```bash
jlink --module-path <<path>> --add-modules <<modulo>> --output runtime
```

---

## ☕ jmod – Gerenciar módulos
Cria e inspeciona arquivos `.jmod`.

```bash
jmod <<acao>> <<opcoes>>
```

```bash
jmod describe java.base.jmod
```

---

## ☕ jcmd – Enviar comandos a JVM
Interage com processos Java em execução.

⚠️ **Cuidado:** afeta aplicações em runtime.

```bash
jcmd <<pid>> <<comando>>
```

```bash
jcmd 1234 GC.run
```

---

## ☕ jps – Listar processos Java
Lista processos Java ativos na máquina.

```bash
jps <<opcoes>>
```

```bash
jps -l
```

---

## ☕ jstack – Dump de threads
Exibe o estado das threads de uma JVM.

⚠️ **Uso diagnóstico**.

```bash
jstack <<pid>>
```

---

## ☕ jmap – Mapa de memória
Analisa uso de memória e heap da JVM.

⚠️ **Pode impactar performance**.

```bash
jmap <<opcoes>> <<pid>>
```

```bash
jmap -heap <<pid>>
```

---

## ☕ jstat – Estatísticas da JVM
Monitora garbage collection e memória.

```bash
jstat <<opcoes>> <<pid>> <<intervalo>>
```

```bash
jstat -gc <<pid>> 1000
```

---

## ☕ keytool – Gerenciamento de certificados
Gerencia certificados e keystores.

```bash
keytool <<acao>> <<opcoes>>
```

```bash
keytool -list -keystore <<arquivo.jks>>
```

---

## ☕ javap – Desmontador de bytecode
Inspeciona bytecode `.class`.

```bash
javap <<opcoes>> <<classe>>
```

```bash
javap -c Main
```

---

## ☕ jfr – Java Flight Recorder
Grava e analisa eventos da JVM.

```bash
jfr <<acao>>
```

```bash
jfr start
jfr stop
```

---

## ☕ jpackage – Empacotar aplicações
Cria instaladores nativos (exe, deb, dmg).

```bash
jpackage <<opcoes>>
```

```bash
jpackage --input <<dir>> --main-jar <<app.jar>> --name App
```

---

## ☕ javac + classpath
Compilação com dependências externas.

```bash
javac -cp <<classpath>> Main.java
```

---

## ☕ java + classpath
Execução com dependências externas.

```bash
java -cp <<classpath>> Main
```

---

## 📌 Observações finais
- Este guia cobre **os comandos oficiais do JDK**
- Compatível com Java 8+ (alguns comandos exigem Java 9+)
- Ideal para estudos, automações e pipelines CI/CD

---

📁 **Sugestão de uso:**
Salve este arquivo como `java-cli-cheatsheet.md` no seu repositório GitHub.

