# Testes de frontend ReactJS

Siga as bibliotecas e scripts já configurados no `package.json`. Não presuma que o projeto usa Vitest, Jest, Testing Library ou uma API específica.

## Escopo

Para mudanças em `@core`, cubra o comportamento público das entidades, casos de uso, gateways HTTP e registries modificados. Interfaces puras podem receber teste de contrato tipado quando esse padrão existir no projeto. Mocks que só alimentam outros testes não são unidade sob teste.

Para apresentação, teste a interação observável: estados inicial, carregando, sucesso, vazio, erro, ações do usuário, validação e navegação quando afetados. Mocke a fronteira do registry ou gateway conforme o padrão local, sem testar detalhes internos de implementação.

## Convenções

- Use `describe` e `it` em inglês; preserve em português os textos de negócio apresentados ao usuário.
- Reutilize factories e mocks existentes. Mantenha mocks tipados com `satisfies` ou os tipos nativos da ferramenta, sem casts inseguros para esconder erros.
- Em casos de uso, verifique resultado, parâmetros e interações com gateways.
- Em gateway HTTP, valide request, transformação de resposta e conversão de erro sem fazer chamada de rede real.
- Em componentes e hooks, aguarde atualizações assíncronas e asserte o resultado visível ou a interação pública, não estados privados.

Execute primeiro a suíte ou arquivo diretamente impactado. Antes de encerrar, execute `yarn lint` e `yarn test` ou os equivalentes definidos pelo repositório. Registre limitações causadas por dependências de ambiente, browser, serviço ou credenciais.
