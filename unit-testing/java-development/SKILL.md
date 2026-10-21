---
name: java-development
description: Desenvolver, corrigir, refatorar e testar aplicações Java 22 com Spring Boot, Hibernate e Clean Architecture. Use para APIs, casos de uso, persistência, integrações e testes; não use para apenas revisar diffs.
---

# Desenvolvimento Java

Implemente a demanda respeitando a arquitetura e as convenções verificáveis do repositório. Antes de editar, leia o `pom.xml` ou `build.gradle`, as configurações afetadas e um módulo equivalente; esta skill orienta decisões, mas não substitui o padrão concreto da aplicação.

## Fluxo de trabalho

1. Delimite o impacto entre domínio, aplicação, adaptadores de entrada, infraestrutura, dados, configuração e integração externa.
2. Identifique a versão efetiva do Java e as versões de Spring Boot, Hibernate e bibliotecas de teste declaradas pelo projeto. Não introduza APIs do Java 22 nem dependências incompatíveis com esse conjunto.
3. Preserve a direção das dependências: controlador, consumidor ou job → caso de uso → porta de entrada/saída → adaptador. O domínio e a aplicação não dependem de Spring, JPA/Hibernate, HTTP ou detalhes de banco.
4. Escreva ou ajuste os testes antes da implementação quando o fluxo for novo ou corrigir um defeito; confirme a falha, implemente o mínimo necessário e execute-os novamente.
5. Valide primeiro o escopo alterado. Ao terminar, execute o formatter, análise estática e a suíte definidos pelo projeto — normalmente `./mvnw test` ou `./gradlew test` — e informe com clareza qualquer limitação de ambiente.

## Arquitetura e modelagem

- Modele invariantes, entidades, value objects, regras e exceções de negócio no domínio. Use portas como interfaces de aplicação para persistência, mensageria e integrações; deixe os adaptadores implementarem essas portas.
- Mantenha transações na borda da aplicação, normalmente no caso de uso ou serviço de aplicação. Não abra transações em controladores nem faça o domínio depender de `@Transactional`.
- Separe DTOs de request/response das entidades de domínio e das entidades JPA. Converta nos adaptadores ou mapeadores explícitos; não exponha entidades JPA pela API.
- Aplique Bean Validation na entrada e devolva erros com o mecanismo global já adotado. Validações que definem invariantes de negócio continuam pertencendo ao domínio.
- Prefira construtores para dependências obrigatórias e classes com responsabilidade coesa. Evite estado mutável compartilhado, campos estáticos usados como serviço e injeção por campo.
- Use `record` para dados imutáveis sem identidade e `sealed` apenas quando o conjunto de variantes for realmente fechado. Prefira expressões `switch`, `Optional` como tipo de retorno e coleções imutáveis quando clarificarem o contrato; não use `Optional` em campos de entidade, parâmetros ou serialização.

## Spring Boot e Hibernate

- Mantenha controllers, listeners e schedulers finos: valide e traduza o protocolo, delegue ao caso de uso e converta o resultado para a saída.
- Use configurações tipadas com `@ConfigurationProperties`, perfis e variáveis de ambiente. Não codifique segredos, URLs ou parâmetros específicos de ambiente.
- Trate exceções em um ponto central, preservando erros de domínio e sem expor stack traces, detalhes de SQL ou dados sensíveis ao cliente.
- Faça entidades JPA refletirem o modelo de persistência, com construtor protegido quando necessário ao Hibernate e igualdade consistente com a estratégia de identidade do projeto. Evite `EAGER` por padrão e cascatas amplas sem uma regra de ciclo de vida explícita.
- Planeje carregamento de relações por caso de uso: use projeções, `join fetch`, `@EntityGraph` ou consultas específicas quando apropriado. Verifique N+1, paginação com coleções e serialização de proxies antes de concluir a alteração.
- Prefira paginação no banco, índices compatíveis com filtros/ordenação e operações em lote quando o volume justificar. Não use `findAll()` como atalho para operações potencialmente grandes.
- Para concorrência, declare a estratégia no caso de uso: versionamento otimista com `@Version` é preferível quando conflitos forem esperados; bloqueio pessimista requer justificativa e escopo transacional curto.

## Testes

- Teste domínio e casos de uso de forma unitária com JUnit 5, sem subir o contexto Spring. Use dublês das portas e cubra sucesso, violações de invariantes, ausência de dados e erros relevantes.
- Para adaptadores HTTP, persistência e integração, prefira testes de fatia ou integração que exercitem a configuração real necessária. Use Testcontainers quando o comportamento depender do banco ou serviço efetivamente usado em produção e a infraestrutura estiver disponível.
- Não esconda falhas de infraestrutura com mocks em testes cujo objetivo seja validar mapeamento, transação, consulta, migração ou serialização.
- Preserve dados de teste legíveis e independentes; não dependa de ordem de execução, relógio do sistema ou estado global sem controlar esses elementos explicitamente.

## Encerramento

Revise o diff para confirmar a direção das dependências, fronteiras transacionais, contratos de entrada e saída, carregamento eficiente de dados e cobertura dos caminhos de sucesso e erro. Relate os comandos executados e os que não puderam ser executados.
