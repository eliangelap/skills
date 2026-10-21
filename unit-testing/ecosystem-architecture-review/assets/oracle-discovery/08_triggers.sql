SELECT owner,trigger_name,trigger_type,triggering_event,table_owner,table_name,status FROM all_triggers WHERE owner=UPPER('&OWNER') ORDER BY table_name,trigger_name;
