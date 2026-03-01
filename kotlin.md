# Kotlin CLI — Guia Completo de Comandos

Este documento reúne os principais comandos de **Kotlin via linha de comando (CLI)**, utilizando o compilador oficial mantido pela JetBrains.

Os exemplos utilizam parâmetros genéricos no formato `<<param>>` para facilitar o estudo.

---

## 1. Verificar versão do compilador Kotlin
Exibe a versão instalada do compilador Kotlin.

```bash
kotlinc -version
```

---

## 2. Compilar arquivo Kotlin para JVM (.class)
Compila um arquivo `.kt` gerando bytecode JVM.

```bash
kotlinc <<arquivo.kt>>
```

---

## 3. Compilar e gerar JAR executável
Gera um arquivo JAR executável.

```bash
kotlinc <<arquivo.kt>> -include-runtime -d <<arquivo.jar>>
```

---

## 4. Executar um arquivo Kotlin diretamente (script)
Executa um script Kotlin (`.kts`).

```bash
kotlinc -script <<script.kts>>
```

---

## 5. Executar JAR Kotlin
Executa uma aplicação Kotlin empacotada em JAR.

```bash
java -jar <<arquivo.jar>>
```

---

## 6. Compilar múltiplos arquivos Kotlin
Compila vários arquivos Kotlin ao mesmo tempo.

```bash
kotlinc <<arquivo1.kt>> <<arquivo2.kt>> -d <<saida>>
```

---

## 7. Definir classpath
Define dependências externas para compilação.

```bash
kotlinc <<arquivo.kt>> -cp <<classpath>>
```

---

## 8. Compilar para diretório específico
Define diretório de saída dos `.class`.

```bash
kotlinc <<arquivo.kt>> -d <<diretorio_saida>>
```

---

## 9. Compilar com avisos detalhados
Exibe avisos e mensagens mais detalhadas.

```bash
kotlinc <<arquivo.kt>> -verbose
```

---

## 10. Tratar avisos como erro
Força falha de compilação ao encontrar warnings.

```bash
kotlinc <<arquivo.kt>> -Werror
```

---

## 11. Desativar warnings
Desabilita a exibição de warnings.

```bash
kotlinc <<arquivo.kt>> -nowarn
```

---

## 12. Gerar código com debug
Inclui informações de depuração.

```bash
kotlinc <<arquivo.kt>> -g
```

---

## 13. Compilar código Kotlin para JavaScript
Gera saída JavaScript.

```bash
kotlinc-js <<arquivo.kt>> -output <<arquivo.js>>
```

---

## 14. Compilar múltiplos arquivos para JavaScript
Compila vários arquivos Kotlin para JS.

```bash
kotlinc-js <<arquivo1.kt>> <<arquivo2.kt>> -output <<saida.js>>
```

---

## 15. Definir módulo JS
Define nome do módulo JavaScript.

```bash
kotlinc-js <<arquivo.kt>> -module-name <<nome_modulo>>
```

---

## 16. Compilar para Kotlin/Native
Gera binário nativo.

```bash
kotlinc-native <<arquivo.kt>> -o <<saida>>
```

---

## 17. Definir alvo Kotlin/Native
Especifica o target da compilação nativa.

```bash
kotlinc-native <<arquivo.kt>> -target <<plataforma>>
```

---

## 18. Compilar com otimização (Native)
Habilita otimizações no binário nativo.

```bash
kotlinc-native <<arquivo.kt>> -opt
```

---

## 19. Executar REPL Kotlin
Abre o console interativo Kotlin.

```bash
kotlinc
```

---

## 20. Executar código no REPL
Executa comandos Kotlin interativamente.

```bash
>>> println("Olá, Kotlin CLI")
```

---

## 21. Compilar com API específica
Define versão mínima da API Kotlin.

```bash
kotlinc <<arquivo.kt>> -api-version <<versao>>
```

---

## 22. Definir versão da linguagem
Controla recursos da linguagem Kotlin.

```bash
kotlinc <<arquivo.kt>> -language-version <<versao>>
```

---

## 23. Gerar metadata
Gera apenas metadata Kotlin.

```bash
kotlinc <<arquivo.kt>> -Xmetadata
```

---

## 24. Exibir ajuda do compilador
Mostra todos os comandos disponíveis.

```bash
kotlinc -help
```

---

## 25. Exibir opções avançadas
Lista opções internas e avançadas.

```bash
kotlinc -X
```

---

## 26. Compilar ignorando dependências padrão
Desabilita inclusão automática da stdlib.

```bash
kotlinc <<arquivo.kt>> -no-stdlib
```

---

## 27. Compilar ignorando runtime
Não inclui runtime Kotlin.

```bash
kotlinc <<arquivo.kt>> -no-runtime
```

---

## 28. Compilar com JVM target específico
Define a versão da JVM.

```bash
kotlinc <<arquivo.kt>> -jvm-target <<versao>>
```

---

## 29. Compilar com argumentos livres
Passa argumentos diretamente para o compilador.

```bash
kotlinc <<arquivo.kt>> -P <<plugin:param=valor>>
```

---

## 30. Limpar artefatos (exemplo shell)
Remove arquivos gerados.

```bash
rm -rf <<diretorio_saida>> *.jar
```

---

## Observações Importantes
- A maioria dos comandos são **seguros** (somente leitura/compilação).
- ⚠️ Comandos de remoção (`rm`) ou sobrescrita devem ser usados com cautela.
- Recomenda-se uso integrado com Gradle para projetos maiores.

---

📌 Mantido para estudos e referência rápida de Kotlin CLI.
