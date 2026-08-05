# Testes no padrão Coamo

## Ciclo obrigatório

Para cada artefato, crie o spec na camada correspondente, execute-o em falha, implemente o comportamento mínimo e execute-o em verde. Use as versões reais do `package.json`; não suponha APIs de Jest, NestJS, TypeORM ou Inversify.

Sequência preferencial: domínio → aplicação → infraestrutura → registry → server/worker → E2E.

## Localização e escopo

| Artefato | Local do spec |
| --- | --- |
| Entidade, DTO, enum ou value object | `domain/**/__test__/<arquivo>.spec.ts` |
| Caso de uso | `application/__test__/<arquivo>.spec.ts` |
| Gateway e registry | `infra/__test__/<arquivo>.spec.ts` |
| Controller | `@server/modules/<modulo>/__test__/<arquivo>.spec.ts` |
| Producer/consumer | junto ao módulo worker correspondente |

Coloque testes de domínio no subdiretório do artefato se ele existir; caso contrário, use `domain/__test__`.

## Convenções de teste

- Use `describe` e `it` em inglês; preserve textos de erros de produção em português.
- Para DTOs decorados, valide instâncias válidas e inválidas com `validate` ou `validateSync`, cobrindo cada constraint relevante.
- Para entidades TypeORM, cubra construção, colunas, defaults, campos opcionais e mutabilidade permitida.
- Reutilize factories de `mock/`. Quando criar mocks de contratos, use `satisfies` e `jest.fn<ReturnType<...>, Parameters<...>>()`; não contorne tipos com `as unknown as`.
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
