**Arquitetura API**
- **Stack Base**
  - Servico HTTP em NestJS 11 com bootstrapping em `src/main.ts:1`, habilitando validacao global, limites de payload via `body-parser` e Swagger em tempo de execucao.
  - `AppModule` (`src/app.module.ts:1`) compoe modulos funcionais, habilita ConfigModule com `.env.{NODE_ENV}`, vincula interceptador global de observabilidade e guard de permissoes, alem de iniciar cache Redis e conexao Oracle na inicializacao.

- **Estrutura em Camadas (Clean architecture/DDD)**
  - Baseia-se em NestJS modular com forte separação por domínio (@core/modules, @server/modules, @worker/modules), usando controllers → casos de uso → gateways (ex.: src/@core/modules/modality/infra/modality.container.registry.ts:1 e src/@server/modules/modality/modality.controller.ts:1).
  - Os casos de uso vivem fora da camada HTTP e dependem de interfaces/gateways; adaptadores (TypeORM, Azure Blob, Redis) ficam na pasta infra, sinalizando inspiração em clean architecture/DDD.
  - Porém, nem tudo segue estritamente o modelo “Clean Architecture” clássico: há dependência direta de Nest e Inversify nos registries, e algumas integrações compartilham containers globais.
  - Conclusão: é uma arquitetura modular em camadas com traços de clean architecture (use cases + gateways + adapters), mas não uma implementação 100% aderente aos princípios originais.
  - `@core/modules` abriga dominio seguindo pastas `domain`, `application`, `infra` e `mock`; cada modulo exporta entidades, gateways e use cases fortemente tipados.
  - Containeres Inversify (`*.container.registry.ts`) instanciam dependencias por simbolo, encapsulando adaptadores (por exemplo `src/@core/modules/modality/infra/modality.container.registry.ts:1`).
  - `@server/modules` definem controllers HTTP NestJS que consomem os casos de uso via registries do nucleo, centralizam documentacao Swagger e validacao (`src/@server/modules/modality/modality.controller.ts:1`).
  - `@worker/modules` implementam produtores/consumidores BullMQ herdando bases comuns (`src/@worker/modules/common/base.producer.ts:1` e `base.consumer.ts`) usando Redis configurado em `src/@worker/config.ts:1`.
  - `@orchestrator` sincroniza schedulers BullMQ para fluxos batch (`src/@orchestrator/orchestrator.service.ts:1`), agrupando definicoes em `flow/*`.

- **Integracoes e Infraestrutura**
  - Banco: TypeORM + Oracle com seeds via typeorm-extension; datasource configurado em `src/@core/modules/common/infra/db/config.ts:1`. `DatabaseService` gerencia reconexao/resiliencia e registra subscribers por modulo (`src/database/database.service.ts:1`).
  - Cache: clientes Redis iniciados em `src/@core/modules/common/infra/cache/config.ts:1`, armazenados no container global (`src/@core/modules/common/infra/container.ts:1`).
  - Storage: adaptador Azure Blob com operacoes de upload, tags e SAS token (`src/@core/modules/storage/infra/storage.fs.gateway.ts:1`).
  - Observabilidade: Application Insights configurado condicionalmente e interceptor que rastreia requests/responses (`src/@core/modules/common/infra/observability/http/http-observability.interceptor.ts:1`).

- **Seguranca e Controle de Acesso**
  - Middleware opcionais para headers e sessao comentados em `AppModule.configure`.
  - `PermissionGuard` (`src/@server/modules/permission/permission.guard.ts:1`) injeta metadados via decorator e consulta container de permissoes; atualmente usa ID placeholder, exigindo integracao futura com autenticacao real.
  - OAuth e sessao expostas via `@app/middlewares` e registries em `@core/modules/oauth`.

- **Fluxo de Requisicao**
  - Controller recebe request, aplica validacao, resolve usuario via OAuth registry, delega a use cases que orquestram gateways (DB, cache, storage).
  - Gateways transformam chamadas em queries TypeORM ou integracoes externas, retornando DTOs/entidades para os casos de uso e controladores.
  - Interceptadores/loggers registram metricas; guard bloqueia se permissao inexistente.

- **Trabalho Assincrono**
  - Producers adicionam jobs com opcoes padrao (`producerJobOptions`), Consumers herdam retry/backoff configuraveis e executam casos de uso; ambos registrando eventos de observabilidade por modulo.
  - Orquestrador garante que schedulers declarativos permaneçam sincronizados com as filas configuradas, removendo obsoletos e subindo novos automaticamente.

- **Configuracao e Deploy**
  - Dockerfile + compose (raiz) suportam execucao containerizada.
  - Scripts Yarn cobrem build obfuscado, seeds, testes, lint e releases (`package.json:1`).
  - Ambiente definido por `.env.{env}` com flags utilitarias em `src/environnements.ts:1` (ex.: `isDev`, `isProd`, `isPrdSeed`).
  - Sonar, Husky/Commitlint e testes Jest (`jest.setup.ts`, `test/*`) reforcam qualidade.
