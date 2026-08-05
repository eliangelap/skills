---
name: nodejs-development-coamo
description: Desenvolver, corrigir, refatorar e testar APIs Node.js/NestJS no padrão Coamo, especialmente projetos com TypeORM, Oracle, Inversify, Redis e BullMQ. Use ao implementar módulos ou endpoints, casos de uso, gateways, registries, workers, integrações e testes em APIs Coamo estruturadas em `@core`, `@server` e `@worker`.
---

# Desenvolvimento Node.js Coamo

Desenvolva mudanças aderentes à arquitetura existente. Antes de editar, inspecione `package.json`, o módulo mais semelhante e os arquivos de configuração afetados; não aplique exemplos desta skill literalmente quando divergirem do código atual.

## Fluxo

1. Delimite a camada e os efeitos da demanda: domínio, aplicação, infraestrutura, HTTP, worker, orquestração, dados ou configuração.
2. Use `src/@core/modules/modality` como primeira referência de convenções, substituindo-a por um módulo mais próximo quando houver.
3. Preserve a direção das dependências: controller/worker → caso de uso → gateway/contrato → adaptador. Não coloque regras de negócio em controller, worker ou gateway.
4. Trabalhe em TDD: escreva o spec, execute-o para confirmar a falha, implemente o mínimo necessário e execute-o novamente. Mantenha `describe` e `it` em inglês; mantenha mensagens de negócio em português.
5. Valide apenas no escopo necessário durante a implementação e finalize com `yarn lint`, `yarn test` e, para mudanças HTTP, dados ou integração, `yarn test:e2e`. Informe limitações de ambiente (Oracle, Redis, credenciais ou serviços externos) sem ocultá-las.

## Seleção de referência

- Para estruturar ou expandir módulo em `@core`, leia [architecture.md](references/architecture.md).
- Para criar ou revisar testes, leia [testing.md](references/testing.md).
- Para jobs, filas ou fluxos agendados, leia a seção correspondente de [architecture.md](references/architecture.md) e compare com as bases comuns já existentes.
- Para E2E com dependências de dados, inspecione `architecture/e2e-test-plan.md` no repositório-alvo antes de alterar a ordem, os seeds ou as fixtures.

## Regras de implementação

- Modele entidades, value objects, DTOs e contratos no domínio; use `class-validator` e Swagger conforme os pares existentes.
- Faça os casos de uso dependerem de interfaces de gateway, e deixe TypeORM, Oracle, Redis, Azure e APIs externas na infraestrutura.
- Registre dependências com símbolos únicos no registry Inversify e exponha somente os casos de uso necessários ao adaptador chamador.
- Reutilize factories de `mock/`; para mocks TypeScript, prefira `satisfies`, `jest.MockedFunction` ou tipos nativos do Jest. Não use casts inseguros para silenciar incompatibilidades.
- Nunca trate erros com `throw new error` ou `throw new Error`. Prefira as classes de exception já definidas pelo projeto; em aplicações NestJS, use as exceptions fornecidas pelo Nest quando não houver uma exception de domínio ou de projeto adequada.
- Use imports, nomes, caminhos e convenções já vigentes no projeto. Não acrescente dependências nem padrões paralelos sem necessidade comprovada.

## Encerramento

Revise o diff para confirmar limites de camada, cobertura de fluxos de sucesso/erro e alterações de configuração. Documente no resultado os comandos executados e os que não puderam ser executados.
