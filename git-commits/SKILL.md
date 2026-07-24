---
name: git-commits
description: Regras de preparação e formatação de commits para qualquer repositório. Use quando a usuária pedir para criar, fazer, revisar ou sugerir um commit.
---

# Repo Commits

Use esta skill quando a tarefa envolver preparar, revisar, sugerir ou criar commits em qualquer repositório Git.

## Comportamento Esperado

- Quando a usuária pedir para `criar o commit`, `fazer o commit`, `commitar` ou equivalente, a ação padrão deve ser executar o fluxo completo de commit, e não apenas sugerir a mensagem.
- Só responda apenas com proposta de mensagem quando a usuária pedir explicitamente uma sugestão, revisão da mensagem, ou quando ainda não estiver claro quais arquivos devem entrar no commit.
- Antes de commitar, revise o estado do repositório, confirme que o agrupamento de arquivos está coerente e então faça `git add` e `git commit` dos arquivos pertinentes.
- Se houver alterações não relacionadas misturadas no worktree, preserve-as e faça stage apenas do conjunto coerente com o commit em questão.
- Depois de criar o commit, informe o hash gerado, o título final e se hooks automáticos alteraram arquivos durante o processo.

## Commit Rules

- As mensagens de commit devem ser escritas em português, com acentuação correta, salvo se o padrão do repositório exigir outro idioma.
- Siga o padrão Commitizen / Conventional Commits no título: `tipo(escopo): emoji título curto`.
- Quando a equipe usar identificador de ticket ou branch no escopo, extraia esse código da branch atual, por exemplo `feature/GESTRUR-597-ajuste-data` vira `GESTRUR-597`.
- Quando não houver identificador aplicável, use um escopo curto e coerente com o contexto da alteração.
- O título deve ser curto, objetivo e focado no resultado da alteração.
- O corpo da mensagem é permitido e recomendado quando houver contexto relevante.
- No corpo, explique motivação, impacto, regras de negócio e observações de implementação.
- Prefira descrever o motivo ou efeito da mudança, não uma lista de arquivos alterados.
- Use tipos compatíveis com `commitlint`, como `feat`, `fix`, `refactor`, `chore`, `test`, `docs`, `style`, `perf`, `build`, `ci` e `revert`.
- Antes de commitar, adapte a mensagem às convenções específicas do repositório quando elas divergirem deste padrão base.

## Formato Esperado

- Título obrigatório:
  `tipo(escopo): emoji título`
- Corpo opcional, separado por linha em branco:

  ```text
  tipo(escopo): emoji título

  descrição detalhada da alteração
  - impacto principal
  - regra de negócio afetada
  - observações importantes
  ```

## Exemplos

- `refactor(GESTRUR-597): ♻️ ajustada consulta da data de referência`
- `fix(auth): 🐛 corrigida validação do token expirado`
- `feat(pagamentos): ✨ adicionada validação de acesso revogado`
- `test(api): ✅ adicionados testes do fluxo de autenticação`
- `chore(build): 🔧 ajustada configuração de build`

- Exemplo com título + corpo:

  ```text
  fix(movimentacao): 🐛 corrigido cálculo do total da movimentação

  Ajustado o cálculo para considerar apenas itens válidos no período informado.
  A alteração evita divergência no fechamento quando existem lançamentos estornados.
  ```

## Regra Prática

- Antes de qualquer commit, pergunte obrigatoriamente: `Deseja alterar a versão antes do commit?`
  1. Não
  2. Alterar Patch
  3. Alterar Minor
  4. Alterar Major
- Execute a release escolhida antes de preparar o commit: Patch com `yarn release:hotfix`, Minor com `yarn release:minor` e Major com `yarn release:major`.
- Se a usuária escolher `Não`, siga diretamente com a revisão, stage e commit. Se escolher uma alteração de versão, revise novamente o estado do repositório e inclua no commit as alterações de versão pertinentes.
- Antes de criar o commit, confira se a mensagem segue exatamente o padrão esperado pelo repositório para evitar falha em hooks como `commit-msg`.
- Se estiver usando `yarn commit` ou ferramenta equivalente, preencha o tipo e o escopo conforme a convenção vigente no projeto.
- Se houver contexto importante, preencha também o corpo da mensagem com uma descrição detalhada.
- Antes de propor ou criar commits, verifique `git status --short`, `git diff`, `git diff --cached` e `git log -5 --oneline`.
- Agrupe arquivos que entregam a mesma funcionalidade no mesmo commit.
- Isole correções reutilizáveis de componentes compartilhados em commit próprio quando fizer sentido.
- Isole ajustes de configuração em commit próprio.
- Evite dividir um mesmo fluxo em commits artificiais; só separe quando a divisão continuar coerente no histórico.

## Comandos Úteis

- Título + corpo com `git commit`:
  `git commit -m "fix(auth): 🐛 corrigida validação do token" -m "Detalha a motivação, impacto e regra de negócio afetada."`
