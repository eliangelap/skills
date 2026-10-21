SELECT owner,name,type,referenced_owner,referenced_name,referenced_type FROM all_dependencies WHERE owner=UPPER('&OWNER') ORDER BY name,type,referenced_owner,referenced_name;
