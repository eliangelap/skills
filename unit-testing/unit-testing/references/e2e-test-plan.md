# Plano de Execução dos Testes E2E

## Objetivo
- Garantir ordem determinística na suíte E2E para que dependências de dados (PK/FK) sejam respeitadas.
- Documentar quais entidades e _seeds_ sustentam cada cenário para facilitar manutenção da pipeline.

## Preparação do Ambiente
- Banco Oracle acessível e variáveis `DB_TNS`, `DB_USER`, `DB_PASSWORD` configuradas.
- Executar _seeds_ com `NODE_ENV=test yarn seed:run` para popular as tabelas conforme `src/@core/modules/common/infra/db/seeds/scripts`.
- Gerar artefatos de build (`yarn build`) antes do comando de _seed_, conforme script existente.

## Comando de Execução Ordenada
- Novo script `yarn test:e2e:ordered` usa `test/e2e-order.json` e garante execução `--runInBand`.
- `yarn test:e2e:ordered --list` imprime a ordem configurada sem rodar o Jest.

## Fluxo Sugerido (PK/FK)

| Ordem | Suíte (`test/e2e-order.json`) | Entidades principais / FK | Seeds ou Fonte |
|-------|-------------------------------|---------------------------|----------------|
| 1 | `src/@server/modules/access/__test__/access.controller.e2e-spec.ts` | Solicitação de acesso, componentes OAuth | Seeds de pessoa e componentes OAuth |
| 2 | `src/@server/modules/accountManagement/__test__/accountManagement.controller.e2e-spec.ts` | `AccountManagement` (PK `id`) | `20250703092538_create_account_management.seed.ts` |
| 3 | `src/@server/modules/state/__test__/state.controller.e2e-spec.ts` | `State` (PK `code`), `City.stateCode` | `20250820101802_create_states.seed.ts` + base de municípios (pré-carregada) |
| 4 | `src/@server/modules/address/__test__/address.controller.e2e-spec.ts` | Tipos de endereço/logradouro (valores enum) | Sem dependência de tabela, lógica em código |
| 5 | `src/@server/modules/phone/__test__/phone.controller.e2e-spec.ts` | Tipos de telefone (enum) | Sem dependência de tabela |
| 6 | `src/@server/modules/email/__test__/email.controller.e2e-spec.ts` | Tipos de e-mail (enum) | Sem dependência de tabela |
| 7 | `src/@server/modules/indicator/__test__/indicator.controller.e2e-spec.ts` | Indicadores financeiros/metereológicos | Requer componentes OAuth (`20250908103912_component.seed.ts`) |
| 8 | `src/@server/modules/cycle/__test__/cycle.controller.e2e-spec.ts` | Ciclos (`Cycle`) | Dados estáticos do módulo (`ECycleType`) |
| 9 | `src/@server/modules/managementArea/__test__/managementArea.controller.e2e-spec.ts` | `ManagementArea.accountManagementId` FK | Depende de `AccountManagement` seed |
| 10 | `src/@server/modules/miscellaneousArea/__test__/miscellaneousArea.controller.e2e-spec.ts` | `MiscellaneousArea.managementAreaId` (1:1) | Cria `ManagementArea` em tempo de teste, usa `accountManagementData` |
| 11 | `src/@server/modules/field/__test__/field.controller.e2e-spec.ts` | `Field.managementAreaId` FK | Necessita `ManagementArea` pré-existente (ID `123e4567-e89b-12d3-a456-426614174000`) |
| 12 | `src/@server/modules/standardUnitMeasurement/__test__/standardUnitMeasurement.controller.e2e-spec.ts` | `StandardUnitMeasurement` FK -> `AccountManagement`, `MasterRecord` | `20250703100126_create_standard_unit_measurement.seed.ts` |
| 13 | `src/@server/modules/financialGroupType/__test__/financialGroupType.controller.e2e-spec.ts` | `FinancialGroupType.accountManagementId`, `masterRecordId` | `20250703104215_create_financial_group_type.seed.ts` |
| 14 | `src/@server/modules/financialGroup/__test__/financialGroup.controller.e2e-spec.ts` | `FinancialGroup.financialGroupTypeId`, `accountManagementId` | `20250703110810_create_financial_group.seed.ts` |
| 15 | `src/@server/modules/modality/__test__/modality.controller.e2e-spec.ts` | `modality.accountManagementId`, `masterRecordId` | `20250703101521_create_modality.seed.ts` + `20250703093830_create_master_record.seed.ts` |
| 16 | `src/@server/modules/agriculturalProduct/__test__/agriculturalProduct.controller.e2e-spec.ts` | `AgriculturalProduct.modalityId`, `accountManagementId` | Depende de `modality` e `MasterRecord` seeds (ver itens 2, 15) |
| 17 | `src/@server/modules/product/__test__/product.controller.e2e-spec.ts` | `Product.financialGroupId`, `standardUnitMeasurementId` | `20250710135439_create_product.seed.ts`, `StandardUnitSeed`, `financialGroupE2eSeed` |
| 18 | `src/@server/modules/partner/__test__/partner.controller.e2e-spec.ts` | `Partner.accountManagementId`, `personId` + `Person` agregados | `20250617140000_create_person_init.ts`, `20250617140001_create_user_document_init.ts`, `20250703093830_create_master_record.seed.ts` |
| 19 | `src/@server/modules/example/__test__/example.controller.e2e-spec.ts` | Entidade exemplo independente | Sem dependência externa |

## Notas e Riscos
- **Autenticação**: todas as suítes (exceto `access`) usam `Registry.oauth.getAccess.admin()`; garantir que `Component` e `AccountComponent` seeds estejam ajustados ao usuário de teste (`UserData.id`).
- **Área de gestão**: validar que a base de teste contém `ManagementArea` com UUID `123e4567-e89b-12d3-a456-426614174000`; caso contrário, incluir _seed_ específico ou criar _fixture_ anterior ao teste de `field`.
- **Dados compartilhados**: suítes `product`, `financialGroup`, `financialGroupType` e `standardUnitMeasurement` compartilham registros auditados; manter execução sequencial evita conflitos ao limpar auditorias.
- **Reexecução**: `yarn test:e2e:ordered --list` ajuda a alinhar pipeline (pode ser consumido por `CI` para montar etapas paralelas, se desejado).
- **Ambiente legado**: testes como `indicator` dependem de integração externa; considere _mocks_ ou feature flags caso o endpoint não esteja disponível no ambiente de CI.
