---
name: git-commits
description: Regras de preparação e formatação de commits para qualquer repositório. Use quando a usuária pedir para criar, fazer, revisar ou sugerir um commit.
---

# Repo Commits

Use esta skill quando a tarefa envolver preparar, revisar, sugerir ou criar commits em qualquer repositório Git.

## Comportamento Esperado

- Quando a usuária pedir para `criar o commit`, `fazer o commit`, `commitar` ou equivalente, a ação padrão deve ser executar o fluxo completo de commit, e não apenas sugerir a mensagem.
- Só responda apenas com proposta de mensagem quando a usuária pedir explicitamente uma sugestão, revisão da mensagem, ou quando ainda não estiver claro quais arquivos devem entrar no commit.
- Antes de commitar, revise o estado do repositório e inclua todas as alterações presentes — rastreadas, não rastreadas, staged ou não — usando `git add -A` antes de criar o commit.
- O resultado padrão de um commit deve deixar o worktree limpo. Não preserve alterações para depois nem separe arquivos em commits distintos por iniciativa própria.
- A única exceção é quando a usuária indicar explicitamente que um ou mais arquivos não devem ser enviados no commit. Preserve somente esses arquivos fora do stage e informe que eles permaneceram no worktree.
- Depois de criar o commit, informe o hash gerado, o título final e se hooks automáticos alteraram arquivos durante o processo.
- Após o commit, execute `git status --short` para confirmar que o worktree está limpo, exceto pelos arquivos que a usuária tenha explicitamente pedido para não enviar.

## Commits Atômicos

- Quando a usuária solicitar explicitamente commits atômicos, substitua o commit único padrão por uma sequência de commits independentes, agrupados por funcionalidade ou mudança coerente.
- Revise os diffs e defina os grupos antes de fazer stage; cada commit deve ser completo, compilável quando aplicável e não depender de alterações que ficaram apenas em outro grupo.
- Faça stage somente do grupo atual — inclusive trechos específicos de um mesmo arquivo quando necessário — e crie uma mensagem cujo tipo, escopo, título e corpo descrevam exatamente aquela alteração.
- Mantenha testes, ajustes de configuração e documentação no mesmo commit da funcionalidade que eles sustentam; se entregarem uma mudança independente, crie um commit atômico próprio.
- Ao concluir todos os grupos, confirme que todos os arquivos permitidos foram commitados e que o worktree está limpo, preservando apenas os arquivos que a usuária tenha explicitamente pedido para não enviar.

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
- Em projetos Node.js ou React, verifique se existe um arquivo `VERSION` na raiz do projeto. Se existir, seu conteúdo deve ser exatamente a versão de `package.json` (incluindo a atualização gerada pela release).
- Antes do commit, compare `VERSION` com o campo `version` de `package.json` quando ambos existirem. Corrija `VERSION` se houver divergência e inclua a correção no mesmo commit.
- Ao realizar uma alteração de versão, atualize também `VERSION` para receber exatamente a nova versão de `package.json` e inclua ambos os arquivos no commit.
- Se a usuária escolher `Não`, após essa verificação de consistência siga com a revisão, stage e commit. Se escolher uma alteração de versão, revise novamente o estado do repositório e inclua no commit as alterações de versão pertinentes, inclusive `VERSION` quando existir.
- Antes de criar o commit, confira se a mensagem segue exatamente o padrão esperado pelo repositório para evitar falha em hooks como `commit-msg`.
- Se estiver usando `yarn commit` ou ferramenta equivalente, preencha o tipo e o escopo conforme a convenção vigente no projeto.
- Se houver contexto importante, preencha também o corpo da mensagem com uma descrição detalhada.
- Antes de propor ou criar commits, verifique `git status --short`, `git diff`, `git diff --cached` e `git log -5 --oneline`.
- Ao criar commits atômicos, agrupe arquivos que entregam a mesma funcionalidade no mesmo commit e evite dividir um fluxo em commits artificiais.

## Comandos Úteis

- Título + corpo com `git commit`:
  `git commit -m "fix(auth): 🐛 corrigida validação do token" -m "Detalha a motivação, impacto e regra de negócio afetada."`
