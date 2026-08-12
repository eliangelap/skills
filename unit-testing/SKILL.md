---
name: unit-testing
description: "Unit test generation for Eliangela-style backend projects using NestJS + TypeORM + layered @core/@server/@worker architecture. Use when writing or expanding specs for entities, DTOs, use cases, gateways, container registries, controllers, workers, or e2e flows in similar repositories."
argument-hint: "<module-name> [layer: domain|application|infra|registry|controller|worker|e2e]"
---

# Unit Testing

## When to Read References
- Read `references/details.md` to understand the project architecture, layering, infra, and runtime conventions before writing tests in an unfamiliar module.
- Read `references/how_to_test.md` before generating tests for a layer-specific workflow in `@core`, `@server`, or `@worker`.
- Read `references/how_to_do.md` when the task involves creating or extending a module and the tests need to follow the exact Eliangela build order.
- Read `references/e2e-test-plan.md` when adding or adjusting e2e tests that depend on ordered execution, seeds, or Oracle PK/FK constraints.
- Read the prompt references only when the task is narrowly focused:
  - `references/prompt_test_unit_domain_entity.md` for domain entities, DTOs, enums, gateways, or value objects.
  - `references/prompt_test_unit_use_case.md` for application/use-case tests.
  - `references/prompt_test_unit_infra_registry.md` for container registry tests.

## Core Rules
- Check `package.json` first to confirm the active versions of Jest, NestJS, class-validator, ORM, and related tooling.
- Use the `modality` module as the canonical style reference when the current repository follows the Eliangela pattern.
- Follow TDD: write the failing test first, implement the minimum production change, then rerun until green.
- Prefer the layer order Domain -> Application -> Infra -> Registry -> Server/Worker -> E2E.
- Keep `describe` and `it` text in English, while preserving runtime exception messages exactly as implemented, usually in Portuguese.

## Testing Conventions
- Reuse factories from `mock/` when available; extend them instead of duplicating fixtures.
- Prefer typed Jest mocks with `satisfies jest.Mocked<T>` or explicit Jest helper generics.
- Do not use `as unknown as jest.Mocked<T>`.
- Never hit real infra in unit tests; mock DB, Redis, queues, storage, and external services.
- Keep controller tests facade-oriented and registry tests binding-oriented.
- Run the validation commands that exist in `package.json`, usually `yarn lint`, `yarn test`, and `yarn test:e2e` when applicable.

## Final Checklist
- Spec is in the correct layer path.
- Success, error, and edge cases are covered.
- Mocks are typed safely and return contract-compatible values.
- No unused imports remain in spec or production code.
- The relevant repository validation commands were run.
