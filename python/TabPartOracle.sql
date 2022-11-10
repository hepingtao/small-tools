SELECT t1.OWNER||'.'||t1.TABLE_NAME TabName,
       t5.column_name               PartCol,
       t2.partitioning_type         PartType,
       to_char(t2.partition_count)  PartCnt,
       t6.partition_name            PartName,
       t6.high_value                HighValue
FROM SYS.ALL_ALL_TABLES                           t1
     LEFT JOIN sys.All_Part_Tables                t2
               ON  t1.owner = t2.owner
               AND t1.table_name = t2.table_name
     LEFT JOIN sys.all_part_key_columns           t5
               ON  t1.owner = t5.owner
               AND t1.table_name = t5.name
     LEFT JOIN sys.all_tab_partitions             t6
               ON  t1.owner = t6.table_owner
               AND t1.table_name = t6.table_name
 WHERE 1 = 1
   and t1.table_name = upper('$TabName')
   and (t1.owner = upper('$TabSchema') or '$TabSchema' = 'TabSchema')
 ORDER BY t6.partition_name
