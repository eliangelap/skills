# Testes no padrão Eliangela

## Ciclo obrigatório

Para cada artefato, crie o spec na camada correspondente, execute-o em falha, implemente o comportamento mínimo e execute-o em verde. Use as versões reais do `package.json`; não suponha APIs de Jest, NestJS, TypeORM ou Inversify.

Sequência preferencial: domínio → aplicação → infraestrutura → registry → server/worker → E2E.

## Localização e escopo

Ao receber uma demanda para testar `@core`, trate todo código executável dessa camada como escopo obrigatório. Antes de escrever specs, inventarie os arquivos de produção em `domain`, `application` e `infra`, excluindo declarações sem comportamento em runtime, como interfaces e tipos puros, e arquivos ou diretórios de `mock/`. A exceção obrigatória são as interfaces em `domain/gateway`: inclua cada uma no inventário para criar seu teste de contrato tipado. Mocks são dados e dublês fornecidos para viabilizar os testes unitários, não unidades sob teste. Não encerre a demanda com testes somente para casos de uso: cubra também todos os artefatos executáveis em `domain`, inclusive entidades, DTOs, enums, value objects, factories, mappers e serviços de domínio quando existirem.

Para cada artefato inventariado, crie um spec ou complete o spec existente. Teste o comportamento público e as ramificações relevantes; não crie testes artificiais para detalhes de implementação sem comportamento observável. Se algum artefato não puder ser testado de forma unitária, registre o motivo e aplique a forma de validação compatível com o projeto.

| Artefato | Local do spec |
| --- | --- |
| Entidade, DTO, enum ou value object | `domain/**/__test__/<arquivo>.spec.ts` |
| Interface de gateway | `domain/gateway/**/__test__/<arquivo>.spec.ts` |
| Caso de uso | `application/__test__/<arquivo>.spec.ts` |
| Gateway e registry | `infra/__test__/<arquivo>.spec.ts` |
| Controller | `@server/modules/<modulo>/__test__/<arquivo>.spec.ts` |
| Producer/consumer | junto ao módulo worker correspondente |

Para classes auxiliares, factories, mappers e serviços de domínio, siga o subdiretório `__test__` já adotado pelo módulo que os contém. Não mova testes existentes apenas para padronizar localização.

Coloque testes de domínio no subdiretório do artefato se ele existir; caso contrário, use `domain/__test__`.

## Convenções de teste

- Use `describe` e `it` em inglês; preserve textos de erros de produção em português.
- Para DTOs decorados, valide instâncias válidas e inválidas com `validate` ou `validateSync`, cobrindo cada constraint relevante.
- Para entidades TypeORM, cubra construção, colunas, defaults, campos opcionais e mutabilidade permitida.
- Para value objects, enums, mappers, factories e serviços de domínio, cubra invariantes, transformações, valores-limite, defaults e erros de domínio aplicáveis.
- Para cada interface em `domain/gateway`, crie obrigatoriamente um teste de contrato tipado. Declare o contrato esperado pelo consumidor e use asserções de tipo bidirecionais compatíveis com o projeto para garantir igualdade da assinatura de cada método, incluindo parâmetros e retorno. O spec deve falhar na compilação quando o contrato do gateway divergir; não substitua essa verificação por teste de comportamento de mock.
- Reutilize factories de `mock/`. Não crie specs unitários para mocks, pois eles são insumos de teste. Quando criar mocks de contratos, use `satisfies` e `jest.fn<ReturnType<...>, Parameters<...>>()`; não contorne tipos com `as unknown as`.
- Em casos de uso, valide resultado, parâmetros e interações observáveis com gateways. Em falhas, use as exceções oficiais do projeto.
- Em gateways, mocke `DataSource` e repositórios; não acesse Oracle. Em registries, resolva todos os símbolos exportados, mocke fábricas compartilhadas e prefira verificar instância/comportamento quando o binding for dinâmico.
- Em controllers, teste a delegação ao registry e use o módulo NestJS de teste quando o padrão local o fizer.

## E2E e validação final

Use `supertest` e `AppModule` real para E2E. Antes, confira seeds, credenciais, dependências externas e a ordem declarada das suítes. Depois de validar o escopo alterado, execute:

```bash
yarn lint
yarn test
yarn test:e2e
```

Reporte claramente qualquer comando bloqueado por ambiente ou infraestrutura.
