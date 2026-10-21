SELECT owner,view_name,text_length FROM all_views WHERE owner=UPPER('&OWNER') ORDER BY view_name;
