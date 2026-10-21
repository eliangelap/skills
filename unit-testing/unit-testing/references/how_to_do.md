**Guia TDD completo: criando um módulo em `src/@core`**

Este roteiro reproduz exatamente como um desenvolvedor deve construir um módulo seguindo os padrões existentes (ex.: `modality`, `unit`). Cada etapa possui o que escrever primeiro (teste), os imports esperados e o código mínimo para fazê-lo passar. Não pule etapas.

---

### 0. Diagnóstico inicial
1. **Estudar um módulo pronto**: navegue por `src/@core/modules/modality` para entender a convenção.
   ```bash
   tree -I '__*|mock' src/@core/modules/modality
   ```
2. Verifique os pontos-chave já existentes:
   - Entidade TypeORM (`src/@core/modules/modality/domain/entity/modality.entity.ts:1`).
   - Interface do gateway (`src/@core/modules/modality/domain/gateway/modality.gateway.ts:1`).
   - Caso de uso (`src/@core/modules/modality/application/get.use.case.ts:1`).
   - Registry Inversify (`src/@core/modules/modality/infra/modality.container.registry.ts:1`).
   - Testes de aplicação (`src/@core/modules/modality/application/__test__/get.use.case.spec.ts:1`).
3. Tenha claras as operações do novo domínio (CRUD, sincronia, etc.).

---

### 1. Montar a estrutura de pastas
```bash
mkdir -p src/@core/modules/<modulo>/domain/{entity,gateway,value-object,__test__}
mkdir -p src/@core/modules/<modulo>/application/__test__
mkdir -p src/@core/modules/<modulo>/infra/__test__
mkdir -p src/@core/modules/<modulo>/mock
```
Estrutura resultante:
```text
src/@core/modules/<modulo>/
  domain/
    entity/
    gateway/
    value-object/
    __test__/
  application/
    __test__/
  infra/
    __test__/
  mock/
```

---

### 2. TDD do domínio (entidades e value objects)
1. **Escreva primeiro o teste da entidade** em `src/@core/modules/<modulo>/domain/__test__/<modulo>.entity.spec.ts`:
   ```ts
   import { <Modulo> } from '../entity/<modulo>.entity';

   describe('<Modulo> entity', () => {
       it('cria instância válida', () => {
           const entity = new <Modulo>('id-123', 'Nome', new Date());
           expect(entity.id).toBe('id-123');
       });

       it('lança erro se nome vazio', () => {
           expect(() => new <Modulo>('id', '', new Date())).toThrow('Nome obrigatório');
       });
   });
   ```
2. Execute o teste para confirmar que falha: `yarn test <modulo>.entity.spec.ts`.
3. **Implemente a entidade** em `src/@core/modules/<modulo>/domain/entity/<modulo>.entity.ts` com imports TypeORM idênticos ao padrão:
   ```ts
   import {
       Column,
       Entity,
       PrimaryGeneratedColumn,
   } from 'typeorm';
   import { BasePermissionEntity } from '@core/modules/common/entity/basePermission.entity';

   @Entity('<TABELA_ORACLE>')
   export class <Modulo> extends BasePermissionEntity {
       @PrimaryGeneratedColumn('uuid', { name: 'ID_<MODULO>' })
       id: string;

       @Column({ name: 'NM_<MODULO>', length: 200 })
       name: string;

       constructor(id: string, name: string, createdAt: Date) {
           super();
           if (!id) throw new Error('ID obrigatório');
           if (!name) throw new Error('Nome obrigatório');
           this.id = id;
           this.name = name;
           this.createdAt = createdAt;
       }
   }
   ```
4. Rodar novamente `yarn test <modulo>.entity.spec.ts` até passar.
5. **Value objects** (se necessários): escreva teste semelhante em `value-object/__test__`, depois implemente em `value-object/<vo>.ts` seguindo `src/@core/modules/document/domain/value-object`.

---

### 3. Contratos e DTOs
1. **Escreva testes de validação** para DTOs em `domain/__test__/<modulo>.entities.spec.ts` usando `class-validator` para espelhar `src/@core/modules/modality/domain/entity/modality.entities.ts:1`.
   ```ts
   import { validate } from 'class-validator';
   import { TCreate } from '../entity/<modulo>.entities';

   it('falha se name < 3 caracteres', async () => {
       const dto = new TCreate();
       dto.name = 'ab';
       const errors = await validate(dto);
       expect(errors[0].constraints?.minLength).toBeDefined();
   });
   ```
2. Rode o teste (falha). `yarn test <modulo>.entities.spec.ts`.
3. **Implemente DTOs** em `domain/entity/<modulo>.entities.ts`, copiando o padrão de imports presentes em `modality.entities.ts`:
   ```ts
   import { ApiProperty } from '@nestjs/swagger';
   import { IsNotEmpty, IsString, MinLength, MaxLength } from 'class-validator';

   export class TCreate {
       @ApiProperty({ example: 'Nome' })
       @IsNotEmpty()
       @IsString()
       @MinLength(3)
       @MaxLength(200)
       name: string;
   }
   ```
4. Ajuste até os testes de validação passarem.

---

### 4. Interface do gateway
1. **Crie o teste que usa o gateway** antes da implementação no passo seguinte (caso de uso). Aproveite para definir o contrato no spec.
2. **Escreva a interface** em `domain/<modulo>.gateway.ts`, imitando `src/@core/modules/modality/domain/modality.gateway.ts:1`:
   ```ts
   import { <Modulo> } from '../entity/<modulo>.entity';
   import * as BaseEntities from '@core/modules/common/entity/base.entities';
   import { TCreate } from '../entity/<modulo>.entities';

   export interface <Modulo>Gateway {
       get(params: BaseEntities.TId): Promise<<Modulo> | undefined>;
       create(params: TCreate): Promise<<Modulo>>;
   }
   ```
3. Não rode testes ainda; a verificação acontecerá pelos casos de uso.

---

### 4.1 Interface do gateway que estão no diretório em domain
1. **Crie o teste que usa o gateway** antes da implementação no passo seguinte (caso de uso). Aproveite para definir o contrato no spec.
2. **Escreva a interface** em `domain/<modulo>.gateway.ts`, imitando `src/@core/modules/modality/domain/modality.gateway.ts:1`:
   ```ts
   import { <Modulo> } from '../entity/<modulo>.entity';
   import * as BaseEntities from '@core/modules/common/entity/base.entities';
   import { TCreate } from '../entity/<modulo>.entities';

   export interface <Modulo>Gateway {
       get(params: BaseEntities.TId): Promise<<Modulo> | undefined>;
       create(params: TCreate): Promise<<Modulo>>;
   }
   ```
3. Não rode testes ainda; a verificação acontecerá pelos casos de uso.

---

### 5. TDD dos casos de uso (`application`)
1. **Escreva o teste do primeiro caso de uso** em `application/__test__/get.use.case.spec.ts`, seguindo `src/@core/modules/modality/application/__test__/get.use.case.spec.ts:1`:
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
           expect(result.id).toBe('id-123');
       });
   });
   ```
2. Rode o teste e confirme falha: `yarn test get.use.case.spec.ts`.
3. **Crie o mock** em `mock/<modulo>.mock.ts` antes de implementar o caso de uso:
   ```ts
   import { <Modulo> } from '../domain/entity/<modulo>.entity';

   export const make<Modulo> = (override?: Partial<<Modulo>>) =>
       Object.assign(new <Modulo>('id-123', 'Nome', new Date()), override);
   ```
4. **Implemente o caso de uso** em `application/get.use.case.ts` exatamente como o padrão:
   ```ts
   import { <Modulo>Gateway } from '../domain/gateway/<modulo>.gateway';
   import { TId } from '@core/modules/common/entity/base.entities';
   import { <Modulo> } from '../domain/entity/<modulo>.entity';

   export class GetUseCase {
       constructor(private readonly gateway: <Modulo>Gateway) {}

       async execute(params: TId): Promise<<Modulo> | undefined> {
           return this.gateway.get({ id: params.id });
       }
   }
   ```
5. Rode novamente `yarn test get.use.case.spec.ts` até passar.
6. Repita o ciclo TDD para outros casos (`create`, `update`, `pagination`). Use os specs existentes como modelo, por exemplo `src/@core/modules/modality/application/__test__/create.use.case.spec.ts:1`.

---

### 6. Gateway concreto com TDD (`infra`)
1. **Escreva o teste do gateway** em `infra/__test__/<modulo>.db.gateway.spec.ts` usando `jest` e mocks de `DataSource`, seguindo `src/@core/modules/storage/infra/__test__/storage.fs.gateway.spec.ts` ou `modality`:
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
2. Rode o teste (falha): `yarn test <modulo>.db.gateway.spec.ts`.
3. **Implemente o gateway** em `infra/<modulo>.db.gateway.ts` com imports reais iguais aos de `src/@core/modules/modality/infra/modality.db.gateway.ts:1`:
   ```ts
   import { DataSource } from 'typeorm';
   import { <Modulo>Gateway } from '../domain/gateway/<modulo>.gateway';
   import { <Modulo> } from '../domain/entity/<modulo>.entity';
   import * as BaseEntities from '@core/modules/common/entity/base.entities';
   import { TCreate } from '../domain/entity/<modulo>.entities';

   export class <Modulo>DbGateway implements <Modulo>Gateway {
       constructor(private readonly dbInstance: DataSource) {}
       private readonly repository = this.dbInstance.getRepository(<Modulo>);

       async get(params: BaseEntities.TId): Promise<<Modulo> | undefined> {
           return this.repository.findOne({ where: { id: params.id } });
       }

       async create(params: TCreate): Promise<<Modulo>> {
           const entity = this.repository.create(params);
           return this.repository.save(entity);
       }
   }
   ```
4. Rodar novamente `yarn test <modulo>.db.gateway.spec.ts` até verde.
5. Adicione demais métodos (`update`, `paginate`, etc.) sempre escrevendo o teste antes.

---

### 7. Registry Inversify
1. **Escreva o teste de integração do registry** em `infra/__test__/<modulo>.container.registry.spec.ts`:
   ```ts
   import * as Registry from '../<modulo>.container.registry';
   import { GetUseCase } from '../../application/get.use.case';

   it('resolve GetUseCase a partir do container', () => {
       expect(Registry.<modulo>.get).toBeInstanceOf(GetUseCase);
   });
   ```
2. Rodar o teste (falha). `yarn test <modulo>.container.registry.spec.ts`.
3. **Implementar o registry** em `infra/<modulo>.container.registry.ts`, copiando o padrão de `src/@core/modules/modality/infra/modality.container.registry.ts:1`:
   ```ts
   import 'reflect-metadata';
   import { Container } from 'inversify';
   import { db } from '../../common/infra/db/config';
   import { <Modulo>DbGateway } from './<modulo>.db.gateway';
   import { GetUseCase } from '../application/get.use.case';

   export const Registry = {
       dbInstance: Symbol.for('<Modulo>DbInstance'),
       Gateway: Symbol.for('<Modulo>Gateway'),
       GetUseCase: Symbol.for('<Modulo>GetUseCase'),
   } as const;

   const container = new Container();

   container.bind(Registry.dbInstance).toConstantValue(db);
   container
       .bind(Registry.Gateway)
       .toDynamicValue((ctx) => new <Modulo>DbGateway(ctx.get(Registry.dbInstance)));
   container
       .bind(Registry.GetUseCase)
       .toDynamicValue((ctx) => new GetUseCase(ctx.get(Registry.Gateway)));

   export const <modulo> = {
       get: container.get<GetUseCase>(Registry.GetUseCase),
   };
   ```
4. Rodar o teste do registry até passar.

---

### 8. Integrar com `@server` (se houver endpoints)
1. **Escreva o teste do controller** em `src/@server/modules/<modulo>/__test__/<modulo>.controller.spec.ts` usando `@nestjs/testing`, como em `src/@server/modules/modality/__test__/modality.controller.spec.ts`.
   ```ts
   import { Test } from '@nestjs/testing';
   import { ModuloController } from '../<modulo>.controller';
   import * as Registry from '../../../@core/modules/<modulo>/infra/<modulo>.container.registry';

   describe('<Modulo>Controller', () => {
       it('GET /:id usa Registry.<modulo>.get', async () => {
           jest.spyOn(Registry.<modulo>.get, 'execute').mockResolvedValueOnce({ id: 'id' } as any);
           const moduleRef = await Test.createTestingModule({ controllers: [ModuloController] }).compile();
           const controller = moduleRef.get(ModuloController);
           await controller.get('id');
           expect(Registry.<modulo>.get.execute).toHaveBeenCalledWith({ id: 'id' });
       });
   });
   ```
2. Faça o teste falhar.
3. **Implemente controller e módulo**:
   - `src/@server/modules/<modulo>/<modulo>.controller.ts`
     ```ts
     import * as Nest from '@nestjs/common';
     import * as Registry from '../../../@core/modules/<modulo>/infra/<modulo>.container.registry';

     @Nest.Controller('api/v1/<modulo>')
     export class ModuloController {
         @Nest.Get('/:id')
         async get(@Nest.Param('id') id: string) {
             return Registry.<modulo>.get.execute({ id });
         }
     }
     ```
   - `src/@server/modules/<modulo>/<modulo>.module.ts`
     ```ts
     import { Module } from '@nestjs/common';
     import { ModuloController } from './<modulo>.controller';

     @Module({ controllers: [ModuloController] })
     export class ModuloModule {}
     ```
4. Adicionar `ModuloModule` em `AppModule` (exemplo em `src/app.module.ts:25`).
5. Rodar `yarn test` no spec do controller até verde.

---

### 9. Workers / Orquestrador (se aplicável)
1. Escreva testes para producers/consumers baseados em `src/@worker/modules/modality`.
2. Implementar classes herdando `BaseProducer`/`BaseConsumer` e validar com testes.
3. Atualizar `src/@worker/worker.module.ts:1` com novos providers e exports.

---

### 10. Subscribers e inicialização
1. Se for necessário disparar eventos do TypeORM, crie teste para subscriber em `infra/__test__/<modulo>.subscriber.spec.ts`, similar a `src/@core/modules/modality/infra/modality.subscriber.ts:1`.
2. Registrar o subscriber no `DatabaseService` (`src/database/database.service.ts:29`) adicionando instância ao array `db.subscribers`.

---

### 11. Documentação e observabilidade
1. Adicionar documentação Swagger em `@server/modules/<modulo>/documentation.ts` (veja `src/@server/modules/modality/documentation.ts`).
2. Criar decorator config se necessário (`@server/config/documentation.decorator.ts`).
3. Atualizar `arquitetura/detalhes.md` com um resumo do novo módulo.

---

### 12. Rodada final de TDD
1. Executar suite completa:
   ```bash
   yarn lint
   yarn test
   yarn test:e2e
   ```
2. Subir aplicação (`yarn start:dev`) e validar rota manualmente.
3. Se usar seeds/queues, rodar `yarn seed:run` e observar logs de `DatabaseService` (`src/database/database.service.ts:10`).

Checklist final:
- [ ] Todos os testes de domínio, aplicação, infra e server escritos antes do código produtivo.
- [ ] Entidade, DTOs e gateway alinhados com padrões (`modality` como referência).
- [ ] Registry expõe casos de uso via objeto `export const <modulo>`.
- [ ] Controller/worker usam apenas casos de uso resolvidos pelo registry.
- [ ] Documentação e subscribers atualizados.
- [ ] `yarn lint`, `yarn test`, `yarn test:e2e` concluídos.

Seguindo esse passo a passo TDD, o módulo nasce testado ponta a ponta e consistente com os padrões de `@core/modules/*`.
