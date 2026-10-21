SELECT owner, table_name, tablespace_name FROM all_tables WHERE owner = UPPER('&OWNER') ORDER BY table_name;
