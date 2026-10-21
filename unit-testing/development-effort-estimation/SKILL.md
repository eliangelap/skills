---
name: development-effort-estimation
description: Analyze the current repository and produce a realistic, human-developer effort estimate for web (React), mobile (React Native), or Node.js/NestJS demands. Use when asked to size a feature, change, bug fix, or technical demand with P20/P50/P80 ranges for senior, mid-level, and junior developers.
---

# Development Effort Estimation

Produce a realistic P20/P50/P80 estimate calibrated to the repository actually available in the current working directory. Do not ask questions: state material assumptions and proceed.

## Scope and constraints

- Include only production implementation, unit tests for changed behavior, and debugging performed within each task.
- Exclude E2E/Maestro/Cypress tests, PR work, review, deploy, QA, and documentation unless explicitly requested.
- Never create a standalone code-reading or debugging task. Embed code-reading overhead in each implementation task: 10% for unfamiliar modules and 5% for familiar modules.
- Inspect and estimate only the current repository. If the demand refers to an absent repository, layer, service, or application, ignore it completely.
- Never invent files, modules, integrations, patterns, or work that cannot be supported by the repository inspection.
- Treat **Likely** as P50: the median realistic result, not a comfortable or buffered commitment. Put scenarios beyond P80 in the risk table.

## Phase 0 — inspect the repository first

Before drafting the estimate, inspect the repository to establish:

1. Directory structure and relevant existing files.
2. Stack, architecture, naming, and code organization.
3. Only the layers that are present.
4. Existing integrations such as authentication, queues, and third parties.
5. Test presence, framework, and conventions.

Use targeted file search and read representative implementation and test files. Do not mention this inspection as a separately estimated task.

## Produce the estimate in this order

### 1. Understanding the demand

Briefly describe the problem, the repository areas affected, and explicit assumptions. Distinguish assumptions from facts observed in the codebase.

### 2. Technical impact map

List the real files and modules to create or change. For each, classify reuse:

- **New** — no comparable implementation exists.
- **Pattern** — a comparable implementation exists and can be copied and adapted.
- **Modify** — an existing file is changed in place.

Use this format:

| File or module | Reuse | Evidence / reason |
|---|---|---|
| `actual/path/file.ts` | Pattern | Matches existing `actual/path/reference.ts` pattern |

If a precise filename cannot be established from the demand and repository, identify the real module or directory rather than fabricating a filename.

### 3. Task breakdown and estimates

Create implementation-sized tasks; include the matching unit-test work in the task that changes the behavior. Assign reuse and complexity (`Simple`, `Medium`, or `Complex`) to each task.

Start from the closest applicable Senior/New reference below. For work not listed, choose the closest reference and say which one was used.

| Task type | Minimum | Likely | Pessimistic |
|---|---:|---:|---:|
| Simple screen, one action, no form | 0.5h | 0.75h | 1.25h |
| Form screen (React Hook Form + Yup) | 1h | 1.5h | 2.5h |
| Screen with camera/native permission | 1.5h | 2.5h | 4h |
| Use case + unit test; gateway exists | 0.5h | 0.75h | 1.25h |
| Gateway method + HTTP implementation | 0.5h | 0.75h | 1.25h |
| Domain entity/type | 0.25h | 0.5h | 0.75h |
| DI binding and keys | 0.25h | 0.5h | 0.75h |
| Navigation stack restructure | 1h | 1.5h | 2.5h |
| Context-state update | 0.25h | 0.5h | 0.75h |
| Native library installation and iOS/Android config | 2h | 3.5h | 6h |
| Animated processing screen | 1h | 2h | 3.5h |
| Manual integration smoke test | 1h | 1.5h | 2.5h |

Apply this calculation, retaining sensible two-decimal precision internally and displaying practical rounded values:

1. Start with the reference Likely time and add the embedded familiarity overhead (5% familiar, 10% unfamiliar).
2. Apply reuse to Likely: New ×1.00, Pattern ×0.65, Modify ×0.75.
3. Apply the seniority multiplier after reuse: Senior ×1.00; Pleno ×1.25/×1.40/×1.55; Junior ×1.75/×2.25/×3.00 for Simple/Medium/Complex.
4. Derive P20 from the selected reference's `Minimum ÷ Likely` ratio.
5. Derive P80 from the selected reference's `Pessimistic ÷ Likely` ratio, capped at 1.7× Likely for Senior, 1.8× for Pleno, and 2.0× for Junior.

The task table shows P50 only:

| Task | Reuse | Complexity | Senior Likely | Pleno Likely | Junior Likely |
|---|---|---|---:|---:|---:|
| Concrete task with embedded test work | Pattern | Medium | 0.0h | 0.0h | 0.0h |

Then sum every task for this totals table. Show 8-hour workdays.

| Scenario | Senior time | Senior days | Pleno time | Pleno days | Junior time | Junior days |
|---|---:|---:|---:|---:|---:|---:|
| Minimum (P20) | | | | | | |
| Likely (P50) | | | | | | |
| Pessimistic (P80) | | | | | | |

### 4. Ideal implementation sequence

List the dependency-aware order of the tasks and give a short reason for it. Prefer foundational types/contracts, then backend or state, then UI/navigation, then unit tests integrated with each change. Adapt this order to the real architecture rather than forcing layers that do not exist.

### 5. Complexity classification

Classify the demand as **Very simple**, **Simple**, **Medium**, **Complex**, or **Very complex**. Justify it from impacted layers, business logic, regression risk, and external dependencies found in the repository.

### 6. Technical risks

List only risks that could push the work beyond P80. Do not use the risk table to pad the estimate.

| Risk | Probability | Impact | Senior delta | Pleno delta | Mitigation |
|---|---|---|---:|---:|---|

Use `N/A` when no material beyond-P80 risk is supported by the repository and demand.

## Seniority calibration

- **Senior:** recognizes familiar use-case and DI patterns quickly; tests take roughly 50% of implementation effort.
- **Pleno:** consults reference files before coding; tests take roughly 80%; native configuration and navigation require more tracing.
- **Junior:** studies examples and documentation, can iterate on patterns, tests take roughly 120%, and unknown native/DI/navigation behavior carries substantially higher uncertainty.

Do not add a generic project-management contingency. Make each task reflect its own scope, familiarity, testing, and likely debugging.
