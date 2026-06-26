---
name: code-review-nodejs
description: "Review code changes in Node.js projects. Use when a user wants a code review of local changes, staged files, or the current branch, especially in TypeScript, NestJS, Express, Fastify, or similar back-end repositories."
---

# Node Code Review

Use this skill when the task is to review code changes in a Node.js repository.

## Workflow

1. Identify the review scope.
   - For branch review, compare the current branch against the repository base branch.
   - Prefer `git diff origin/develop...HEAD` when the repo uses `develop`.
   - Otherwise use the appropriate base, such as `origin/main...HEAD` or `origin/master...HEAD`.
   - For staged-only review, use `git diff --cached`.
   - For worktree review including unstaged changes, use `git diff HEAD`.
2. Read the affected files and enough surrounding context to understand behavior and impact.
3. Review for correctness, regressions, risks, and missing tests.
4. Always provide the review in Português do Brasil unless the user explicitly asks for another language.

## Review Criteria

### 1. Architecture and project patterns

- Check if the change follows the repository structure and framework conventions.
- In TypeScript projects, verify type safety and avoid unnecessary `any`.
- In NestJS projects, verify module boundaries, providers, DTOs, decorators, and dependency injection.
- In Express/Fastify projects, verify route/controller, service, and persistence separation when such layers exist.

### 2. Correctness and regressions

- Look for logic bugs, broken edge cases, incorrect assumptions, and incompatible contract changes.
- Confirm that renamed or extended DTOs, response objects, and validation rules remain consistent with callers and tests.
- Check for null/undefined handling, async flow issues, and error propagation problems.

### 3. Code quality

- Flag unclear naming, long functions, duplicated logic, dead code, and weak abstractions.
- Verify whether the implementation is understandable without hidden coupling.
- Prefer concrete, actionable findings over generic style comments.

### 4. Tests

- Check whether the change has adequate unit or integration coverage.
- Look for missing assertions, missing edge cases, and outdated expectations after contract changes.
- If tests fail, identify whether the failure indicates a real regression or an outdated test.

### 5. Security and performance

- Watch for secrets, unsafe query construction, missing authorization checks, and unsafe input handling.
- Check for avoidable N+1 queries, repeated I/O, unnecessary loops, or excessive synchronous work in request paths.
- In transactional flows, verify that related writes are kept consistent.

### 6. Error messages and API consistency

- Check if equivalent errors use consistent language and wording across validation, service, controller, and tests.
- Verify that status codes and thrown errors match the real behavior of the implementation.

## Output Format

Default to a review-first response:

1. List findings first, ordered by severity, with file references when possible.
2. Then list open questions or assumptions.
3. Finish with a brief summary only if it adds value.

If no issues are found, say that explicitly and mention any residual risk or testing gap.

## Useful Commands

- `git status --short`
- `git diff --cached`
- `git diff HEAD`
- `git diff origin/develop...HEAD`
- `git diff origin/main...HEAD`
- `git log --oneline --decorate -5`
