# Arquitetura de referência

## Estrutura e responsabilidades

O padrão de referência é uma API NestJS modular, com TypeORM/Oracle, Redis, BullMQ e registries Inversify. A separação principal é:

- `src/@core/modules/<modulo>`: domínio, aplicação, infraestrutura e mocks.
- `src/@server/modules/<modulo>`: controllers NestJS, validação de entrada e documentação Swagger.
- `src/@worker/modules/<modulo>`: producers e consumers BullMQ, baseados nas classes comuns.
- `src/@orchestrator`: sincronização dos schedulers e fluxos batch.

Fluxo esperado: adaptador HTTP ou worker → caso de uso → contrato de gateway → adaptador de infraestrutura. O `AppModule` compõe os módulos, a configuração e os componentes globais; não mova regra de negócio para ele.

## Novo módulo de domínio

Use como molde um módulo existente, preferencialmente `modality`. Organize somente as pastas necessárias:

```text
src/@core/modules/<modulo>/
  domain/{entity,gateway,value-object}/
  application/
  infra/
  mock/
```

Crie entidades TypeORM e DTOs no domínio, com nomes de tabela/coluna e decorators compatíveis com o banco e o módulo de referência. Defina interfaces de gateway antes de seus adaptadores. Faça cada caso de uso receber o contrato pelo construtor e expor `execute`.

Em `infra`, implemente apenas o gateway com `DataSource` ou a integração específica. Parsers, normalizações e validações de entrada, contrato ou negócio pertencem a `application`, nunca ao adaptador de infraestrutura. Quando forem responsabilidades autônomas, crie casos de uso separados, com contratos e testes próprios, e componha-os no fluxo que deles precisar. No registry, crie `Symbol.for(...)` exclusivos, faça os bindings do container e exporte apenas os atalhos de casos de uso exigidos pelos consumidores. Compare o registry com o módulo de referência antes de escolher entre `toConstantValue` e `toDynamicValue`.

## Adaptadores

Controllers recebem parâmetros, aplicam os decorators e delegam ao caso de uso resolvido no registry. Atualize o módulo NestJS, `AppModule`, documentação Swagger e permissões somente se o módulo equivalente o fizer.

Para trabalho assíncrono, derive producer e consumer das bases comuns. Preserve opções de retry/backoff, instrumentação e a configuração central de Redis. Para novos schedulers, atualize as definições declarativas do orquestrador, em vez de criar loops próprios.

Ao adicionar subscribers TypeORM, valide a necessidade e registre-os no `DatabaseService`. Mantenha cache, storage, observabilidade e OAuth como adaptadores de infraestrutura, usando os registries e fábricas existentes.

## Configuração e dados

Leia as variáveis em `.env.{NODE_ENV}` e a configuração de banco antes de alterar conexões. Não execute seeds, E2E ou filas contra infraestrutura real sem as variáveis e o ambiente adequados. Mudanças que dependam de PK/FK devem respeitar a ordem de seeds e suítes E2E documentada no projeto.
