# Dimensoes obrigatorias de analise

## Business e funcional
- Dominios, capabilities, processos, funcionalidades e casos de uso.
- Rastreabilidade entre comportamento de negocio e implementacao.
- Responsabilidade funcional por componente.

## Aplicacao e C4
- Context, Containers e Components.
- Boundaries, dependencias, fan-in/fan-out e acoplamento.
- Responsabilidades atuais e vazamentos de responsabilidade.

## Integracoes
- Endpoints, consumers, producers, DTOs, contratos, protocolos, autenticacao, timeout, retry, idempotencia, versionamento e erros.
- APIs internas/externas, orfas, duplicadas ou sem consumidor identificado.

## Experience Architecture / Design System
- Tokens: cores, tipografia, spacing, radius, elevation, breakpoints e themes.
- Componentes compartilhados/locais/duplicados/deprecated e bibliotecas externas.
- Patterns de forms, search, filters, navigation, feedback, loading e erros.
- Responsividade e evidencias de acessibilidade.
- Mapear Design Component -> Tela -> Funcionalidade.

## Dados
- Modelo conceitual e logico; entidades, tabelas, views, PK/FK, indices, triggers e constraints.
- Read/write, data ownership, master/transacional/configuracao/auditoria/documental/geoespacial/temporario.
- Data lineage e possiveis acessos diretos indevidos.

## Runtime e deployment
- Ambientes evidenciados, servidores/containers, proxies, ports, jobs, schedulers, workers, storage e servicos externos.
- Nunca inventar topologia nao encontrada.

## Identity e Security
- OAuth/OIDC/JWT/Keycloak/AD quando evidenciados; roles, permissoes, service accounts, secrets e autorizacao por camada.
- Trust boundaries e exposicoes.

## Observabilidade
- Logs, metrics, traces, alerts, dashboards e correlation IDs.
- Avaliar se uma requisicao pode ser seguida ponta a ponta.

## Test Architecture
- Unit, integration, contract, E2E, mocks, ferramentas e cobertura somente se comprovada.
- Cruzar criticidade x evidencia de testes.

## Technology Landscape
- Linguagens, frameworks, bibliotecas, bancos, protocolos e versoes.
- Radar: ADOPT/TRIAL/ASSESS/HOLD somente com racional explicito.
- Dependencias desatualizadas/EOL/vulneraveis exigem fonte ou ferramenta confiavel; nao adivinhar.

## Diagnostics
- Boundary violations.
- Hotspots por centralidade, dependencias, tamanho/complexidade observavel e responsabilidades.
- Zombie candidates.
- Change coupling e blast radius.
- Single points of failure apenas quando sustentados pela topologia.
- Technical debt e architecture debt.
