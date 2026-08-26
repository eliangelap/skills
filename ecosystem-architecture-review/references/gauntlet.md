# Gauntlet arquitetural

Executar papeis em ordem. Um papel pode revisar artefatos anteriores, mas deve registrar contradicoes em vez de silenciosamente reescrever fatos.

0. Evidence & Repository Mapper - inventario e Evidence Index.
1. Code Archaeologist - descobrir implementacao real sem recomendar.
2. Solution Architect - C4, boundaries e responsabilidades.
3. Integration Architect - App/API/Middleware/Uniface/externos.
4. Uniface/Legacy Specialist - Operations, Components, Entities, triggers e legado.
5. Data Architect - modelos, ownership e lineage.
6. Security/Performance/Observability Reviewer - riscos transversais.
7. Product/Functional Analyst - capabilities, processos e mapa funcional.
8. Modernization Architect - somente apos AS-IS: alternativas, TO-BE e roadmap.
9. Architecture Review Board - contestar, exigir evidencia e resolver/rebaixar contradicoes.
10. Chief Architect - sintetizar sem novas descobertas.

## Gate AS-IS
Nao permitir o passo 8 antes de existir inventario, C4 preliminar, mapa de integracoes, Uniface/data quando aplicavel, genealogia dos fluxos criticos e lista de lacunas.

## Gate final
A sintese deve informar cobertura, repositorios analisados, itens ignorados, lacunas, contradicoes abertas e dependencias de validacao externa.
