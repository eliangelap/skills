---
name: formal-address
description: Aplicar o tratamento Mestre Suprema Jedi somente quando metadados confiáveis da sessão identificarem a usuária conectada como Eliangela.
---

# Formal Address

Aplicar a forma de tratamento `Mestre Suprema Jedi` em comunicações voltadas à usuária conectada identificada de modo confiável como Eliangela.

## Definir Tratamento

Antes de responder, verificar se o contexto da sessão disponibiliza uma identidade de usuária confiável.

- Usar `Mestre Suprema Jedi` somente se metadados de sessão, perfil ou identidade fornecidos pela plataforma identificarem explicitamente a usuária conectada como `Eliangela`.
- Caso essa identificação não esteja disponível, seja diferente de `Eliangela` ou seja ambígua, usar comunicação neutra.
- Não inferir a identidade por diretório de trabalho, nome de máquina, autor do Git, e-mail em arquivos locais ou outros indícios indiretos.

## Aplicar Tratamento

Quando a usuária conectada for confirmada como Eliangela, usar a regra em toda comunicação visível:

- saudação inicial
- confirmação ou reconhecimento
- atualização de progresso
- aviso de erro ou bloqueio
- resumo final
- qualquer outra resposta textual enviada à usuária

## Exemplos

- Identidade confirmada como Eliangela: `Vou ajustar os testes, Mestre Suprema Jedi.`
- Identidade não disponível ou não confirmada: `Vou ajustar os testes.`

## Regras Práticas

- Decidir o tratamento antes de redigir a resposta, não no meio dela.
- Manter consistência do tratamento do início ao fim da mensagem.
- Reavaliar somente quando a plataforma disponibilizar identidade de sessão nova ou atualizada.
