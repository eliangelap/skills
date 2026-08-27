---
name: reactjs-development
description: Desenvolver, corrigir, refatorar e testar frontends React 19 com Vite e Ant Design no padrão Eliangela, especialmente módulos em `@core` e `@presentation`. Use para implementar telas, componentes, hooks, casos de uso, gateways, registries e testes; não use para apenas revisar diffs.
---

# Desenvolvimento ReactJS

Implemente a demanda aderindo à arquitetura e às convenções já presentes no repositório. Antes de editar, leia `package.json`, a configuração afetada e um módulo semelhante ao solicitado; esta skill é referência, não substitui o padrão concreto do projeto.

## Fluxo de trabalho

1. Delimite o impacto: domínio, aplicação, infraestrutura, apresentação, rotas, configuração ou integração.
2. Em código pré-existente, antes de alterar lógica já existente, pergunte à usuária se essa lógica pode ser melhorada. Se ela autorizar, elabore antes da implementação um plano de alteração com objetivo, comportamento atual e proposto, camadas, casos de uso, contratos e testes afetados. Sem essa autorização, limite-se à mudança necessária e preserve a lógica existente fora do escopo.
3. Identifique uma referência equivalente no projeto. Para um módulo novo, use a estrutura mais próxima em `src/@core/modules` e `src/@presentation/modules`.
4. Preserve o fluxo `rota/página ou hook → registry → caso de uso → contrato de gateway → adaptador HTTP`. Não instancie casos de uso em componentes e não faça IO diretamente em hooks ou componentes.
5. Trabalhe em TDD: escreva ou ajuste o spec, confirme a falha, implemente o mínimo necessário e valide em verde. Ao criar ou alterar artefatos executáveis de `@core`, mantenha specs relevantes para cada artefato alterado, incluindo domínio, aplicação, infraestrutura e registry; não crie specs para mocks que só forneçam dados aos testes.
6. Valide inicialmente no escopo alterado. Finalize com os comandos definidos pelo repositório — normalmente `yarn lint` e `yarn test` — e informe com clareza o que não pôde ser executado e por quê.

## Arquitetura e dependências

- Mantenha `@core` independente de React, React Router, Ant Design, `react-hook-form` e APIs do navegador. Ele contém regras de negócio, contratos, entidades e casos de uso.
- Em `@presentation`, concentre-se em UI, estado de interação, composição de rotas, contextos e hooks. Cálculos, parsing, normalização, validação de contrato e regras de negócio pertencem a `application`.
- Faça casos de uso dependerem de interfaces de gateway. `infra` apenas adapta HTTP ou outras integrações e implementa o contrato; regras de negócio nela são proibidas, inclusive decisões condicionais que definam resultado de negócio. Toda regra, parsing, validação ou normalização pertence a `application` e deve estar em um caso de uso, com contrato e testes próprios; quando for responsabilidade distinta, crie um caso de uso separado e componha-o explicitamente no fluxo principal.
- Exponha casos de uso por registries Inversify com símbolos e bindings consistentes com o módulo de referência. A apresentação consome o atalho do registry, nunca importa o arquivo `*.use.case.ts` diretamente.
- Siga as convenções vigentes para `T` em types, `I` em interfaces, `E` em enums, arquivos de caso de uso em kebab-case, componentes em PascalCase e hooks iniciados por `use`.
- Use aliases `@core` e `@presentation`, em vez de imports profundos. Agrupe símbolos do mesmo módulo em uma única declaração de import e use `import type` quando aplicável.

Leia [architecture.md](references/architecture.md) ao criar ou reorganizar módulos, hooks, gateways, registries, rotas ou configuração. Leia [testing.md](references/testing.md) ao escrever ou ampliar testes.

## React, Ant Design e estado

- Prefira componentes com uma responsabilidade clara; extraia componentes ou hooks quando a composição, a regra de interação ou o estado se tornarem independentes.
- Use fonte reativa para valores de formulário que alteram a renderização, a validação ou o payload. Com Ant Design, prefira `Form.useWatch` a leituras imperativas de `form.getFieldValue()` ou `getFieldsValue()` durante o render.
- Declare dependências granulares em `useMemo`, `useCallback` e `useEffect`; não dependa do objeto inteiro quando apenas campos específicos são usados.
- Em efeitos, faça uma única chamada para uma função nomeada que encapsule o fluxo. Trate carregamento, vazio, erro e sucesso quando forem estados possíveis da tela.
- Não inicie buscas dependentes de catálogos, permissões ou opções assíncronas antes que esses dados estejam prontos. Evite estados de tela temporariamente incorretos.
- Não deixe chamadas `Promise` sem `await`, `return`, `void` deliberado ou composição/tratamento equivalente. Nunca engula erros.
- Para retornos possivelmente nulos, avalie o contrato: use guarda explícita e estado/erro adequado quando a tela não puder prosseguir; use `?.` somente quando a ausência for realmente aceitável.

## Segurança e configuração

- Obtenha autenticação pelo contexto ou interceptor existente, nunca lendo token manualmente de `localStorage`.
- Proteja rotas conforme o mecanismo já adotado e não exponha PII, secrets ou stack traces em notificações e logs.
- Use apenas variáveis de runtime `import.meta.env.VITE_*`; não use `process.env` no código executado pelo navegador e não deixe URLs, chaves ou credenciais hardcoded.
- Mantenha modais, notificações e cliente HTTP centralizados, reutilizando as abstrações da aplicação.
- Ao registrar falhas na observabilidade, use mensagem ou evento específico da operação e atributos que permitam diagnóstico, como operação, identificador técnico não sensível, código/categoria do erro e causa. Não registre mensagens genéricas como `erro ao processar`; a observabilidade não substitui tratamento explícito: após registrar, propague ou converta o erro conforme o contrato do fluxo e apresente o estado de erro adequado. Nunca capture uma exceção apenas para registrá-la e continuar silenciosamente.

## Encerramento

Revise o diff para confirmar direção das dependências, ausência de React em `@core`, contratos entre camadas, estados transitórios e cobertura dos fluxos de sucesso e erro. Relate os comandos executados e quaisquer limitações do ambiente.
