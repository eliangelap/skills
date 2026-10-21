# Contrato de saida - Ecosystem Architecture Atlas

Gerar, quando aplicavel:

```text
architecture-review/
├── 00-executive/
│   ├── EXECUTIVE-SUMMARY.md
│   └── ARCHITECTURE-HEALTH.md
├── 01-inventory/
│   ├── ECOSYSTEM-INVENTORY.md
│   ├── TECHNOLOGY-RADAR.md
│   └── EVIDENCE-INDEX.md
├── 02-business/
│   ├── CAPABILITY-MAP.md
│   ├── PROCESS-MODEL.md
│   └── FUNCTIONAL-ARCHITECTURE.md
├── 03-architecture/
│   ├── AS-IS.md
│   ├── C4.md
│   ├── COMPONENT-RESPONSIBILITIES.md
│   └── DEPENDENCIES.md
├── 04-integrations/
│   ├── INTEGRATION-CATALOG.md
│   ├── API-CATALOG.md
│   └── CONTRACT-ASSESSMENT.md
├── 05-uniface/
│   ├── COMPONENT-CATALOG.md
│   ├── OPERATIONS.md
│   ├── ENTITIES.md
│   └── LEGACY-ASSESSMENT.md
├── 06-data/
│   ├── DATA-ARCHITECTURE.md
│   ├── CONCEPTUAL-MODEL.md
│   ├── LOGICAL-MODEL.md
│   └── DATA-LINEAGE.md
├── 07-experience/
│   ├── DESIGN-SYSTEM-AS-IS.md
│   ├── DESIGN-TOKENS.md
│   ├── COMPONENT-INVENTORY.md
│   └── UX-CONSISTENCY.md
├── 08-runtime/
│   ├── DEPLOYMENT.md
│   ├── SECURITY.md
│   └── OBSERVABILITY.md
├── 09-quality/
│   ├── TEST-ARCHITECTURE.md
│   ├── ARCHITECTURE-FITNESS.md
│   ├── HOTSPOTS.md
│   ├── ZOMBIE-COMPONENTS.md
│   ├── BOUNDARY-VIOLATIONS.md
│   └── RISKS-TECHNICAL-DEBT.md
├── 10-genealogy/
│   ├── FUNCTIONAL-GENEALOGY.md
│   ├── DATA-GENEALOGY.md
│   ├── BLAST-RADIUS.md
│   └── CHANGE-COUPLING.md
├── 11-adr/
│   ├── discovered/
│   └── proposed/
├── 12-evolution/
│   ├── TO-BE.md
│   ├── GAP-ANALYSIS.md
│   └── EVOLUTION-ROADMAP.md
├── 13-validation/
│   ├── CONTRADICTIONS.md
│   ├── OPEN-QUESTIONS.md
│   └── REVIEW-BOARD.md
└── diagrams/
    ├── ecosystem-context.mmd
    ├── c4-context.mmd
    ├── c4-container.mmd
    ├── c4-components.mmd
    ├── functional-architecture.mmd
    ├── integration-map.mmd
    ├── data-model.mmd
    ├── genealogy.mmd
    ├── deployment-as-is.mmd
    ├── deployment-to-be.mmd
    └── sequence-*.mmd
```

## Executive Summary
Responder: o que e o ecossistema, principais responsabilidades, tecnologias, fluxo central, saude, maiores riscos, principal ponto de evolucao e recomendacoes prioritarias.

## Architecture Health
Avaliar manutenibilidade, escalabilidade, seguranca, observabilidade, testabilidade, resiliencia, evolutividade, coupling, data, API governance, UX consistency e deployment. Toda nota precisa de evidencia.

## Roadmap
Ordenar por Quick Wins, curto prazo, medio prazo e transformacoes estruturais. Para cada iniciativa: problema, evidencia, impacto, esforco relativo, risco, dependencias, ADR relacionado e resultado esperado.
