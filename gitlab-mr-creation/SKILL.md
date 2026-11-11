---
name: gitlab-mr-creation
description: "Crie Merge Requests no GitLab com glab, atribuindo-os à pessoa autenticada e redigindo uma descrição detalhada em português do Brasil. Use quando a solicitação for abrir um MR; não use apenas para revisar um MR existente."
---

# Criação de Merge Request no GitLab

Crie o Merge Request com `glab`. A pessoa autenticada no `glab` deve ser sempre definida como assignee. Toda a descrição, incluindo títulos e seções, deve estar em português do Brasil.

## Execução com `glab`

Sempre execute qualquer comando `glab` fora do sandbox, com `sandbox_permissions: "require_escalated"`, inclusive consultas, criação e confirmação do MR. Isso permite reutilizar a credencial local da pessoa usuária. Não use `curl`, tokens ou outros clientes HTTP como alternativa.

Execute os comandos abaixo no diretório do repositório-alvo. Os exemplos usam variáveis de shell apenas para evitar que informações obtidas em uma etapa sejam redigitadas ou presumidas nas etapas seguintes.

### Identificar repositório, autenticação e assignee

Para obter metadados de forma estruturada de maneira compatível com o CLI, use `glab api` com o placeholder `:fullpath`, que representa o projeto do repositório Git atual. `glab api` não oferece a opção `--jq`; processe sua saída JSON com `jq -er`. O `pipefail` faz a atribuição falhar se a chamada da API ou a extração do campo falhar.

```bash
git rev-parse --show-toplevel
git remote get-url origin
glab auth status
set -o pipefail
project_path="$(glab api projects/:fullpath | jq -er '.path_with_namespace')"
target_branch="$(glab api projects/:fullpath | jq -er '.default_branch')"
assignee="$(glab api user | jq -er '.username')"
```

Se `project_path`, `target_branch` ou `assignee` estiver vazio, ou qualquer comando falhar, interrompa o fluxo e resolva a autenticação, o remote ou o repositório antes de criar o MR. Use exatamente o `username` retornado em `assignee`; não fixe um nome de usuário e não presuma que `@me` será interpretado da mesma forma em todas as versões do CLI.

## Preparar o MR

Identifique a branch de origem atual. Se a pessoa usuária informar uma branch de destino, ela substitui o valor obtido para `target_branch`; caso contrário, use a branch padrão obtida da API. Não crie MR a partir de HEAD destacado ou quando origem e destino forem iguais.

```bash
source_branch="$(git branch --show-current)"
test -n "$source_branch"
test "$source_branch" != "$target_branch"
git rev-parse --verify --quiet "${target_branch}^{commit}"
git rev-parse --verify --quiet "${source_branch}^{commit}"
git log --oneline "${target_branch}..${source_branch}"
git diff --stat "${target_branch}...${source_branch}"
git diff --check "${target_branch}...${source_branch}"
git ls-remote --exit-code --heads origin "$source_branch"
```

Os comandos de comparação devem evidenciar os commits e o diff que serão publicados. Se não houver commits ou diff relevantes, pare e informe a situação. `git ls-remote` confirma que a branch de origem já está publicada, sem realizar push. Se a branch ainda não existir no remoto, peça autorização explícita para fazer push — a criação do MR não deve publicar a branch implicitamente.

Não é necessário consultar previamente se existe MR aberto para a branch. Essa consulta fica reservada para recuperar com segurança uma possível criação após uma falha.

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

## Criar, recuperar de falha e confirmar

Monte a descrição em um arquivo temporário para preservar quebras de linha e Markdown. Substitua o conteúdo entre `EOF` pela descrição baseada nas evidências reunidas. O `trap` remove somente esse arquivo temporário ao término do shell.

```bash
description_file="$(mktemp "${TMPDIR:-/tmp}/gitlab-mr-description.XXXXXX.md")"
trap 'rm -f "$description_file"' EXIT

cat > "$description_file" <<'EOF'
## Contexto

<contexto confirmado>

## Requisitos atendidos

- <requisito confirmado>

## Implementação

- <mudança confirmada>

## Motivos e impacto

- <motivo e impacto confirmados>

## Pontos de atenção

- <risco, dependência ou lacuna conhecida>

## Validação

- <testes executados ou motivo de não execução>
EOF
```

Crie o MR com todas as opções que evitam interação e efeitos colaterais não solicitados. `--push=false` é explícito para que o comando nunca publique a branch; `--yes` apenas confirma a submissão já inteiramente parametrizada.

```bash
glab mr create \
  --source-branch "<branch-origem>" \
  --target-branch "<branch-destino>" \
  --title "<título em português>" \
  --description-file "$description_file" \
  --assignee "$assignee" \
  --push=false \
  --yes
```

Defina `mr_title` com o título em português derivado das evidências e, na execução real, use as variáveis já verificadas:

```bash
mr_title="<título em português baseado no diff e na demanda>"

glab mr create \
  --source-branch "$source_branch" \
  --target-branch "$target_branch" \
  --title "$mr_title" \
  --description-file "$description_file" \
  --assignee "$assignee" \
  --push=false \
  --yes
```

Depois da criação, consulte o MR pela branch de origem e confirme IID, URL, branches e assignee com saída estruturada:

```bash
glab mr view "$source_branch" \
  --output json \
  --jq '{iid, web_url, source_branch, target_branch, assignees: [.assignees[].username]}'
```

Se `glab mr create` falhar, guarde o erro da tentativa e não a repita. Primeiro verifique se a criação foi concluída apesar da falha, usando o mesmo comando de consulta. Se houver MR, confirme seus dados e informe-o; se a consulta não encontrar MR, informe o erro original e peça orientação antes de uma nova tentativa.

Informe à pessoa usuária IID, URL, branches e assignee, juntamente com um resumo conciso do conteúdo publicado.
