---
name: nodejs-development-eliangela
description: Desenvolver, corrigir, refatorar e testar APIs Node.js/NestJS no padrão Eliangela, especialmente projetos com TypeORM, Oracle, Inversify, Redis e BullMQ. Use ao implementar módulos ou endpoints, casos de uso, gateways, registries, workers, integrações e testes em APIs Eliangela estruturadas em `@core`, `@server` e `@worker`.
---

# Desenvolvimento Node.js Eliangela

Desenvolva mudanças aderentes à arquitetura existente. Antes de editar, inspecione `package.json`, o módulo mais semelhante e os arquivos de configuração afetados; não aplique exemplos desta skill literalmente quando divergirem do código atual.

## Fluxo

1. Delimite a camada e os efeitos da demanda: domínio, aplicação, infraestrutura, HTTP, worker, orquestração, dados ou configuração.
2. Identifique a versão de Node exigida pelo projeto em `.nvmrc`, `package.json` ou configuração equivalente. Quando a versão atual não atender ao requisito, use o NVM para instalá-la, se necessário, e selecioná-la antes de instalar dependências, testar ou executar scripts; confirme a versão com `node --version`.
3. Use `src/@core/modules/modality` como primeira referência de convenções, substituindo-a por um módulo mais próximo quando houver.
4. Preserve a direção das dependências: controller/worker → caso de uso → gateway/contrato → adaptador. Não coloque regras de negócio em controller, worker ou gateway.
5. Trabalhe em TDD: escreva o spec, execute-o para confirmar a falha, implemente o mínimo necessário e execute-o novamente. Ao criar ou ampliar testes em `@core`, inventarie todos os artefatos executáveis do escopo e crie ou complete specs para cada um, sem limitar a cobertura aos casos de uso; inclua obrigatoriamente o diretório `domain`. Crie obrigatoriamente testes de contrato tipados para cada interface em `domain/gateway`, verificando assinaturas, parâmetros e retornos esperados pelos consumidores. Não crie specs para arquivos de `mock/`: eles fornecem dados e dublês aos testes. Mantenha `describe` e `it` em inglês; mantenha mensagens de negócio em português.
6. Valide apenas no escopo necessário durante a implementação e finalize com `yarn lint`, `yarn test` e, para mudanças HTTP, dados ou integração, `yarn test:e2e`. Informe limitações de ambiente (Oracle, Redis, credenciais ou serviços externos) sem ocultá-las.

## Seleção de referência

- Para estruturar ou expandir módulo em `@core`, leia [architecture.md](references/architecture.md).
- Para criar ou revisar testes, leia [testing.md](references/testing.md). Em demandas de cobertura de `@core`, siga o inventário integral dessa referência, incluindo `domain`.
- Para jobs, filas ou fluxos agendados, leia a seção correspondente de [architecture.md](references/architecture.md) e compare com as bases comuns já existentes.
- Para E2E com dependências de dados, inspecione `architecture/e2e-test-plan.md` no repositório-alvo antes de alterar a ordem, os seeds ou as fixtures.

## Regras de implementação

- Modele entidades, value objects, DTOs e contratos no domínio; use `class-validator` e Swagger conforme os pares existentes.
- Faça os casos de uso dependerem de interfaces de gateway, e deixe TypeORM, Oracle, Redis, Azure e APIs externas na infraestrutura.
- Registre dependências com símbolos únicos no registry Inversify e exponha somente os casos de uso necessários ao adaptador chamador.
- Reutilize factories de `mock/`; para mocks TypeScript, prefira `satisfies`, `jest.MockedFunction` ou tipos nativos do Jest. Não use casts inseguros para silenciar incompatibilidades.
- Não crie funções com mais de sete parâmetros. Quando a função precisar de mais de quatro parâmetros, prefira receber um objeto tipado que nomeie e valide os dados de entrada; mantenha parâmetros posicionais apenas quando tornarem a chamada mais clara.
- Nunca trate erros com `throw new error` ou `throw new Error`. Prefira as classes de exception já definidas pelo projeto; em aplicações NestJS, use as exceptions fornecidas pelo Nest quando não houver uma exception de domínio ou de projeto adequada.
- Use imports, nomes, caminhos e convenções já vigentes no projeto. Não acrescente dependências nem padrões paralelos sem necessidade comprovada.
- Nunca faça múltiplas declarações de `import` para o mesmo arquivo. Agrupe todos os símbolos necessários em uma única declaração, usando `type` nos especificadores quando aplicável.
- Ao consumir o retorno de uma função que possa ser `null` ou `undefined`, proteja o acesso às propriedades, métodos ou índices com optional chaining (`resultado?.propriedade`). Antes de adotá-lo, avalie o contrato do fluxo: quando a ausência do objeto impedir a continuação correta da lógica, faça uma guarda explícita e encerre o fluxo com a exception de domínio/projeto apropriada, em vez de propagar `undefined` silenciosamente.

## Encerramento

Revise o diff para confirmar limites de camada, cobertura de fluxos de sucesso/erro e alterações de configuração. Documente no resultado os comandos executados e os que não puderam ser executados.
