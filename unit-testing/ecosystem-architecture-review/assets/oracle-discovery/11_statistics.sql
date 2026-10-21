SELECT owner,table_name,num_rows,blocks,avg_row_len,last_analyzed FROM all_tables WHERE owner=UPPER('&OWNER') ORDER BY table_name;
