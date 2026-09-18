---
name: code-review-php-laravel
description: Revisar diffs e branches de projetos backend PHP, especialmente APIs Laravel com Eloquent e Oracle. Use quando a usuária pedir code review de alterações locais, staged, branch atual ou MR em projetos PHP/Laravel, com foco em arquitetura, regras equivalentes ao Danger, testes, segurança, regressão e consistência de contrato.
---

# PHP e Laravel Code Review

Revisar apenas o diff solicitado e priorizar bugs, regressões, riscos e gaps de teste.

## Definir Escopo

1. Identificar o escopo da revisão.
   - Para review de branch, comparar a branch atual com a branch-base do repositório.
   - Preferir `git diff origin/develop...HEAD` quando o repositório usa `develop`.
   - Caso contrário, usar a base apropriada, como `origin/main...HEAD` ou `origin/master...HEAD`.
   - Para staged-only review, usar `git diff --cached`.
   - Para worktree review com alterações unstaged, usar `git diff HEAD`.
2. Ler os arquivos afetados e o contexto suficiente para entender comportamento e impacto.
3. Revisar corretude, regressão, riscos e cobertura de testes.
4. Verificar se regras de negócio novas ou alteradas são coerentes entre si, com o fluxo existente e com os invariantes esperados do domínio.
5. Responder em Português do Brasil, salvo pedido explícito em outro idioma.

## Preparar Runtime e Validar

Antes de executar testes ou qualquer script do repositório:

1. Identificar as versões exigidas em `composer.json`, `.php-version`, `.tool-versions`, Dockerfile ou configuração equivalente.
2. Comparar a restrição de `composer.json` com `php --version` e conferir extensões requeridas com `composer check-platform-reqs` quando as dependências estiverem instaladas.
3. Se houver gerenciador de versão configurado no projeto, como `phpenv`, `asdf` ou mise, ativar a versão exigida. Se o projeto define o runtime apenas em Docker, executar os comandos no serviço PHP apropriado.
4. Não alterar `composer.json`, `composer.lock`, plataforma simulada do Composer nem ignorar requisitos (`--ignore-platform-reqs`) apenas para fazer a validação passar.
5. Usar os scripts definidos em `composer.json` quando existirem. Executar ao menos a suíte unitária; executar também testes de integração/feature, Pint ou PHPCS e PHPStan/Larastan quando forem pertinentes ao diff.

Comandos usuais, escolhidos conforme o projeto:

- `composer test`, `php artisan test`, `vendor/bin/phpunit` ou `vendor/bin/pest`.
- `vendor/bin/pint --test`, `vendor/bin/phpcs` ou script equivalente de lint.
- `vendor/bin/phpstan analyse` ou `vendor/bin/psalm`.

Não executar correção automática durante um review somente leitura. Registrar no parecer os comandos executados, falhas encontradas e qualquer bloqueio externo que impeça uma validação.

## Aplicar Regras Equivalentes ao Danger

Quando o projeto possuir `Dangerfile`, regras próprias, PHPStan/Psalm, PHPCS, Pint ou verificações no pipeline, duplicar manualmente no diff as validações relevantes, mesmo que o CI possa executá-las. As regras locais do repositório prevalecem quando forem mais estritas.

Comentar toda violação encontrada nas linhas alteradas.

| Regra | Validação no diff | Exceções usuais |
|---|---|---|
| Arquivo grande | Arquivo novo ou modificado com mais de 150 linhas deve ser avaliado. Se o crescimento ocorreu por inflação sem refatoração, exigir divisão por responsabilidade. | Models de mapeamento extenso, repositories de integração, providers, migrations, seeders, factories, configurações, documentação gerada, testes e mocks quando a extensão for justificada |
| Função longa | Método, função ou closure com mais de 40 linhas deve ser comentado e deve haver sugestão concreta de extração. | Bootstrap, providers, migrations e adaptadores gerados quando a divisão pioraria a legibilidade |
| Tipo inseguro | Comentar `mixed` usado como fuga de tipagem, parâmetros ou retornos sem tipo quando puderem ser modelados, arrays sem shape em fronteiras importantes e supressões como `@phpstan-ignore-*` sem justificativa. | Fronteiras inevitavelmente dinâmicas devem usar validação e estreitamento antes do consumo; mocks podem ser menos estritos |
| Comentário explicativo | Em Application, Domain e Infrastructure, comentar explicações que compensam código confuso ou preservam código morto. Preferir nomes e extrações. | PHPDoc que define generics/array shapes, anotações exigidas por framework/ferramenta, comentários de segurança e justificativas de supressão |
| Teste por unidade nova | Classe nova em Application, Domain ou Infrastructure com comportamento deve ter teste significativo. | DTOs puros, enums, exceptions sem comportamento, interfaces/contratos e código gerado |

Não tratar arquivos de configuração da ferramenta como regras próprias sem ler o conteúdo real.

## Validar Arquitetura e Camadas

Aplicar a regra de ouro: zero lógica de negócio em `app/Http`. Controller deve ser uma fachada HTTP fina.

Reconhecer a estrutura real do repositório. Quando o projeto adotar arquitetura em camadas, validar o equivalente a:

| Camada | Paths comuns | Responsabilidade |
|---|---|---|
| HTTP | `app/Http/Controllers`, `Requests`, `Resources`, middleware | Transporte HTTP, autenticação/autorização, validação de entrada e serialização |
| Application | `app/Application`, `app/Actions`, `app/UseCases` | Orquestração de casos de uso e transações da aplicação |
| Domain | `app/Domain` | Regras, entidades, value objects, serviços e contratos do domínio |
| Infrastructure | `app/Infrastructure`, `app/Repositories`, integrações | Eloquent, banco, filas, cache e clientes externos |
| Async/Schedule | `app/Jobs`, `app/Listeners`, `app/Console` | Jobs, listeners, commands e agendamento |

Comentar as seguintes violações quando incompatíveis com a arquitetura do projeto:

- Controller contendo regra de negócio, query Eloquent complexa, transação ou orquestração extensa.
- Controller, job ou command instanciando dependência de aplicação com `new` em vez de usar injeção pelo Service Container.
- Domain importando `Illuminate\*`, facades, Eloquent Models, classes HTTP, Jobs ou Infrastructure. Aceitar dependência do framework somente se o projeto não separa domínio puro e a convenção existente a autoriza.
- Caso de uso fazendo IO direto de HTTP, Redis, fila, filesystem ou cliente externo em vez de delegar a um contrato/infrastructure quando o projeto usa separação em camadas.
- Infrastructure decidindo resultado de negócio, elegibilidade, estado permitido ou mensagem de domínio. Parsers puramente técnicos podem ficar na infraestrutura; normalização ou decisão orientada à regra deve ficar em Application/Domain.
- Repository que mistura persistência com regra, notificação, dispatch de job ou formatação de resposta HTTP.
- Facades globais escondendo dependências relevantes em Domain/Application quando injeção explícita é o padrão do projeto.
- Imports ou referências circulares entre módulos.

## Validar Service Container e Providers

Confirmar que contratos e implementações estão registrados no Service Container por provider, atributo ou mecanismo adotado no projeto.

Comentar quando houver:

- Interface nova sem binding para a implementação usada em runtime.
- Binding incorreto entre `singleton`, `scoped` e `bind`, especialmente quando o objeto carrega estado por request, conexão ou tenant.
- Dependência concreta usada onde o contrato é necessário para isolamento ou teste.
- Service locator via `app()`, `resolve()` ou facade dentro da regra de negócio sem justificativa.
- Uso de `new` que contorna injeção, configuração, decorator ou proxy do container.
- Provider com efeitos colaterais, query ao banco ou chamada externa durante `register()`/`boot()` sem necessidade.
- Closure de binding capturando configuração ou estado incorreto para workers persistentes, como Octane ou queue workers.

## Validar Naming e Contratos

- Classes, traits, enums e interfaces em PascalCase; métodos e propriedades em camelCase; constantes conforme a convenção do projeto.
- Arquivos PSR-4 devem corresponder à classe e ao namespace declarados.
- Interfaces devem ter padrão consistente (`FooRepository` ou `FooRepositoryInterface`); não impor sufixo diferente do repositório.
- Enums devem representar conjunto fechado real e usar backing type compatível com banco e contrato externo.
- Actions/use cases devem ter nome de uma responsabilidade; evitar nomes como `ValidateAndSave` quando há duas operações separáveis.
- Form Requests, Resources, DTOs, Jobs, Events, Listeners, Policies e Commands devem indicar a função real implementada.
- Verificar se renomeações preservam rotas, container bindings, serialização, consumers e contratos públicos.
- Tabelas Oracle usam o prefixo `EGRU_` quando essa for a convenção do projeto.
- Colunas Oracle devem seguir UPPERCASE com underscore quando essa for a convenção do schema.

## Validar Models Eloquent e Persistência

- Confirmar `$table`, `$primaryKey`, `$keyType`, `$incrementing`, timestamps e conexão quando diferirem das convenções do Laravel.
- Exigir `SoftDeletes` e coluna compatível quando o domínio usa exclusão lógica; comentar `delete` físico ou query builder que contorne esse comportamento sem justificativa.
- Conferir `$casts` para datas, booleanos, decimais, JSON, enums e objetos de valor. Para valores monetários, apontar conversão por `float` quando precisão decimal for requisito.
- Avaliar `$fillable`/`$guarded`; comentar mass assignment de payload bruto ou proteção ampla demais.
- Não aceitar UUID/ULID manual quando o projeto possui trait, observer ou geração centralizada. Confirmar formato e ordenação exigidos.
- Conferir cardinalidade, chaves local/estrangeira, tabela pivô, timestamps e campos extras em relacionamentos.
- Comentar acesso a relação em loop sem eager loading quando produzir N+1.
- Comentar accessor, mutator, cast ou observer que faça IO, dispare efeitos colaterais ocultos ou contenha regra extensa.
- Comentar model event/observer que possa recursar por `save()` ou gerar efeitos duplicados em retry.
- Conferir transações em operações com múltiplas gravações dependentes.
- Comentar `DB::transaction()` envolvendo HTTP, fila ou operação lenta externa, pois prolonga locks e combina atomicidades diferentes.
- Vetar alteração de schema sem migration e migration destrutiva sem estratégia de compatibilidade/rollback.
- Confirmar que migrations não dependem de Models de aplicação sujeitos a mudar.

### Oracle

- Validar nomes físicos, sequence/trigger, chave primária não incremental, tipos `NUMBER`, `VARCHAR2`, `CLOB`, datas/timestamps e nulabilidade contra o DDL real.
- Considerar limite de 1000 expressões em listas `IN` do Oracle e dividir lotes quando necessário.
- Não presumir suporte idêntico ao MySQL/PostgreSQL para `returning`, JSON, índices, alteração de coluna, upsert e locks.
- Comentar comparação de string vazia distinta de `NULL`, pois Oracle trata string vazia como `NULL`.

## Validar Requests, Resources e Contrato HTTP

- Usar Form Request ou mecanismo central equivalente para validação não trivial; controller não deve repetir validação manual dispersa.
- Confirmar `authorize()` e Policies/Gates/middleware nas rotas protegidas. `authorize(): true` sem outra autorização deve ser questionado quando o recurso é sensível.
- Regras `sometimes`, `nullable`, `present`, `filled`, `required_if` e exclusões condicionais devem corresponder à semântica de create/update/patch.
- Comentar uso direto de `$request->all()` e mass assignment; exigir somente dados validados/autorizados.
- Validar route model binding, inclusive escopo por pai/tenant e comportamento para soft-deleted.
- API Resources devem evitar queries, regras e carregamento preguiçoso invisível. Usar `whenLoaded` quando a relação for opcional.
- Preservar status HTTP, envelope, paginação, nomes de campos, tipos, nulabilidade e formato de erro do contrato existente.
- Comentar retorno acidental de Model/Exception/stack trace com campos internos ou sensíveis.
- Para parâmetros numéricos ou listas em query string, comentar `explode` + cast sem validação, valores vazios, `0` involuntário e entradas inválidas.

## Validar Exceções, Auth e Observabilidade

- Vetar `throw new \Exception('...')` ou `RuntimeException` genérica em regra de negócio quando houver exception de domínio apropriada.
- Apontar `catch (Throwable $e)` quando `$e` não é usado; nessa situação, exigir `catch (Throwable)` se a versão PHP permitir, ou remover o catch quando não houver tratamento.
- Comentar catch amplo que engole falha, retorna `null`/`false` ambiguamente ou continua o fluxo após apenas registrar log.
- Ao traduzir exception, preservar a causa com `previous: $e` quando o contrato permitir e não expor detalhes internos ao cliente.
- Avaliar acesso a resultado possivelmente `null`, como `first()`, `find()`, `sole()` alternativo, relação opcional ou índice ausente. Quando o fluxo não puder continuar, exigir guarda explícita e exception adequada; nullsafe `?->` que apenas propaga `null` pode esconder bug.
- Verificar coerência e padronização das mensagens de erro; apontar mensagens genéricas, contraditórias ou desalinhadas do contrato.
- Exigir usuário autenticado pelos mecanismos do Laravel, sem confiar em `user_id`, tenant ou papel enviados pelo cliente.
- Validar autenticação e autorização separadamente. Estar autenticado não concede acesso ao recurso.
- Evitar transportar `executionId`, correlation ID ou tenant por toda assinatura de domínio quando o projeto possui contexto por request/middleware; garantir propagação explícita em jobs.
- Vetar `dump`, `dd`, `var_dump`, `print_r` e logs de debug em produção.
- Preferir `Log`/logger injetado, contexto estruturado e canal padronizado a escrita direta em arquivo ou stdout.
- Exigir operação, identificador técnico não sensível, código/categoria e causa segura nos eventos de observabilidade.
- Comentar logs de senha, token, cookie, Authorization, CPF/CNPJ completos, payload sensível ou dados pessoais desnecessários.

## Validar Filas, Eventos, Cache e Schedule

- Jobs enfileirados devem implementar `ShouldQueue` e definir connection/queue, timeout, tries, backoff e tratamento de falha conforme criticidade.
- Verificar idempotência diante de retry, timeout, redelivery e execução concorrente.
- Comentar job cujo construtor serializa Model grande, relação carregada ou estado mutável; preferir IDs e recarregar o estado necessário.
- Avaliar `afterCommit` quando o job/evento depende de dados gravados na transação atual.
- Garantir unicidade/lock quando execuções simultâneas causariam duplicidade; conferir TTL e liberação do lock.
- Comentar `dispatchSync` ou processamento pesado no request quando contradiz o desenho assíncrono.
- Listeners e subscribers não devem esconder regra crítica sem teste nem depender de ordem não garantida.
- Chaves de cache devem incluir tenant, usuário, versão e parâmetros relevantes. Validar TTL, invalidação e comportamento de cache miss/stale.
- Evitar `Cache::remember` com closure que produz efeito colateral ou mantém lock por IO excessivo.
- Commands agendados devem tratar overlap, múltiplas instâncias, timezone e execução em apenas um servidor quando aplicável.
- Workers persistentes não podem reter estado de request/tenant entre jobs.

## Validar Paginação, Queries e Performance

- Usar paginação consistente (`paginate`, `simplePaginate` ou cursor pagination) e preservar os metadados do contrato.
- Comentar `get()` sem limite em endpoint ou job que pode crescer indefinidamente.
- Ao compor query incremental, não sobrescrever filtros anteriores nem introduzir `orWhere` sem agrupamento lógico.
- Conferir precedência de `where`/`orWhere`, filtros de tenant, soft delete, joins e escopo de autorização.
- Comentar query em loop quando houver eager loading, preload, join, agregação, `whereIn`, chunking ou processamento em lote.
- Comentar HTTP, cache ou filesystem em loop quando batch, paralelização controlada ou reorganização for possível.
- Usar `chunkById`/`lazyById` quando registros podem mudar durante a iteração; questionar `chunk` por offset em conjuntos mutáveis.
- Não usar `cursor()` sem considerar duração da conexão, memória do driver e acesso a relações.
- Comentar `count()` seguido de `get()`/`exists()` redundante ou consultas repetidas com o mesmo resultado.
- Validar índices para filtros/joins novos quando o impacto for material e houver evidência suficiente; não afirmar ausência de índice sem inspecionar migrations/schema.
- Comentar seleção de todas as colunas e relações quando o fluxo precisa de subconjunto pequeno em caminho quente.

## Validar Segurança

- Apontar SQL Injection em `DB::raw`, `whereRaw`, `orderByRaw` e expressões construídas com entrada. Exigir bindings e allowlist para identificadores/direção de ordenação.
- Validar autorização contra IDOR/BOLA em recursos buscados por ID, inclusive escopo por tenant, unidade ou proprietário.
- Verificar upload: MIME real, extensão, tamanho, nome gerado, armazenamento não executável, visibilidade e autorização de download.
- Vetar path traversal, command injection, unserialize inseguro e template/renderização com conteúdo não confiável.
- Exigir secrets e credenciais em configuração/env; não aceitar valor sensível hardcoded ou fallback inseguro.
- Não expor stack trace, SQL, filesystem path, credenciais ou configuração no response.
- Avaliar SSRF em URLs fornecidas pelo cliente: esquema, host, redirects e redes privadas devem ser controlados.
- Validar assinatura e replay protection de webhooks; não confiar apenas em IP quando assinatura está disponível.
- Conferir rate limiting em endpoints de autenticação, consulta custosa, geração de arquivo e integrações sujeitas a abuso.
- Comentar desativação de CSRF, autenticação, TLS verification ou validação de certificado sem justificativa estrita.
- Validar escaping e política de conteúdo quando backend produz HTML, e-mail ou arquivos consumidos por planilhas.

## Validar Anti-Patterns

Comentar quando encontrar:

- Valores hardcoded de negócio ou infraestrutura em produção; usar configuração, enum/value object ou parâmetro conforme o contexto.
- Leitura direta de `env()` fora de arquivos de configuração; isso quebra `config:cache` e dificulta testes.
- Service/action/use case com mais de uma responsabilidade clara.
- Controller fazendo três ou mais operações de aplicação sem um caso de uso explícito quando isso representa um único fluxo.
- Domain entity ou value object fazendo IO.
- Helpers globais novos para lógica de negócio quando uma dependência explícita seria mais clara e testável.
- Static methods ou facades usados para esconder estado e impedir isolamento de teste.
- Muitos níveis de `if`, `foreach` e `try`; preferir guard clauses, extração ou tabela de decisão.
- Operador `@` para suprimir erro, comparação frouxa (`==`) em IDs/estados críticos ou truthiness ambígua.
- `empty()` quando `0`, `'0'`, `false`, `null` e array vazio possuem significados diferentes.
- Datas com timezone implícito, mutabilidade inesperada de Carbon ou comparação entre timezone distintos.
- `now()`/`Carbon::now()` espalhado em regra difícil de testar quando Clock ou instante injetado é necessário.
- Eventos, observers ou traits que escondem gravações e efeitos colaterais não evidentes.
- Dependência nova ou atualização no `composer.lock` sem mudança intencional correspondente em `composer.json`, ou atualização ampla não relacionada ao diff.

## Validar Regressões Conhecidas

Quando o diff tocar fluxos parecidos, procurar explicitamente:

- Remoção de itens da mesma Collection/array durante iteração que possa pular elementos ou desalinhar índices. Exigir `filter`, nova coleção ou iteração segura.
- Saves parciais que zeram, removem ou sobrescrevem composições ausentes do payload. Em PATCH/update parcial, não alterar registros não enviados sem regra explícita.
- Regras de conclusão ou permissão de salvamento que aceitam resultado consolidado vazio.
- Parse manual de lista numérica com `explode` + `intval`/cast que converte inválidos ou vazios para `0`.
- `updateOrCreate`/`firstOrCreate` com atributos de busca insuficientes, gerando colisão entre tenant, edição ou proprietário.
- `first()` usado onde duplicidade deveria ser erro; considerar `sole()` ou constraint única quando a unicidade é invariante.
- `save()` em model parcialmente preenchido ou `update($validated)` que apaga valores por normalização incorreta.
- Evento/job disparado antes do commit e executado sem conseguir ler os dados persistidos.
- Retry de job duplicando cobrança, envio, manifestação, notificação ou gravação externa.
- Cache sem chave de tenant/usuário ou invalidação após escrita.
- Resource acessando relação não carregada e introduzindo N+1.

## Validar Boas Práticas Gerais

Aplicar estas regras ao código novo presente no diff:

| # | Regra | Como aplicar |
|---|---|---|
| 1 | Sem recursão desnecessária; máximo de 3 níveis de aninhamento; preferir guard clauses | Apontar blocos novos com nesting excessivo |
| 2 | Loops com limite verificável; `while` exige condição de saída e proteção contra loop infinito | Apontar loop sem limite claro |
| 3 | Não recriar arrays, Collections ou objetos acumuladores indevidamente dentro de loop | Apontar inicialização ou transformação redundante |
| 4 | Função com responsabilidade única; nome não deve sugerir duas ações independentes | Apontar nomes como `validateAndSave` |
| 5 | Validar precondições de métodos públicos e invariantes/resultado quando aplicável | Apontar entrada aceita sem validação relevante |
| 6 | Variável no menor escopo possível; não reutilizar para significados diferentes; preferir imutabilidade quando prática | Apontar reatribuição que dificulta raciocínio |
| 7 | Parâmetros e retornos tipados; não ignorar retorno ou falha de operação relevante | Apontar chamadas cujo resultado é descartado indevidamente |
| 8 | Sem `mixed` como contorno; arrays complexos devem usar DTO, value object, Collection tipada ou array shape | Apontar ausência de contrato e supressão da análise estática |
| 9 | Erros devem ser propagados ou convertidos intencionalmente; nunca catch vazio ou apenas log | Apontar swallow de exception e exception genérica |
| 10 | Complexidade cognitiva controlada; evitar literal repetido, código morto e excesso de parâmetros | A partir de 5 parâmetros, avaliar DTO/objeto de entrada; comentar 8 ou mais salvo exigência do framework |
| 11 | Dados sensíveis protegidos; input validado; auth e autorização explícitas; sem debug em produção | Apontar credenciais, exposição e proteção ausente |
| 12 | Não introduzir custo evitável em caminho quente | Sugerir batching, eager loading, cache, agregação ou reorganização com base no caso real |

Não transformar preferências estilísticas em finding se Pint/PHPCS já cobrem o ponto e não houver efeito em corretude ou manutenção.

## Validar Testes

- Verificar cobertura adequada de unidade, feature e integração conforme a camada alterada.
- Usar o framework adotado pelo projeto (PHPUnit ou Pest) e respeitar a organização existente.
- Apontar asserts ausentes, testes que só verificam status genérico, edge cases não cobertos e expectativas desatualizadas.
- Para regras de negócio, exigir casos válido, inválido e fronteiras relevantes.
- Para endpoint, validar autorização, validação, status, shape do JSON e efeitos persistidos.
- Para banco, evitar teste que passa por SQLite quando o comportamento depende de Oracle/MySQL/PostgreSQL; registrar risco quando o banco real não puder ser usado.
- Conferir factories e fixtures: estados devem representar o cenário e não depender de dados globais ou ordem de execução.
- Comentar mocks excessivos que apenas reproduzem a implementação e não testam resultado observável.
- Em jobs/listeners, testar idempotência, retry/falha e `afterCommit` quando aplicável.
- Se teste falhar, distinguir regressão real, ambiente incompleto e teste desatualizado.
- Incluir no resultado o efeito da execução real dos testes; análise estática não substitui essa validação.

## Formatar a Resposta

Responder em formato review-first:

1. Listar findings primeiro, em ordem de severidade, com arquivo e linha do diff quando possível.
2. Para cada finding, explicar o cenário concreto de falha, impacto e correção esperada. Evitar comentários vagos.
3. Listar perguntas em aberto ou premissas em seguida.
4. Informar comandos de validação executados e respectivos resultados.
5. Encerrar com resumo breve apenas se adicionar valor.

Classificar severidade de modo consistente:

- **Crítico:** vulnerabilidade explorável, perda/corrupção de dados, indisponibilidade ampla ou quebra certa de produção.
- **Alto:** bug funcional provável, autorização incorreta, contrato quebrado ou regressão importante.
- **Médio:** falha em cenário relevante, risco de concorrência/performance ou gap de teste que oculta comportamento importante.
- **Baixo:** manutenção ou robustez com impacto concreto, sem elevar estilo puro a defeito.

Se nenhum problema for encontrado, dizer isso explicitamente e registrar risco residual ou gap de teste.

## Comandos Úteis

- `git status --short`
- `git diff --cached`
- `git diff HEAD`
- `git diff origin/develop...HEAD`
- `git diff origin/main...HEAD`
- `git log --oneline --decorate -5`
- `composer validate --strict`
- `composer audit`
- `php artisan test`
- `vendor/bin/pest`
- `vendor/bin/phpunit`
- `vendor/bin/pint --test`
- `vendor/bin/phpstan analyse`

Antes de qualquer commit solicitado explicitamente, executar o formatador/lint com correção automática definido pelo projeto, como `vendor/bin/pint` ou `vendor/bin/phpcbf`, revisar as alterações produzidas e só então fazer stage. Não modificar arquivos durante um review somente leitura.

## Foco Final

Revisar o diff, não o repositório inteiro.

- Comentar apenas problemas introduzidos ou materialmente agravados pelas linhas do diff.
- Se mencionar identificadores não alterados, deixar claro que são apenas contexto.
- Duplicar validações automatizadas do projeto como defesa em profundidade.
- Adicionar violações semânticas que regex, Pint, PHPStan, Psalm, PHPCS ou pipeline não detectam.
- Não afirmar bug com base apenas em preferência. Demonstrar o caminho de execução, entrada ou invariante violado.
