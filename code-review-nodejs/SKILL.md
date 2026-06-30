---
name: code-review-nodejs
description: Revisar diffs e branches de projetos backend Node.js, especialmente APIs NestJS + TypeORM + Oracle do padrao Coamo. Use quando a usuaria pedir code review de alteracoes locais, staged, branch atual ou MR em projetos TypeScript/NestJS/Express/Fastify, com foco em arquitetura, regras de danger, testes, seguranca, regressao e consistencia de contrato.
---

# Node Code Review

Revisar apenas o diff solicitado e priorizar bugs, regressoes, riscos e gaps de teste.

## Definir Escopo

1. Identificar o escopo da revisao.
   - Para review de branch, comparar a branch atual com a branch-base do repositorio.
   - Preferir `git diff origin/develop...HEAD` quando o repositorio usa `develop`.
   - Caso contrario, usar a base apropriada, como `origin/main...HEAD` ou `origin/master...HEAD`.
   - Para staged-only review, usar `git diff --cached`.
   - Para worktree review com alteracoes unstaged, usar `git diff HEAD`.
2. Ler os arquivos afetados e o contexto suficiente para entender comportamento e impacto.
3. Revisar corretude, regressao, riscos e cobertura de testes.
4. Responder em Portugues do Brasil, salvo pedido explicito em outro idioma.

## Aplicar Regras da API Coamo

Ao revisar um projeto backend NestJS do padrao Coamo, duplicar manualmente no diff as validacoes que costumam existir em `danger.js` e em `rules/`, mesmo que o pipeline possa ja faze-las.

Comentar toda violacao encontrada nas linhas alteradas.

### Validacoes automaticas de `rules/`

| Arquivo | Regra que deve ser validada no diff | Excecoes |
|---|---|---|
| `big-file.rule.ts` | Arquivo novo ou modificado com mais de 150 linhas deve ser comentado. Se o crescimento ocorreu por inflacao sem refatoracao, exigir split. | Permitido em `*.entity(.ies).ts`, `*.http.gateway.ts`, `*.documentation.ts`, `*.container.registry.ts`, `*.constraint.ts`, migrations, seeds, `main.ts`, `@worker/config.ts`, testes e mocks |
| `long-function.rule.ts` | Funcao ou arrow com mais de 40 linhas deve ser comentada e sugerir extracao. | Permitido em `*.container.registry.ts`, `main.ts`, `@worker/config.ts`, `common/infra/{mock,http,observability}.ts`, `documentation.decorator.ts`, scripts de migration |
| `any-param.rule.ts` | Qualquer `any` em parametro, retorno, generic, cast ou variavel deve ser comentado. | Permitido apenas em `main.ts`, `@worker/config.ts`, `common/infra/{mock,http,observability,findSimilarity}.ts`, `convertFileBase64.use.case.ts`, `database.service.ts`, `seeds/` e libs `@uniface/*` |
| `no-comment.rule.ts` | Qualquer comentario (`//` ou `/* */`) em `application/*.use.case.ts`, `domain/**/*.ts` e `infra/**/*.ts` deve ser comentado. | Permitido em `.container.registry.ts`, modulo `observability/` e comentario `/* eslint-disable */` justificado |
| `core-layer-spec.rule.ts` | Arquivo novo em `@core/<mod>/{application,domain,infra}/` sem spec em `__test__/` deve ser comentado. Spec vazia ou generica tambem deve ser comentada. | Nao exigir spec para mocks, `domain/gateway/*.gateway.ts`, `*.enum.ts`, `key.ts` e modulo `common/` |

Nao tratar `Dangerfile.ts` e `types.ts` como regras proprias.

## Validar Arquitetura e Camadas

Aplicar a regra de ouro: zero logica de negocio em `@server`. Controller deve ser uma fachada HTTP fina.

### Camadas

| Camada | Path | Responsabilidade |
|---|---|---|
| `@server` | `src/@server/modules/<dom>/` | HTTP apenas: controller, Swagger e validacao de DTO |
| `@core` | `src/@core/modules/<dom>/` | Logica de negocio: entities, use cases e gateways |
| `@worker` | `src/@worker/modules/<dom>/` | Bull MQ: producers e consumers assincronos |
| `@orchestrator` | `src/@orchestrator/` | Agendamento e cron |

### Estrutura esperada de `@core/modules/<dom>/`

```text
application/<acao>.use.case.ts
domain/entity/<name>.entity.ts
domain/entity/<name>.entities.ts
domain/gateway/<name>.gateway.ts
infra/<name>.db.gateway.ts
infra/<name>.container.registry.ts
__test__/*.spec.ts
```

### Dependencias entre camadas

Comentar as seguintes violacoes:

- `@server/**` instanciando use case com `new` em vez de importar do `container.registry`.
- `@core/**` importando de `@server`, `@worker` ou `@nestjs/*`, salvo necessidade estrita em `infra/`.
- `application/<x>.use.case.ts` fazendo IO direto de HTTP, banco, Redis ou Bull em vez de delegar para gateway via DI.
- `domain/**` importando de `application/` ou `infra/`.
- `infra/<x>.db.gateway.ts` sem implementar a interface `I<Name>Gateway` de `domain/`.
- Imports profundos com `../../../` quando path aliases deveriam ser usados.

## Validar Container Registry

Confirmar que cada modulo `@core/<dom>` exporta use cases pre-instanciados em `<dom>.container.registry.ts`.

Comentar quando houver:

- Novo use case sem atualizacao do registry.
- Controller instanciando use case manualmente com `new`.
- Chamada fora do padrao `registry.acao.execute(...)`.

## Validar Naming e Contratos

- Tipos com prefixo `T`.
- Interfaces com prefixo `I`.
- Enums com prefixo `E`.
- Arquivos de use case em kebab-case e classe em PascalCase.
- Tabelas Oracle com prefixo `EGRU_`.
- Colunas Oracle em UPPERCASE com underscore.

## Validar Entities

- Exigir extensao de `BaseEntity` do projeto.
- Tratar soft delete por `deletedAt`; comentar hard delete sem justificativa.
- Nunca aceitar geracao manual de UUID v7 em use case.

### Nao comentar como bug

Nao apontar como erro os seguintes padroes idiomaticos de TypeORM usados no mapeamento Oracle:

- FK como `@Column` e relacao `@ManyToOne` ou `@OneToOne` para a mesma coluna.
- Mesma coluna fisica em `@JoinColumn({ name })` e outro atributo de FK.
- `@JoinColumn` com `referencedColumnName`.
- Self-reference via `@ManyToOne` ou `@OneToMany`.

### Comentar como bug em entidade

- `@Column` sem `name` quando a coluna Oracle nao bate com camelCase.
- Tipo divergente do mapeamento Oracle, como `varchar` em vez de `varchar2`.
- Falta de `nullable: true` quando o DDL real aceita `NULL`.
- Entidade sem `BaseEntity`.
- Duplicacao literal da mesma coluna em dois atributos conflitantes.

## Validar Excecoes, Auth e Observabilidade

- Vetar `throw new Error('...')` em producao quando houver excecoes de dominio apropriadas.
- Exigir `@User()` em controller em vez de `req.user`.
- Exigir `@RequirePermission(...)` em rotas protegidas.
- Vetar parametro `executionId`; o contexto deve vir de `AsyncLocalStorage`.
- Vetar `console.log` em producao.
- Preferir `observability.event(...)` a `TelemetryClient` direto.
- Aceitar logger do NestJS em middlewares e guards, nao em use cases.

## Validar Paginacao, Banco e Workers

- DTOs de paginacao devem estender `TPagination`.
- Use cases de listagem devem estender ou usar `PaginationGenericUseCase`.
- Gateways devem usar `andWhere`, nunca `where`, ao compor query incremental.
- Considerar o limite Oracle de 999 itens em clausula `IN`.
- Vetar `synchronize: true` em DataSource.
- Exigir migration para mudanca de schema.
- Confirmar nome de migration no padrao do projeto.
- Exigir producers derivados de `BaseProducer` e consumers de `BaseConsumer`.
- Exigir payload no envelope pattern do projeto.
- Exigir `obs.ts` para context propagation.
- Exigir registro de workers apenas em `background.module.ts`.

## Validar Anti-Patterns

Comentar quando encontrar:

- Use case com mais de uma responsabilidade clara.
- Use case lendo `process.env` direto.
- Use case com `try/catch` que engole erro sem rethrow ou log estruturado.
- Controller com logica de orquestracao fazendo tres ou mais chamadas a use cases.
- Domain entity com metodo de negocio fazendo IO.
- Imports circulares entre modulos.
- Endpoint sem decorator de documentacao Swagger do projeto.

## Validar Boas Praticas Gerais

Aplicar estas regras ao codigo novo presente no diff:

| # | Regra | Como aplicar |
|---|---|---|
| 1 | Sem recursao; sem `break` ou `continue` aninhados; maximo de 3 niveis de aninhamento; preferir early return | Apontar blocos novos com nesting excessivo |
| 2 | Loops com limite verificavel; preferir `for...of`; `while` exige contador-guarda; nunca `while(true)` sem saida documentada | Apontar `while` sem limite claro |
| 3 | Nao criar arrays, objetos ou Maps dentro de loop para acumulacao externa | Apontar inicializacao indevida dentro do loop |
| 4 | Funcao com responsabilidade unica; nome nao deve sugerir duas acoes | Apontar nomes como `validateAndSave` |
| 5 | Minimo de duas guardas por funcao publica: pre-condicao e pos-condicao quando aplicavel | Apontar funcao publica nova sem validacao de input |
| 6 | Variavel no menor escopo possivel; preferir `const`; nunca `var`; nao reutilizar variavel para significados diferentes | Apontar `let` desnecessario e reuso semantico |
| 7 | Validar parametros na primeira linha de funcoes exportadas; nao ignorar retorno de Promise ou funcao que pode falhar | Apontar chamada sem checagem de falha quando relevante |
| 8 | Sem `any`; sem `import * as` salvo exigencia da lib; usar `import type` para tipos | Apontar `as any`, `: any` e imports amplos injustificados |
| 9 | `async` com tratamento explicito ou propagacao intencional; nunca `catch` vazio ou so com `console.log`; usar erros de dominio com `status` ou `code` | Apontar swallow de erro e `throw new Error` |
| 10 | Respeitar Sonar: complexidade cognitiva <= 15, maximo de 5 parametros, evitar string literal repetida e remover variaveis mortas | Apontar funcoes novas com 6 ou mais parametros e repeticoes obvias |
| 11 | Nao expor stack trace ao cliente; sanitizar input; secret/token via env; rota protegida valida auth/autz; sem `debug=true` ou logs verbosos em producao | Apontar credenciais hardcoded e falta de protecao |

## Validar Testes

- Verificar cobertura adequada de unidade e integracao.
- Apontar asserts ausentes, edge cases nao cobertos e expectativas desatualizadas.
- Se teste falhar, distinguir regressao real de teste desatualizado.
- Comentar ausencia de spec quando a regra do projeto exigir.

## Formatar a Resposta

Responder em formato review-first:

1. Listar findings primeiro, em ordem de severidade, com referencias de arquivo quando possivel.
2. Listar perguntas em aberto ou premissas em seguida.
3. Encerrar com um resumo breve apenas se isso adicionar valor.

Se nenhum problema for encontrado, dizer isso explicitamente e registrar risco residual ou gap de teste.

## Comandos Uteis

- `git status --short`
- `git diff --cached`
- `git diff HEAD`
- `git diff origin/develop...HEAD`
- `git diff origin/main...HEAD`
- `git log --oneline --decorate -5`

## Foco Final

Revisar o diff, nao o repositorio inteiro.

- Comentar apenas sobre linhas que aparecem no diff.
- Se mencionar identificadores nao alterados, deixar claro que sao apenas contexto.
- Duplicar as validacoes das rules do projeto como defesa em profundidade.
- Adicionar violacoes semanticas que regex ou automacoes nao detectam.
