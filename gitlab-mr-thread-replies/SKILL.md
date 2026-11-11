---
name: gitlab-mr-thread-replies
description: Analise e responda threads não resolvidas de code review em Merge Requests do GitLab com `glab`, propondo correções antes de alterar código ou publicar. Use para tratar comentários de revisão; não use para criar ou revisar o código do MR sem uma thread em escopo.
---

# GitLab MR Thread Replies

Trate o MR como um ciclo de análise, proposta aprovada, correção e retorno às threads. Alterações no código, commits, pushes, respostas e resolução de threads são ações externas: não as execute antes da aprovação explícita do plano pela pessoa usuária.

## Execução do `glab`

Execute toda chamada ao `glab` fora do sandbox, com `sandbox_permissions: "require_escalated"`, para reutilizar a credencial local da pessoa usuária. A justificativa da elevação deve ser curta e específica. Não leia, imprima, copie ou substitua credenciais manualmente e não use `curl` ou outro cliente HTTP como alternativa.

Os subcomandos `glab mr note` são experimentais nesta versão do CLI, mas são a interface nativa para listar, responder e resolver discussões. Use-os no checkout do projeto e informe o IID explicitamente quando ele for conhecido.

## Mapa de comandos

| Tarefa | Comando validado |
| --- | --- |
| Consultar os dados do MR | `glab mr view "$mr_iid" --output json --jq '{iid, title, web_url, source_branch, target_branch}'` |
| Examinar o patch do MR | `glab mr diff "$mr_iid" --color=never` |
| Listar apenas threads abertas | `glab mr note list "$mr_iid" --state unresolved --output json` |
| Listar todas as discussões para confirmação | `glab mr note list "$mr_iid" --state all --output json` |
| Responder a uma thread existente | `glab mr note create "$mr_iid" --reply "$discussion_id" --message "$reply_body"` |
| Resolver uma thread | `glab mr note resolve "$mr_iid" "$discussion_id"` |
| Reabrir uma thread, se a pessoa usuária pedir | `glab mr note reopen "$mr_iid" "$discussion_id"` |

Não use `glab mr view --json`: nesta versão a opção correta é `--output json`. Não use `glab mr note create` sem `--reply` para responder uma discussão, pois isso cria uma nova thread. O argumento de `--reply`, `resolve` e `reopen` é o ID da discussão; pode ser o ID completo ou um prefixo único de pelo menos oito caracteres. Prefira o ID completo presente no JSON.

## Identificar e analisar threads

Quando o MR não estiver inequívoco, peça o IID ou a URL. Quando estiver claro, defina e consulte-o antes de propor qualquer ação:

```bash
mr_iid="<iid-do-mr>"

glab mr view "$mr_iid" \
  --output json \
  --jq '{iid, title, web_url, source_branch, target_branch}'
glab mr note list "$mr_iid" --state unresolved --output json
glab mr diff "$mr_iid" --color=never
```

Examine cada discussão e suas notas. Diferencie comentários de linha, gerais e notas de sistema; concentre a análise em threads não resolvidas. Não responda nem altere threads já resolvidas, salvo pedido explícito.

Analise o código, o patch e o contexto de cada apontamento. Não presuma que um comentário procede nem o descarte sem justificativa técnica verificável. Guarde o `id` da discussão, não o ID individual de uma nota, para responder e resolver.

## Plano para aprovação

Antes de corrigir código, commitar, fazer push, responder ou resolver threads, mostre um plano em Markdown e aguarde aprovação explícita. Use uma linha por thread, mesmo que uma correção resolva várias:

```markdown
| Thread | Resumo | Procede? | Proposta |
| --- | --- | --- | --- |
| `<discussion-id>` | Resumo curto do apontamento | Sim | Corrigir `<componente>`, validar, fazer commit e push, responder com o hash e resolver a thread. |
| `<discussion-id>` | Resumo curto do apontamento | Não | Responder com `<motivo técnico verificável>` e manter a thread aberta. |
```

Explique o diagnóstico na medida necessária para a decisão. Se houver informação ausente ou dúvida material sobre o comportamento esperado, exponha-a no plano e peça esclarecimento em vez de escolher a correção.

## Executar correções aprovadas

Para cada thread aprovada como procedente, use a skill de desenvolvimento compatível com a linguagem e a camada do projeto antes de modificar código. Se não houver uma skill compatível, avise antes de implementar; uma skill de review não a substitui.

Implemente e valide a correção. Faça commit e push antes de responder à thread. Mantenha inequívoca a relação entre cada thread e sua alteração; se um commit resolver várias, registre o mesmo hash em cada resposta.

```bash
git rev-parse --short HEAD
git push
```

## Responder, confirmar e resolver

Para um apontamento procedente, mencione o hash enviado e resuma a solução. Para um apontamento que não procede, explique tecnicamente por que não haverá correção. Não alegue implementação ou validação sem evidência. Mantenha a língua e o tom predominantes da thread, salvo orientação contrária.

Defina a mensagem em variável para preservar caracteres especiais e publique uma resposta na discussão existente:

```bash
discussion_id="<id-completo-da-discussao>"
reply_body="<resposta baseada na análise aprovada>"

glab mr note create "$mr_iid" \
  --reply "$discussion_id" \
  --message "$reply_body"
```

Após cada publicação, recarregue as discussões e confirme que a resposta está na thread certa. Para uma thread procedente, só a resolva depois de confirmar que a correção foi commitada, enviada e respondida:

```bash
glab mr note list "$mr_iid" --state all --output json
glab mr note resolve "$mr_iid" "$discussion_id"
glab mr note list "$mr_iid" --state unresolved --output json
```

A última consulta não deve conter uma thread que foi resolvida. Se ainda aparecer, pare e informe a falha; não repita a resolução automaticamente. Não resolva threads que não procedem apenas por ter publicado uma justificativa, nem threads cuja correção, commit, push ou resposta tenha falhado.

Informe quais threads receberam resposta e quais foram resolvidas, os hashes das correções e quaisquer threads deliberadamente mantidas abertas. Se houver ambiguidade material sobre os comentários, a mensagem a publicar ou a aprovação do plano, apresente o resumo relevante e peça orientação antes de agir.
