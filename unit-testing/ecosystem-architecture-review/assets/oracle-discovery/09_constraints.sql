SELECT owner,table_name,constraint_name,constraint_type,status,validated,search_condition_vc FROM all_constraints WHERE owner=UPPER('&OWNER') ORDER BY table_name,constraint_type,constraint_name;
