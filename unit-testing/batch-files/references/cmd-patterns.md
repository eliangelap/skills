# Referência de padrões do cmd.exe

## Expansão e blocos

- `%VAR%` expande quando o bloco entre parênteses é interpretado; dentro de loops, pode ficar com valor antigo.
- `!VAR!` expande na execução, mas perde/explora sinais `!` presentes nos dados quando delayed expansion está ativo.
- Para ler dados literais em um `FOR /F`, desative delayed expansion; ative-a somente para calcular e copiar o resultado para uma variável segura. Não use `!linha!` em dados que podem conter exclamações.
- Escape metacaracteres em comandos compostos: `^&`, `^|`, `^<`, `^>`, `^^`. Prefira argumentos entre aspas, mas lembre que aspas não neutralizam todos os metacaracteres se o valor for reinjetado em `cmd /c` ou `call`.

## Modelo de erro

```bat
comando-que-pode-falhar
set "RC=%ERRORLEVEL%"
if not "%RC%"=="0" (
  >&2 echo Falha: comando-que-pode-falhar retornou %RC%.
  exit /b %RC%
)
```

`IF ERRORLEVEL 1` significa “maior ou igual a 1”; para vários códigos, testar do maior para o menor. `exit /b` retorna ao chamador, enquanto `exit` encerra o processo `cmd.exe`.

## Argumentos, diretórios e arquivos

```bat
@echo off
setlocal EnableExtensions DisableDelayedExpansion

if "%~1"=="" (
  >&2 echo Uso: %~nx0 "arquivo-ou-pasta"
  exit /b 2
)

set "TARGET=%~f1"
if not exist "%TARGET%" (
  >&2 echo Nao encontrado: "%TARGET%"
  exit /b 3
)

pushd "%~dp0" || exit /b 4
rem Trabalhar relativo ao diretorio do script.
popd
```

- `%~1` remove aspas externas; `%~f1` normaliza para caminho absoluto existente ou resolvível.
- Verificar explicitamente arquivo versus diretório quando a diferença importar: `if exist "X\NUL"` para diretório; usar `for %%I in ("X") do if exist "%%~fI\"` quando adequado.
- Nunca montar uma linha de comando executável a partir de argumento não confiável. Passar dados como argumentos entre aspas para programas conhecidos.

## Operações potencialmente destrutivas

- Exibir o alvo absoluto, exigir confirmação ou parâmetro explícito e oferecer `/dry-run` antes de `del`, `rmdir /s`, `move`, sobrescrita e limpeza em massa.
- Rejeitar alvos vazios, raiz de unidade e diretórios inesperados antes de remover conteúdo.
- Registrar arquivos afetados e o código de saída de cada etapa relevante.

## Limitações práticas

- Batch não trata Unicode, datas locais, JSON e texto complexo de modo confiável. Preferir PowerShell para essas partes.
- `FOR /F` ignora linhas vazias e trata `;` como comentário por padrão; ajustar `eol=` e `delims=` quando necessário.
- Não depender da codificação do console para nomes de arquivo ou conteúdo internacionalizado sem testar no ambiente-alvo.
