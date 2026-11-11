---
name: gitlab-mr-creation
description: "Crie Merge Requests no GitLab com glab, atribuindo-os à pessoa autenticada e redigindo uma descrição detalhada em português do Brasil. Use quando a solicitação for abrir um MR; não use apenas para revisar um MR existente."
---

# Criação de Merge Request no GitLab

Crie o Merge Request com `glab`. A pessoa autenticada no `glab` deve ser sempre definida como assignee. Toda a descrição, incluindo títulos e seções, deve estar em português do Brasil.

## Execução com `glab`

Execute todas as chamadas ao `glab` fora do isolamento, com `sandbox_permissions: "require_escalated"`, para reutilizar a credencial local da pessoa usuária. Não use `curl`, tokens ou outros clientes HTTP como alternativa.

Antes de criar o MR, confirme que o repositório atual e a autenticação estão corretos:

```bash
glab auth status
glab repo view --json path_with_namespace,default_branch
glab api user --jq '.username'
```

Use o `username` retornado por `glab api user` como assignee. Não fixe um nome de usuário e não presuma que `@me` será interpretado da mesma forma em todas as versões do CLI.

## Preparar o MR

Identifique a branch de origem atual e a branch de destino solicitada. Se não houver destino informado, use a branch padrão do repositório. Confira se a branch de origem possui commits e alterações relevantes em relação ao destino. Não é necessário verificar previamente se já existe MR aberto para a branch.

Não faça push, commit, alteração de código, adicione labels, reviewers, milestone ou configure auto-merge, salvo quando isso tiver sido solicitado ou já fizer parte do escopo aprovado.

Baseie o título e a descrição no diff, nos commits, na demanda relatada e nos testes efetivamente executados. Não invente requisitos, validações, impactos ou resultados. Quando uma informação importante não estiver disponível, registre a limitação de forma objetiva ou peça esclarecimento antes de criar o MR se ela impedir uma descrição fiel.

## Descrição em português do Brasil

Para MRs comuns, escreva uma descrição detalhada com esta estrutura, omitindo somente se não se aplicar:

```markdown
## Contexto

<problema, necessidade ou oportunidade que motivou a demanda>

## Requisitos atendidos

- <requisito funcional ou técnico atendido>

## Implementação

- <mudança realizada e como ela atende ao requisito>

## Motivos e impacto

- <por que a solução foi adotada e efeito esperado>

## Pontos de atenção

- <riscos, dependências, compatibilidade, rollout ou lacunas conhecidas>

## Validação

- <testes, verificações ou motivo de não terem sido executados>
```

Considere como hotfix somente quando a pessoa usuária o indicar ou houver evidência inequívoca no contexto ou na convenção da branch. Para um hotfix, mantenha as seções pertinentes e acrescente:

```markdown
## Correção aplicada

- <defeito corrigido e comportamento anterior>
- <comportamento esperado após a correção>

## Motivo da urgência

<impacto operacional, risco ou incidente que justifica o hotfix>
```

Explique com precisão o que foi corrigido, a causa ou motivação conhecida, o impacto e as verificações. Não declare causa-raiz se ela não tiver sido comprovada.

## Criar e confirmar

Monte a descrição em um arquivo temporário para preservar quebras de linha e Markdown. Em seguida, crie o MR, incluindo explicitamente a atribuição à pessoa autenticada:

```bash
glab mr create \
  --source-branch "<branch-origem>" \
  --target-branch "<branch-destino>" \
  --title "<título em português>" \
  --description-file "<arquivo-temporário>" \
  --assignee "<username-autenticado>"
```

Depois, consulte o MR criado com `glab mr view` e confirme IID, URL, branches e assignee. Informe esses dados à pessoa usuária juntamente com um resumo conciso do conteúdo publicado. Se a criação falhar, informe o erro e não tente criar o MR novamente sem antes verificar se a primeira tentativa já o criou.
