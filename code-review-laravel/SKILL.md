---
name: code-review-laravel
description: "Revise mudanças PHP e Laravel para identificar riscos de segurança, desempenho, arquitetura e convenções. Use em code reviews de diffs Git ou diretórios selecionados; não use para implementar correções."
---

# Code Review Laravel

Revise apenas o escopo solicitado — normalmente o diff atual, staged, uma branch ou diretórios indicados — e baseie cada achado em evidência no código. Não altere arquivos ao revisar, salvo pedido explícito para corrigir os problemas.

## Focos da revisão

### Desempenho e Eloquent

- Procure consultas dentro de `foreach` e outros loops, em especial acessos a relacionamentos que indiquem N+1. Sugira eager loading com `with()` quando aplicável.
- Avalie coleções potencialmente grandes obtidas com `get()`. Considere `select()`, `chunk()`, `cursor()` ou `paginate()` de acordo com o uso real.
- Identifique relacionamentos acessados preguiçosamente quando o carregamento prévio for necessário; não reporte isso se já houver eager loading, strict mode ou outro mecanismo comprovado no escopo analisado.

### Laravel idiomático e arquitetura

- Exija `FormRequest` dedicado para validação de entrada em controllers; reporte validação inline como inconformidade.
- Mantenha controllers finos: regras de negócio, orquestrações complexas e fluxos extensos devem ser extraídos para Actions, Services ou casos de uso coerentes com a arquitetura do projeto.
- Verifique PSR-12 e convenções Laravel somente quando a divergência prejudicar legibilidade, consistência ou manutenção.
- Aplique princípios de Clean Architecture: regras de negócio não pertencem a controllers ou gateways de banco; métodos devem ter responsabilidade única e tamanho proporcional; exceções precisam de mensagens úteis sem vazar detalhes técnicos ao cliente.

### Segurança e autorização

- Examine `$fillable`, `$guarded` e fluxos de `create()`, `update()` e `fill()` para riscos de mass assignment.
- Confirme que operações críticas têm autorização via Policy, `$this->authorize()` ou `Gate`, considerando middleware e verificações já presentes no fluxo.
- Rastreie entradas do usuário até consultas. Dados usados em `DB::raw`, SQL concatenado ou fragmentos dinâmicos devem ser validados e parametrizados; reporte caminhos plausíveis de SQL injection.
- Não trate sanitização genérica como substituta de validação contextual. Evite falsos positivos quando o dado já foi validado ou a construção utiliza bindings comprovadamente seguros.

## Como relatar

Relate somente achados acionáveis. Ordene do mais grave ao menos grave e use este formato para cada inconformidade:

1. **Arquivo e linha:** `caminho/do/arquivo.php:linha` (linha aproximada quando o review for de diff).
2. **Gravidade:** `[Bloqueante]`, `[Melhoria]` ou `[Informativo]`.
3. **Descrição do problema:** explicação curta, direta e ligada ao impacto.
4. **Sugestão de correção:** exemplo PHP conciso que mostre a refatoração adequada.

Classifique como **Bloqueante** riscos exploráveis de segurança, ausência relevante de autorização ou falhas que comprometam dados; como **Melhoria** problemas de arquitetura, desempenho e manutenção; e como **Informativo** ajustes de baixo impacto. Se não houver achados, diga isso explicitamente e informe o escopo revisado. Não invente linhas, contexto ou problemas fora das mudanças examinadas.
