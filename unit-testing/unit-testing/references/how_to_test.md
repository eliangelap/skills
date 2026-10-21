**Passo a passo de testes unitários por camada**

Este guia explica, em ordem de execução, como um desenvolvedor deve criar testes unitários para cada artefato do módulo `@core`. Use os módulos existentes (ex.: `modality`) como referência para imports e estilo.

---

### 1. Domínio – Entidades (`domain/entity`)
1. **Criar o teste primeiro** em `src/@core/modules/<modulo>/domain/__test__/<modulo>.entity.spec.ts`.
   ```ts
   import { <Modulo> } from '../entity/<modulo>.entity';

   describe('<Modulo> entity', () => {
       it('atribui propriedades corretamente', () => {
           const entity = new <Modulo>('id-123', 'Nome', new Date());
           expect(entity.id).toBe('id-123');
       });

       it('lança erro quando nome vazio', () => {
           expect(() => new <Modulo>('id', '', new Date())).toThrow('Nome obrigatório');
       });
   });
   ```
2. **Rodar** `yarn test src/@core/modules/<modulo>/domain/__test__/<modulo>.entity.spec.ts` (falha prevista).
3. **Implementar a entidade** com imports TypeORM conforme `src/@core/modules/modality/domain/entity/modality.entity.ts:1`.
4. Reexecutar o teste até passar.

---

### 2. Domínio – DTOs/Validators (`domain/entity/*.entities.ts`)
1. **Criar teste** `src/@core/modules/<modulo>/domain/__test__/<modulo>.entities.spec.ts` usando `class-validator`:
   ```ts
   import { validate } from 'class-validator';
   import { TCreate } from '../entity/<modulo>.entities';

   describe('TCreate validator', () => {
       it('exige nome com ao menos 3 caracteres', async () => {
           const dto = new TCreate();
           dto.name = 'ab';
           const errors = await validate(dto);
           expect(errors[0].constraints?.minLength).toBeDefined();
       });
   });
   ```
2. Rodar `yarn test <modulo>.entities.spec.ts` (falha).
3. **Implementar DTO** replicando imports de `src/@core/modules/modality/domain/entity/modality.entities.ts:1`.
4. Reexecutar testes.

---

### 3. Mock Factories (`mock`)
1. Criar `src/@core/modules/<modulo>/mock/<modulo>.mock.ts` **antes** dos testes que dependem de dados fakes:
   ```ts
   import { <Modulo> } from '../domain/entity/<modulo>.entity';

   export const make<Modulo> = (override?: Partial<<Modulo>>) =>
       Object.assign(
           new <Modulo>('id-123', 'Nome', new Date()),
           override,
       );
   ```
2. Utilize `make<Modulo>` nos testes das camadas subsequentes.

---

### 4. Casos de Uso (`application/*.use.case.ts`)
1. **Escreva teste** em `src/@core/modules/<modulo>/application/__test__/<acao>.use.case.spec.ts`, copiando estrutura de `src/@core/modules/modality/application/__test__/get.use.case.spec.ts:1`:
   ```ts
   import { GetUseCase } from '../get.use.case';
   import { <Modulo>Gateway } from '../../domain/gateway/<modulo>.gateway';
   import { make<Modulo> } from '../../mock/<modulo>.mock';

   describe('GetUseCase', () => {
       it('retorna entidade quando gateway encontra', async () => {
           const gateway = { get: jest.fn().mockResolvedValue(make<Modulo>()) } as jest.Mocked<<Modulo>Gateway>;
           const useCase = new GetUseCase(gateway);

           const result = await useCase.execute({ id: 'id-123' });

           expect(gateway.get).toHaveBeenCalledWith({ id: 'id-123' });
           expect(result?.id).toBe('id-123');
       });
   });
   ```
2. Rodar `yarn test src/@core/modules/<modulo>/application/__test__/<acao>.use.case.spec.ts` (falha).
3. **Implementar o caso de uso** importando contratos via `@core/modules/common/entity/base.entities` assim como `src/@core/modules/modality/application/get.use.case.ts:1`.
4. Repetir para outros casos (`create`, `update`, etc.).

---

### 5. Gateways Concretos (`infra/<modulo>.db.gateway.ts` ou outros)
1. **Testes** em `src/@core/modules/<modulo>/infra/__test__/<modulo>.db.gateway.spec.ts` seguindo `src/@core/modules/modality/infra/__test__/modality.db.gateway.spec.ts`:
   ```ts
   import { DataSource } from 'typeorm';
   import { <Modulo>DbGateway } from '../<modulo>.db.gateway';
   import { make<Modulo> } from '../../mock/<modulo>.mock';

   describe('<Modulo>DbGateway', () => {
       const repository = { findOne: jest.fn() };
       const dataSource = { getRepository: jest.fn().mockReturnValue(repository) } as unknown as DataSource;
       const gateway = new <Modulo>DbGateway(dataSource);

       it('get retorna entidade', async () => {
           repository.findOne.mockResolvedValue(make<Modulo>());
           const result = await gateway.get({ id: 'id-123' });
           expect(result?.id).toBe('id-123');
       });
   });
   ```
2. Comando: `yarn test src/@core/modules/<modulo>/infra/__test__/<modulo>.db.gateway.spec.ts`.
3. **Implementar gateway** importando `DataSource`, `QueryRunner`, tipos de DTO como em `src/@core/modules/modality/infra/modality.db.gateway.ts:1`.
4. Acrescentar testes para métodos `create`, `update`, `paginate` usando mocks de `repository.create`, `repository.save`, etc.

---

### 6. Registry Inversify (`infra/<modulo>.container.registry.ts`)
1. **Teste** em `infra/__test__/<modulo>.container.registry.spec.ts`:
   ```ts
   import * as Registry from '../<modulo>.container.registry';
   import { GetUseCase } from '../../application/get.use.case';

   describe('<Modulo> registry', () => {
       it('resolve GetUseCase', () => {
           expect(Registry.<modulo>.get).toBeInstanceOf(GetUseCase);
       });
   });
   ```
2. Rodar `yarn test .../<modulo>.container.registry.spec.ts` (falha até fazer binding).
3. **Implementar** container copiando padrão de `src/@core/modules/modality/infra/modality.container.registry.ts:1`, garantindo `Symbol.for` únicos.
4. Reexecutar teste.

---

### 7. Controllers (`src/@server/modules/<modulo>`)
1. **Teste unitário** em `src/@server/modules/<modulo>/__test__/<modulo>.controller.spec.ts` seguindo `src/@server/modules/modality/__test__/modality.controller.spec.ts`:
   ```ts
   import { Test } from '@nestjs/testing';
   import { ModuloController } from '../<modulo>.controller';
   import * as Registry from '../../../@core/modules/<modulo>/infra/<modulo>.container.registry';

   describe('<Modulo>Controller', () => {
       it('GET /:id chama registry', async () => {
           jest.spyOn(Registry.<modulo>.get, 'execute').mockResolvedValue({ id: 'id' } as any);
           const moduleRef = await Test.createTestingModule({ controllers: [ModuloController] }).compile();
           const controller = moduleRef.get(ModuloController);

           await controller.get('id');
           expect(Registry.<modulo>.get.execute).toHaveBeenCalledWith({ id: 'id' });
       });
   });
   ```
2. Rodar `yarn test src/@server/modules/<modulo>/__test__/<modulo>.controller.spec.ts`.
3. **Implementar controller** importando decoradores `@nestjs/common` e registries conforme padrão.

---

### 8. Testes E2E (`test/*.e2e-spec.ts`)
1. Criar arquivo `test/<modulo>.e2e-spec.ts` similar a `test/example.e2e-spec.ts` (ou existente).
2. Usar `supertest` com `INestApplication`, carregando `AppModule` real.
3. Comando único: `yarn test:e2e` (config em `test/jest-e2e.json`).

---

### 9. Workers (`src/@worker/modules/<modulo>`)
1. **Producers** (`producer.spec.ts`): usar `jest.spyOn(queue, 'add')` igual a `src/@worker/modules/common/__test__/base.producer.spec.ts`.
2. **Consumers**: validar método `execute` com mocks conforme `src/@worker/modules/common/__test__/base.consumer.spec.ts`.
3. **Config**: se criar conexões extras, testar `getConnection` (veja `src/@worker/__test__/worker.module.spec.ts`).
4. Comando: `yarn test src/@worker/modules/<modulo>`.

---

### 10. Database Service (`src/database`)
1. Testar reconexão e registro de subscribers.
2. Mockar `db.initialize`, `db.query`, `Logger`.
3. Escrever em `src/database/__test__/database.service.spec.ts` e rodar `yarn test src/database`.

---

### 11. Observabilidade e Cache (`src/@core/modules/common/infra`)
1. Mockar `applicationinsights`, `redis` conforme necessidade.
2. Exemplos: `src/@core/modules/common/infra/__test__/observability.spec.ts` (se existir ou criar).
3. Comando: `yarn test src/@core/modules/common`.

---

### 12. Sequência TDD recomendada
1. Domínio → Application → Infra → Registry → Server/Worker → E2E.
2. Em cada etapa:
   - Escreva o teste (rodará em vermelho).
   - Implemente o código mínimo.
   - Reexecute o teste até verde.
3. Finalize com:
   ```bash
   yarn lint
   yarn test
   yarn test:e2e
   ```

Seguindo este roteiro, cada tipo de arquivo terá testes consistentes com os padrões atuais, garantindo que novos módulos e funcionalidades mantenham a mesma qualidade do código existente.
