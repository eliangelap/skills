---
name: code-review-reactjs
description: Revisar diffs e branches de projetos frontend web do padrão Coamo em React 19 + Vite + Ant Design, comparando com a branch-base adequada e aplicando em profundidade as regras de arquitetura, danger rules, padrões de camadas e boas práticas de React/TypeScript. Usar quando a usuária pedir code review de MRs, branches, staged changes ou worktree em projetos como web-gestor-rural-v2.
---

# Regras de code review — WEB (React 19 + Vite + Ant Design)

Aplicar quando o MR for de um projeto **frontend web** do padrão Coamo
(ex.: `web-gestor-rural-v2`).

Fonte: `worktrees/web/.claude/rules/architecture.md`, README do projeto e
`rules/*.rule.ts` do próprio projeto.

## Fluxo

1. Identificar o escopo do review.
   - Preferir `git diff origin/develop...HEAD` quando o repositório usar `develop`.
   - Caso contrário, usar `origin/main...HEAD` ou a base correta do projeto.
   - Para staged only, usar `git diff --cached`.
   - Para worktree, usar `git diff HEAD`.
2. Ler os arquivos alterados e o contexto suficiente para entender impacto e dependências.
3. Revisar primeiro por bugs, regressões, riscos e ausência de testes.
4. Responder em **Português do Brasil**.
5. Comentar **apenas o que está no diff**. Se citar contexto não alterado, deixar isso explícito.

## Validações automáticas (`rules/`)

Aplicar no diff todas as rules do projeto, mesmo que o pipeline esteja desligado, a lista de exceções esteja desatualizada ou o `Dangerfile` não esteja rodando.

### Rules invocadas pelo `Dangerfile.ts`

| Arquivo | Regra que deve aplicar | Exceções |
|---|---|---|
| `big-file.rule.ts` | Arquivo novo ou modificado **> 200 linhas**: comentar. Se cresceu por inflação sem refator, exigir split. | Permitido em `*.entity(.ies).ts`, `*.http.gateway.ts`, `*.documentation.ts`, `*.container.registry.ts`, `*.constraint.ts`, `*.styles.ts`, `main.ts`, `libs/uniface-orm/`, testes, mocks e lista nominal em `ignoredBigFileFiles` |
| `long-function.rule.ts` | Função > **60 linhas** em `.ts/.js/.jsx`; **> 200 linhas** em `.tsx`: comentar e sugerir extração. | Permitido em `Dangerfile.ts`, `common/infra/{mock,http}.ts`, páginas nominais de auth/example/form em `@presentation` e lista nominal |
| `any-param.rule.ts` | Parâmetro tipado `any` (`any[]`, `Promise<any>`, etc.): comentar. Estender também para `any` em retorno, generic, cast e variável. | Permitido apenas em `@uniface/*`, `libs/uniface-orm/`, `@core/.../common/infra/*`, `@presentation/.../route/*`, `@presentation/components/common/*`, páginas nominais de form, `*.styles.ts`, testes |
| `no-comment.rule.ts` | Qualquer comentário em `application/*.use.case.ts`, `domain/**/*.ts`, `infra/**/*.ts` (exceto `.container.ts`) e em qualquer `.ts/.tsx` de `@presentation/`: comentar. | Apenas `/* eslint-disable */` justificado |
| `inline-style.rule.ts` | `<elem ... style={{` em `.tsx`: comentar e exigir mover para `styles.ts`. | Permitido em `Dangerfile.ts`, `@presentation/components/layout/index.tsx`, `@presentation/components/common/icons/**`, `*.styles.ts` |
| `core-layer-spec.rule.ts` | Arquivo novo em `@core/<mod>/{application,domain,infra}/` sem spec em `__test__/`: comentar. Spec vazia ou genérica: comentar. | Não exigir spec para mocks, `domain/gateway/*.gateway.ts`, `*.enum.ts`, `key.ts`, módulo `common/` |

### Rules standalone

| Arquivo | Regra que deve aplicar | Notas |
|---|---|---|
| `core-architecture.rule.ts` | Módulo novo em `@core/modules/<mod>/` fora do padrão: comentar. | Pastas permitidas: `application`, `domain`, `infra`, `__mock__`, `__mocks__`; subpastas `__test__`; gateway só em `domain/` ou `infra/` fora de `__test__/` |
| `use-case-architecture.rule.ts` | Arquivo `<acao>.use.case.ts` em kebab-case, classe exportada `<Acao>UseCase` em PascalCase, dentro de `application/`, sem `copy` no nome. | Qualquer desvio: comentar |
| `use-case-import.rule.ts` | `import ... from '*.use.case'` fora de `src/@core/modules/<mod>/infra/*.registry.(ts|js)`: comentar. | Hook/componente deve consumir via registry |
| `domain-files.rule.ts` | `domain-entities.ts`: só `type/interface/enum`. `domain-entity.ts`: só `class/type/interface`. `domain-gateway.ts`: exatamente uma `interface I*Gateway`. | Qualquer const/função: comentar |
| `react-usage.rule.ts` | Em `.tsx` de `src/`: lógica aritmética em variável de corpo de componente ou `useEffect` com corpo que não seja uma única chamada de função. | Exigir mover para use case/helper |
| `no-inline-function-in-jsx.rule.ts` | Função inline em prop JSX com **> 3 linhas**: comentar. | Sugerir `useCallback` ou helper |
| `run-react-usage.js` | Runner standalone para `react-usage.rule.ts`. | Aplicar no diff também |

## Camadas e responsabilidades

| Camada | Path | Responsabilidade |
|---|---|---|
| `@core` | `src/@core/modules/<dom>/` | Lógica de negócio: entities, use cases, gateways. Sem React. |
| `@presentation` | `src/@presentation/modules/<dom>/` | UI: pages, components, hooks, contexts, rotas |
| `@presentation/components` | `src/@presentation/components/` | Componentes reutilizáveis |
| `@presentation/config` | `src/@presentation/config/` | Configuração de UI |

**Regra de ouro:** zero React em `@core` e zero lógica de cálculo/negócio em `.tsx`.

## Estrutura esperada de `@core/modules/<dom>/`

```text
application/<acao>.use.case.ts
domain/entity/<name>.entity.ts
domain/entity/<name>.entities.ts
domain/gateway/<name>.gateway.ts
infra/<name>.http.gateway.ts
infra/<name>.container.registry.ts
__test__/*.spec.ts
__mock__/
```

## Violações arquiteturais que deve apontar

- `@presentation/**` importando use case diretamente em vez de registry.
- `@core/**` importando `react`, `react-router`, `antd` ou `react-hook-form`.
- `application/<x>.use.case.ts` fazendo `axios` direto em vez de gateway.
- `domain/**` importando de `application/` ou `infra/`.
- `infra/<x>.http.gateway.ts` sem implementar `I<Name>Gateway`.
- Imports profundos `../../../` em vez de `@core` ou `@presentation`.

## Container Registry (Inversify)

```ts
// correto
import { crop } from '@core/modules/crop/infra/crop.container.registry';
const result = await crop.create.execute({ ...params });

// errado
new CreateCropUseCase(...)
import { CreateCropUseCase } from '@core/modules/crop/application/create.use.case';
```

## Naming

- Types com prefixo `T`.
- Interfaces com prefixo `I`.
- Enums com prefixo `E`.
- Use cases em arquivo kebab-case e classe PascalCase.
- Componentes em `PascalCase.tsx`.
- Hooks em `useNome.tsx`.

## Auth, observabilidade, HTTP, env e rotas

- Token de auth deve vir do contexto/interceptor, não de `localStorage` manual.
- Rotas protegidas devem estar corretamente guardadas em `routes.tsx`.
- `console.log` em produção deve ser apontado.
- Nunca logar PII como CPF ou e-mail completo.
- `*.http.gateway.ts` deve usar o client centralizado via DI.
- Erros HTTP devem ser convertidos em exceptions de domínio.
- Toda env de runtime deve usar `VITE_`.
- `process.env.X` em runtime deve ser apontado; usar `import.meta.env.VITE_X`.
- URL ou credencial hardcoded deve ser apontada.

## Anti-patterns que deve vetar

- Hook customizado fazendo IO direto com `fetch` ou `axios`.
- Componente com mais de uma responsabilidade.
- Use case lendo `import.meta.env` direto.
- Use case com `try/catch` engolindo erro.
- Modal ou notification global instanciado em vários lugares.
- Imports circulares.

## Boas práticas gerais para código novo do diff

Apontar toda violação encontrada em linhas novas ou alteradas.

1. Sem recursão; sem `break`/`continue` aninhados; máximo **3 níveis** de `if/for/while`; preferir early return.
2. Loops com limite verificável; preferir `for...of`; `while` exige contador-guarda; nunca `while(true)` sem justificativa.
3. Não criar arrays, objetos ou `Map` dentro de loop quando o objetivo é acumular fora dele.
4. Função com responsabilidade única; nome não deve usar `e` ou `ou` para juntar ações distintas.
5. Função pública nova deve ter validação de pré-condição e checagem de estado/resultados quando fizer sentido.
6. Preferir `const` a `let`; nunca `var`; não reutilizar variável para papéis diferentes.
7. Validar params no começo de funções exportadas; nunca ignorar retorno relevante de Promise.
8. Sem `any`; sem `import * as` sem motivo; usar `import type` para tipos puros.
9. `async` com tratamento explícito; nunca `catch` vazio ou só com `console.log`; preferir erro custom com `status` ou `code` quando houver padrão do projeto.
10. Vigiar complexidade cognitiva, número excessivo de parâmetros, string literal repetida, código morto e não usado.
11. Não expor stack ao cliente; sanitizar input; secret via env; rota protegida deve validar auth/autz; sem `debug=true` ou logs verbosos em produção.

## Formato da resposta

1. Listar findings primeiro, do mais grave para o menos grave, com referência de arquivo e linha quando possível.
2. Depois listar perguntas abertas ou assumptions.
3. Encerrar com um resumo breve apenas se agregar valor.
4. Se não houver findings, dizer isso explicitamente e citar riscos residuais ou lacunas de teste.
