-- Opcional e dependente de privilegios/semantica. Use somente apos revisar quais colunas de data representam atividade real.
-- Nao execute MAX() em todas as tabelas automaticamente em producao. Primeiro derive candidatos pelo catalogo:
SELECT owner,table_name,column_name,data_type FROM all_tab_columns WHERE owner=UPPER('&OWNER') AND data_type IN ('DATE','TIMESTAMP','TIMESTAMP(6)') ORDER BY table_name,column_id;
