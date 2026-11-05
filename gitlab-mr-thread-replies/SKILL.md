---
name: gitlab-mr-thread-replies
description: Analise e responda threads não resolvidas de code review em Merge Requests do GitLab com `glab`, propondo correções antes de alterar código ou publicar. Use para tratar comentários de revisão; não use para criar ou revisar o código do MR sem uma thread em escopo.
---

# GitLab MR Thread Replies

Trate o MR como um ciclo de análise, proposta aprovada, correção e retorno às threads. Alterações no código, commits, pushes e comentários no GitLab são ações externas: não as execute antes da aprovação explícita do plano pela pessoa usuária.

## Identificar o MR e as threads

Execute os comandos dentro do checkout do projeto para que `:fullpath` seja resolvido pelo `glab`. Quando o MR não estiver inequívoco, peça o IID ou a URL; quando estiver claro, consulte seus dados antes de publicar:

```bash
glab mr view <iid> --json iid,title,web_url
glab api --paginate "projects/:fullpath/merge_requests/<iid>/discussions"
```

Leia o MR e examine cada discussão e suas `notes`. Use o `id` da discussão (não o ID individual de uma nota), diferencie comentários de linha, comentários gerais e notas de sistema, e concentre a análise nas threads não resolvidas. Não responda ou altere threads já resolvidas, a menos que a pessoa tenha pedido isso.

Analise o código, o diff e o contexto de cada apontamento para decidir se ele procede. Não presuma que um comentário do revisor está correto, nem descarte um apontamento sem uma justificativa técnica verificável.

## Plano para aprovação

Antes de corrigir código, commitar, fazer push ou publicar qualquer resposta, mostre um plano em Markdown e aguarde aprovação explícita. Use uma tabela com **uma thread por linha**, mesmo quando mais de uma tiver a mesma solução:

```markdown
| Thread | Resumo | Procede? | Proposta |
| --- | --- | --- | --- |
| `<discussion-id>` | Resumo curto do apontamento | Sim | Corrigir `<componente>` e responder com o hash do commit e o resumo. |
| `<discussion-id>` | Resumo curto do apontamento | Não | Responder que `<motivo técnico verificável>`. |
```

Explique o diagnóstico de forma suficiente para a decisão da pessoa usuária. Se a análise depender de informação ausente ou houver dúvida material sobre o comportamento esperado, exponha-a no plano e peça esclarecimento em vez de escolher uma correção por conta própria.

## Executar correções aprovadas

Para cada thread aprovada como procedente, use a skill de desenvolvimento disponível e compatível com a linguagem e a camada do projeto antes de modificar o código. Quando a alteração atravessar mais de uma camada, use as skills adequadas a cada uma. Se não houver uma skill de desenvolvimento compatível disponível, avise a pessoa usuária dessa ausência antes de implementar; não apresente uma skill de review como se ela autorizasse ou substituísse uma skill de desenvolvimento.

Implemente e valide a correção conforme a skill aplicável. Faça commit e push da correção antes de responder à thread. Mantenha a relação entre cada thread e sua alteração inequívoca; se uma única alteração resolve várias threads, registre o mesmo hash em cada resposta e deixe isso explícito. Obtenha o hash já enviado com:

```bash
git rev-parse --short HEAD
git push
```

## Redigir e publicar

Para um apontamento procedente, responda com o hash do commit enviado e um resumo conciso da solução. Para um apontamento que não procede, responda tecnicamente por que não haverá correção, com base na análise realizada. Não alegue que uma correção foi implementada ou validada sem evidência. Mantenha a língua e o tom predominantes da thread, salvo orientação contrária.

Publique uma resposta como uma nova nota da discussão:

```bash
glab api --method POST \
  "projects/:fullpath/merge_requests/<iid>/discussions/<discussion-id>/notes" \
  --raw-field "body=<resposta>"
```

Use `--raw-field` para que o `glab` codifique o texto com segurança no JSON. Para várias threads, relacione cada resposta ao respectivo `discussion-id`; nunca reutilize o ID da nota original como se fosse o ID da discussão.

Após publicar, confirme a nota retornada pela API ou recarregue a discussão. Informe quais threads receberam resposta, seus respectivos hashes quando houver correção, e quaisquer threads deliberadamente ignoradas. Não marque uma discussão como resolvida só porque respondeu; faça isso somente se for solicitado explicitamente e após confirmar que a resolução é apropriada.

Se houver ambiguidade material sobre quais comentários responder, sobre a mensagem a publicar, ou sobre a aprovação do plano, apresente o resumo das threads relevantes e peça orientação antes de agir.
