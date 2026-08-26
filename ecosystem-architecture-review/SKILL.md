---
name: ecosystem-architecture-review
description: Analisa ecossistemas de software completos formados por multiplos projetos (frontend/app/web, middleware, APIs, backend, componentes Uniface, Oracle e servicos externos), reconstruindo a arquitetura AS-IS com evidencia antes de propor evolucao. Use para revisao arquitetural 360 graus, C4, arquitetura funcional, genealogia ponta a ponta, catalogo de integracoes, Uniface e dados, Design System, runtime, seguranca, observabilidade, testes, riscos, ADRs, TO-BE, gap analysis e roadmap.
---

# Ecosystem Architecture Review

Executar uma avaliacao arquitetural 360 graus orientada por evidencias. Tratar a pasta recebida como um unico ecossistema, mesmo quando contiver varios repositorios independentes.

## Principios obrigatorios

1. Reconstruir o AS-IS antes de julgar ou recomendar.
2. Nao inferir responsabilidade pelo nome da pasta, projeto ou componente; comprovar no codigo/configuracao/documentacao.
3. Nunca apresentar conclusao arquitetural relevante sem evidencia rastreavel.
4. Classificar achados como `CONFIRMADO`, `INFERIDO`, `HIPOTESE`, `RISCO` ou `RECOMENDACAO`.
5. Informar confianca (`alta/media/baixa` ou percentual quando justificavel) e fontes para achados importantes.
6. Distinguir claramente fato, inferencia e proposta.
7. Nao considerar ausencia de referencia como prova de codigo morto; usar `candidato a zombie` ate validacao externa.
8. Nao produzir TO-BE antes de o Architecture Review Board contestar o AS-IS.
9. O Chief Architect pode consolidar, mas nao criar descobertas novas.
10. Priorizar verdade arquitetural sobre documentacao visualmente elegante.

## Entrada

Aceitar uma pasta raiz com no minimo tres projetos e opcionalmente mais repositorios, documentacao, DDL e componentes Uniface. Exemplos comuns: frontend/app/web, middleware, APIs/backend, workers/servicos, pasta Uniface e artefatos de banco.

Inventariar tudo antes de selecionar ferramentas. Ignorar dependencias geradas e binarios (`node_modules`, `dist`, `build`, caches, vendor) salvo necessidade especifica.

## Fluxo de execucao

### Fase 0 - Intake e Evidence Index
Executar `scripts/scan_ecosystem.py <pasta-raiz> --output <arquivo.json>` quando houver acesso ao filesystem. Criar inventario de projetos, tecnologias, manifests, entry points, configuracoes, interfaces, banco, Uniface, Design System, testes, runtime e documentacao.

### Fase 1 - Discovery factual
Atuar como **Evidence & Repository Mapper** e **Code Archaeologist**. Rastrear imports, chamadas, rotas, endpoints, services, DTOs, Operations Uniface, Entities, tabelas, configuracoes e dependencias. Nao recomendar nesta fase.

### Fase 2 - Reconstrucao arquitetural
Atuar sequencialmente como:
1. **Solution Architect** - C4, boundaries, responsabilidades e dependencias.
2. **Integration Architect** - contratos, APIs, protocolos, autenticacao e sistemas externos.
3. **Uniface/Legacy Specialist** - Components, Operations, Entries, Entities, triggers, includes, services, regras e acesso Oracle.
4. **Data Architect** - modelo conceitual/logico, PK/FK, leitura/escrita, ownership e lineage.
5. **Experience Architect** - Design System, tokens, cores, tipografia, componentes, patterns, duplicacoes e acessibilidade.

Consultar `references/analysis-dimensions.md` para cobertura obrigatoria e `references/uniface-oracle.md` para Uniface/Oracle.

### Fase 3 - Knowledge Graph e genealogia
Construir relacoes verificadas no formato:
`Capability -> Processo -> Funcionalidade -> Tela -> Service/Hook -> Endpoint -> Middleware -> Uniface Operation -> Entity -> Tabela/Coluna`.
Construir tambem a genealogia bottom-up. Derivar blast radius, change coupling e ownership. Consultar `references/evidence-genealogy.md`.

### Fase 4 - Diagnostico
Atuar como **Security/Performance/Observability Reviewer** e **Product/Functional Analyst**. Avaliar boundary violations, hotspots, zombie candidates, dependency health, API governance, seguranca, observabilidade, testes, runtime, deployment, Design System e riscos de dados.

### Fase 5 - Review Board
Atuar como **Architecture Review Board**. Contestar afirmacoes, procurar contradicoes entre agentes, exigir evidencia e rebaixar conclusoes nao comprovadas. Registrar contradicoes e perguntas abertas.

### Fase 6 - Modernizacao
Somente apos o AS-IS revisado, atuar como **Modernization Architect**. Definir drivers, alternativas, ADRs propostos, Target Architecture/TO-BE, gaps e roadmap.

### Fase 7 - Sintese
Atuar como **Chief Architect**. Consolidar apenas conclusoes sobreviventes ao Review Board. Gerar o Architecture Atlas conforme `references/output-contract.md`.

## Banco Oracle

Quando o codigo nao for suficiente para comprovar o modelo fisico, fornecer ao usuario os scripts em `assets/oracle-discovery/` para execucao em ambiente autorizado. Nao afirmar que os resultados foram observados antes de receber a saida. Apos receber os resultados, realizar segunda passagem de Data Architecture.

## Diagramas

Usar Mermaid como formato padrao dos arquivos `.mmd`. Gerar C4 conceitual, componentes, integracoes, dados, genealogia, deployment e sequencias. Se uma skill UML/PlantUML estiver disponivel e trouxer melhor representacao, pode compor com ela, preservando Mermaid como entrega obrigatoria.

## ADR

Separar:
- `ADR-D-*`: decisoes descobertas no AS-IS, com evidencia.
- `ADR-P-*`: decisoes propostas para o TO-BE.

Usar `references/adr-template.md`.

## Fitness e saude

Pontuar apenas dimensoes sustentadas por evidencia. Para cada nota registrar justificativa, fontes, confianca e principal risco. Nunca inventar cobertura, SLA, volume, owner, ambiente ou infraestrutura.

## Saida obrigatoria

Gerar o pacote descrito em `references/output-contract.md`, incluindo Executive Summary, Architecture Health, inventario, Technology Radar, capability/process/functional maps, C4, AS-IS, responsabilidades, integracoes, Uniface, dados, Experience/Design System, runtime, seguranca, observabilidade, testes, genealogia, blast radius, hotspots, riscos, ADRs, TO-BE, gaps, roadmap, contradicoes, perguntas abertas e Mermaid pack.

## Criterio de conclusao

Nao declarar revisao completa se houver repositorios relevantes nao lidos, resultados Oracle pendentes indispensaveis, integracoes externas sem evidencia suficiente ou perguntas abertas criticas. Explicitar cobertura analisada e lacunas.
