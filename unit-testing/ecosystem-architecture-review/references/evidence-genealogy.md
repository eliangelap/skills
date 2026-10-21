# Evidencia, genealogia e confianca

## Registro padrao de achado

```text
ID: ARC-017
Classificacao: CONFIRMADO | INFERIDO | HIPOTESE | RISCO | RECOMENDACAO
Confianca: alta | media | baixa
Achado: <afirmacao atomica>
Evidencias:
- <arquivo:symbol/linha ou artefato>
Relacionados: <IDs>
Impacto: baixo | medio | alto | critico
Observacao: <limites>
```

## Regras
- `CONFIRMADO`: evidencia direta e suficiente.
- `INFERIDO`: varias evidencias coerentes, mas elo nao comprovado diretamente.
- `HIPOTESE`: explicacao plausivel que requer validacao.
- `RISCO`: condicao observada + impacto potencial; separar probabilidade de fato.
- `RECOMENDACAO`: proposta; nunca descrever como estado atual.

## Genealogia top-down
`Capability -> Processo -> Funcionalidade -> Caso de uso -> Tela -> Handler/Hook/Service -> Endpoint -> Middleware -> Uniface Component/Operation -> Entity -> Tabela -> Coluna`

## Genealogia bottom-up
`Tabela/Coluna -> Entity -> Operation -> Middleware -> Endpoint -> Consumer -> Tela -> Funcionalidade -> Processo/Capability`

## Blast radius
Para cada mudanca relevante, listar dependencias diretas, transitivas comprovadas, consumidores, dados e funcionalidades potencialmente afetadas. Nao tratar dependencia potencial como impacto certo.

## Contradicoes
Quando duas leituras conflitarem, criar `CONTRADICTION-*`, listar as evidencias de cada lado e deixar aberto ate resolucao. O Review Board decide se rebaixa a confianca.
