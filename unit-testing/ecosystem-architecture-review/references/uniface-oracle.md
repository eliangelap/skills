# Analise Uniface e Oracle

## Uniface
Inventariar Components, Component Templates quando visiveis, Operations, Entries, Entities, fields, triggers, includes, services, activates/calls, retrieve/store/commit/discard, error handling e acesso a dados.

Rastrear chamadas entre componentes e entre middleware/backend e Uniface. Diferenciar regra de negocio, orquestracao, apresentacao e persistencia. Nao assumir semantica apenas pelo nome do componente.

## Oracle
Primeiro extrair tabelas e objetos referenciados no codigo. Quando houver acesso apenas ao codigo, marcar modelo fisico como parcial.

Usar o Database Discovery Pack para confirmar:
- tabelas/colunas/tipos;
- PK/FK;
- indices;
- views;
- sequences;
- triggers;
- constraints;
- dependencias.

Scripts de atividade/estatistica podem ser pesados ou depender de privilegios. Informar isso antes da execucao. Nunca solicitar escrita em producao para discovery; preferir consultas de metadados/read-only.

## Segunda passagem
Apos receber resultados Oracle, reconciliar:
1. referencias no codigo;
2. Entities Uniface;
3. objetos reais do catalogo;
4. relacionamentos reais;
5. divergencias e objetos sem uso identificado.
