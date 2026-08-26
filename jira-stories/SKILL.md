---
name: jira-stories
description: Create complete, testable, traceable Jira epics and user stories in Eliangela's standard. Use when asked to draft, refine, or structure an epic or Functional, Enabler, Exploratory, Kaizen, Bug, Task, or Technical Debt story.
---

# Épicos e histórias Jira

Create Jira-ready epics and stories in Brazilian Portuguese, following the Eliangela standard. Write clearly, objectively, and without unnecessary technical jargon. Keep each complete item between 300 and 600 words unless the user explicitly asks for a different length.

## Identify the work item and gather inputs

First identify whether the request is for an **Épico** or a **História**. When the user asks for both, write the epic first and then each requested story, linking them only when that relationship was supplied or directly established by the request.

For a story, extract the type, product or project, persona, current context, desired action, expected benefit, and affected area from the request and conversation. For an epic, extract the product or initiative, business problem or opportunity, intended outcome, scope, affected audiences, expected value, and known related work.

When material information is missing, either ask a concise follow-up question or state a reasonable assumption before the story. Never invent Jira keys, linked items, interfaces, integrations, dates, teams, or product names.

Use only these types:

| Type | Purpose |
|---|---|
| Funcional | Deliver new value to the end user. |
| Habilitadora | Provide technical support for future functionality. |
| Exploratória | Reduce a technical or business uncertainty. |
| Kaizen | Improve the team or process continuously. |
| Bug | Correct a failure or unexpected behavior. |
| Tarefa | Complete a specific technical or organizational activity. |
| Débito Técnico | Refactor, update, or clean up legacy code. |

If no type is given, infer the most suitable one from the objective and state that choice. Use `[Tipo]` with the selected type in the title.

## Write an epic

Use this structure when the requested item is an epic. An epic should describe a coherent business outcome that can be broken into multiple stories; it is not a large story with implementation steps.

```markdown
## Título
[Épico] <resultado ou objetivo estratégico>

## Objetivo do Épico
<resultado de negócio ou capacidade que será alcançada>

## Contexto
<cenário atual, problema, oportunidade ou motivação>

## Objetivo e Valor
<valor para o negócio, usuário ou operação>

## Escopo
### Inclui
- <capacidade, jornada ou resultado dentro do épico>

### Não inclui
- <limite conhecido do épico>

## Histórias relacionadas
- <histórias fornecidas ou frentes a detalhar, sem inventar chaves Jira>

## Critérios de Sucesso
- [ ] <resultado mensurável, observável ou validável do épico>

## Relacionamentos
<referências fornecidas a outros épicos, histórias, bugs ou iniciativas>

## Interfaces Impactadas
<sistemas, módulos, apps ou integrações informados ou diretamente implicados>

## Labels sugeridas para Jira
`epico`, `<produto>`, `<área>`

## Dica de ouro
<recomendação estratégica para fatiar e acompanhar o épico>
```

Omit the optional **Relacionamentos**, **Interfaces Impactadas**, and **Não inclui** sections when the request does not support them. If stories have not been identified, describe them as areas to detail rather than fabricating titles, keys, or estimates. Include success criteria that demonstrate outcome or adoption, not merely that all tickets were closed. End with a tip that recommends thin, independently valuable stories and an explicit outcome metric.

## Write a story

Use every section below, in this order. Preserve the headings and omit only the two sections marked optional when no supported information exists.

```markdown
## Título
[Tipo] <resumo objetivo da história>

## História
Como <persona>, quero <ação desejada>, para <objetivo ou benefício>.

## Contexto
<cenário atual, dor ou motivação>

## Objetivo e Valor
<valor entregue ou problema resolvido>

## Critérios de Aceite
- [ ] <condição objetiva, observável e testável>
- [ ] <condição objetiva, observável e testável>

## Relacionamentos
<referências fornecidas a histórias, bugs, tarefas ou épicos>

## Interfaces Impactadas
<sistemas, módulos, apps ou integrações informados ou diretamente implicados>

## Labels sugeridas para Jira
`<tipo>`, `<produto>`, `<área>`

## Tempo ou esforço esperado (referência)
<faixa adequada ao tipo>

## Dica de ouro
<recomendação estratégica ou técnica específica do tipo>
```

Write a concise title beginning with the type, for example: `[Funcional] Permitir envio de relatório PDF no app AGROVET`.

For **Bug**, adapt the História sentence if necessary to make the failure, correction, and expected behavior unambiguous. For **Exploratória**, express the action as investigation and the benefit as a decision, recommendation, proof of concept, or uncertainty reduction. For **Habilitadora**, **Tarefa**, and **Débito Técnico**, use the standard sentence when it remains natural; otherwise prioritize a clear outcome over a forced persona.

## Make criteria testable

Write acceptance criteria as observable outcomes, not implementation activities. Cover happy path, permissions or validations when provided, error behavior when relevant, and persistence/integration outcomes only when they are in scope.

Avoid vague terms such as “adequadamente”, “rapidamente”, “intuitivo”, “deve funcionar”, and “conforme necessário”. Replace them with the actor, condition, action, and expected result. Do not prescribe APIs, libraries, schemas, or implementation tasks unless the request makes them a requirement.

## Add labels, effort, and a type-specific tip

Suggest labels from information actually available, using lowercase kebab-case. Include a type label, then product and area labels when known. Do not invent labels to fill the list.

Use these reference ranges; present them as a planning reference, not a commitment:

| Type | Expected effort |
|---|---|
| Funcional | 1–5 days |
| Habilitadora | Assess from the stated enablement scope; do not invent a fixed range |
| Exploratória | Up to 1 sprint |
| Kaizen | Up to 2 days |
| Bug crítico | Immediately or by the end of the sprint |
| Bug não crítico | State a reasonable scope-based reference |
| Tarefa | Up to 2 days |
| Débito Técnico | 1–3 days |

End with one practical **Dica de ouro** appropriate to the selected type:

- **Funcional:** recommend validating the user flow and measurable value with the product representative.
- **Habilitadora:** recommend defining the future capability it unlocks and the contract or constraint it establishes.
- **Exploratória:** recommend a time-box plus tangible decision artifacts, such as findings and a recommendation.
- **Kaizen:** recommend a baseline metric and a follow-up measurement to prove reduced waste or rework.
- **Bug:** recommend recording reproducible steps, expected behavior, and actual behavior before the fix.
- **Tarefa:** recommend a verifiable completion result and a clear owner or dependency when provided.
- **Débito Técnico:** recommend protecting behavior with focused tests before changing the legacy area.

## Final quality check

Before responding, verify that the item type is clear. For stories, verify that the title, story sentence, context, value, acceptance criteria, labels, effort reference, and tip are present. For epics, verify that outcome, context, scope, success criteria, labels, and a slicing-oriented tip are present. In every case, optional sections must contain only supported facts, text must be Jira-ready, and every criterion must be independently verifiable.
