# Arquitetura de referência — ReactJS

O padrão separa lógica de negócio em `src/@core` e interface em `src/@presentation`.

```text
src/
  @core/modules/<dominio>/
    application/
    domain/{entity,gateway}/
    infra/
    __test__/
    __mock__/
  @presentation/
    modules/<dominio>/{page,component,hook,context,route}/
    components/
    config/
```

Adapte a árvore à estrutura já usada pelo projeto; não crie pastas vazias nem camadas paralelas.

## Responsabilidades

| Área | Responsabilidade |
| --- | --- |
| `domain` | Entidades, types, enums e interfaces de gateway. Sem dependência de apresentação ou infraestrutura. |
| `application` | Casos de uso, parsing, validação e orquestração de regras de negócio. |
| `infra` | Adaptadores HTTP e registries; implementa contratos sem concentrar regra de negócio. |
| `@presentation` | Páginas, componentes, hooks, contextos e rotas; consome casos de uso pelo registry. |

Um fluxo típico é: página ou hook chama um atalho do registry; o caso de uso valida e orquestra; o gateway fornece o contrato; o adaptador HTTP executa a integração. A UI recebe um resultado ou exception já apropriado ao fluxo.

## Registry

Use o registry de infraestrutura do módulo como única fronteira de consumo dos casos de uso. Crie símbolos únicos, faça bindings de contratos e exporte apenas os atalhos que os adaptadores de apresentação precisam. Compare com o módulo equivalente antes de escolher lifecycle ou tipo de binding.

```ts
import { crop } from '@core/modules/crop/infra/crop.container.registry';

await crop.create.execute(params);
```

Não faça `new CreateCropUseCase(...)` em componente, hook, rota ou página; nem importe diretamente um arquivo `*.use.case.ts` fora do registry de `infra`.

## HTTP, rotas e configuração

Gateways HTTP usam o client centralizado por DI e convertem erros ao padrão de exceptions do projeto. Rotas protegidas, autenticação e notificações reutilizam as abstrações existentes. Variáveis de browser usam `import.meta.env.VITE_*`.

Quando a demanda alterar rotas, permissões, interceptors ou configuração, use o par mais semelhante do projeto como fonte de integração e teste o fluxo de acesso autorizado e não autorizado que se aplicar.
