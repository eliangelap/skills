---
name: batch-files
description: "Criar, editar, revisar e depurar scripts Windows Batch (.bat e .cmd) para automação avançada via cmd.exe. Usar para tarefas administrativas, inicialização, cópia e limpeza de arquivos, processamento de texto, agendamento, integração com programas Windows e tratamento robusto de erros em cmd.exe."
---

# Windows Batch Specialist

## Desenvolver o script

- Começar com `@echo off` e usar blocos e rótulos legíveis.
- Delimitar atribuições com `set "NOME=valor"` e caminhos com aspas duplas.
- Nomear todas as variáveis com termos descritivos em inglês, como `SOURCE_DIRECTORY`, `BACKUP_FILE` e `EXIT_CODE`; evitar nomes genéricos ou de uma letra, exceto contadores locais inevitáveis.
- Aplicar `setlocal EnableExtensions DisableDelayedExpansion` no início. Ativar `EnableDelayedExpansion` apenas nos blocos que alteram e leem variáveis dentro de `FOR` ou `IF`.
- Preservar texto de entrada que possa conter `!`: manter delayed expansion desligada ao capturá-lo e usar a técnica de alternância descrita em [referências de cmd.exe](references/cmd-patterns.md).
- Capturar o resultado imediatamente após cada comando relevante: `comando` seguido de `set "EXIT_CODE=%ERRORLEVEL%"`. Testar `EXIT_CODE` antes de executar outro comando.
- Usar `IF ERRORLEVEL n` somente em ordem decrescente. Preferir `if not "%EXIT_CODE%"=="0"` quando a intenção for testar falha genérica.
- Validar argumentos, pré-condições, privilégios e caminhos antes de ações que alterem ou removam dados. Oferecer modo de simulação quando a operação for destrutiva ou em lote.
- Redirecionar saída apenas quando ela não for necessária ao diagnóstico. Não ocultar mensagens de erro sem registrar uma alternativa útil.

## Escolher padrões corretos

- Usar `%~dp0` para recursos relativos ao próprio script; não presumir o diretório atual.
- Usar `pushd` e `popd` para trocar de diretório temporariamente; `pushd` também resolve caminhos UNC.
- Usar `for /f "usebackq delims="` para linhas inteiras de arquivo e `findstr` somente quando seu comportamento de expressões regulares e codificação for apropriado.
- Usar `call` com cautela: ele provoca uma segunda expansão e pode executar conteúdo inesperado. Evitar para dados não confiáveis.
- Delegar tarefas cuja confiabilidade dependa de Unicode, JSON, datas, rede, registro ou APIs do Windows ao PowerShell chamado explicitamente, mantendo o Batch como orquestrador quando fizer sentido.

## Entregar a resposta

1. Explicar em poucas frases o objetivo e os efeitos do script.
2. Fornecer um arquivo completo em bloco `bat`, incluindo validação e caminho de erro quando aplicável.
3. Informar como salvar e executar; recomendar ANSI/OEM apenas se necessário ao ambiente e preferir UTF-8 sem BOM quando compatível com os programas chamados.
4. Indicar se exige elevação e listar efeitos destrutivos antes da execução.
5. Sugerir melhorias práticas, como log, modo simulação, parametrização ou agendamento.

## Consultar a referência

Ler [referências de cmd.exe](references/cmd-patterns.md) antes de criar lógica com blocos, `FOR /F`, expansão de variáveis, código de saída, argumentos ou remoção em lote.
