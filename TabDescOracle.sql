SELECT t1.OWNER||'.'||t1.TABLE_NAME TableName,
       t7.COMMENTS TabComments,
       t2.COLUMN_ID ColID,
       t2.COLUMN_NAME ColName,
       CASE t2.DATA_TYPE
            WHEN 'VARCHAR2' THEN t2.DATA_TYPE||'('||t2.DATA_LENGTH||')'
            WHEN 'NUMBER' THEN CASE WHEN t2.DATA_PRECISION IS NULL THEN t2.DATA_TYPE
                                    WHEN t2.DATA_SCALE = 0 THEN t2.DATA_TYPE||'('||t2.DATA_PRECISION||')'
                                    WHEN t2.DATA_SCALE > 0 THEN t2.DATA_TYPE||'('||t2.DATA_PRECISION||','||t2.DATA_SCALE||')'
                                    ELSE t2.DATA_TYPE END
            ELSE t2.DATA_TYPE END DataType,
       t2.NULLABLE Nullable,
       t5.COMMENTS ColComments,
       t3.COLUMN_NAME KeyCol,
       t6.column_name PartCol
  FROM 
       --SYS.ALL_ALL_TABLES                             t1
       (select OWNER, OBJECT_NAME table_name, object_type, last_ddl_time
          from sys.ALL_Objects
         where 1 = 1
           and object_type in ('TABLE','VIEW','INDEX')
       ) t1
       LEFT JOIN SYS.ALL_TAB_COLS                     t2
                 ON  t1.OWNER = t2.owner
                 AND t1.TABLE_NAME = t2.TABLE_NAME
                 AND t2.COLUMN_ID IS NOT NULL
       LEFT JOIN SYS.ALL_CONS_COLUMNS                 t3
                 ON  t1.owner = t3.OWNER
                 AND t1.table_name = t3.TABLE_NAME
                 AND t2.COLUMN_NAME = t3.COLUMN_NAME
                 AND T3.POSITION IS NOT NULL
       LEFT JOIN SYS.ALL_CONSTRAINTS                  t4
                 ON  t1.owner = t4.OWNER
                 AND t1.table_name = t4.TABLE_NAME
                 AND t4.CONSTRAINT_TYPE = 'P'
       LEFT JOIN sys.All_Col_Comments                 t5
                 ON  t1.owner = t5.OWNER
                 AND t1.table_name = t5.TABLE_NAME
                 AND t2.COLUMN_NAME = t5.COLUMN_NAME
       LEFT JOIN sys.all_part_key_columns             t6
                 ON  t1.owner = t6.OWNER
                 AND t1.table_name = t6.name
                 AND t2.COLUMN_NAME = t6.column_name
       LEFT JOIN sys.All_Tab_Comments                 t7
                 ON  t1.owner = t7.OWNER
                 AND t1.table_name = t7.TABLE_NAME
 WHERE 1 = 1
   and t1.table_name = upper('$TabName')
   and (t1.owner = upper('$TabSchema') or '$TabSchema' = 'TabSchema')
   --AND t1.owner IN ('STAGE','ODS','EDS','DM','REF')
 ORDER BY t2.COLUMN_ID
