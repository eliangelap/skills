SELECT owner, table_name, column_id, column_name, data_type, data_length, data_precision, data_scale, nullable FROM all_tab_columns WHERE owner = UPPER('&OWNER') ORDER BY table_name, column_id;
