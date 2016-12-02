SELECT t1.owner||'.'||t1.table_name                      TabName,
       t2.comments                                       TabDesc,
       t1.object_type                                    TabType,
       to_char(t1.last_ddl_time,'YYYY-MM-DD HH24:MI:SS') CreateDate
  --FROM sys.All_All_Tables                             t1
  FROM (select OWNER, OBJECT_NAME table_name, object_type, last_ddl_time
          from sys.DBA_Objects
         where 1 = 1
           and object_type in ('TABLE','VIEW','INDEX')
       ) t1
       --LEFT JOIN sys.All_Tab_Comments                 t2
       LEFT JOIN sys.DBA_Tab_Comments                 t2
                 ON  t1.owner = t2.owner
                 AND t1.table_name = t2.table_name
       --LEFT JOIN sys.All_Objects                      t3
       --LEFT JOIN sys.DBA_Objects                      t3
       --          ON  t1.owner = t3.owner
       --          AND t1.table_name = t3.object_name
 WHERE 1 = 1
   AND t1.table_name like upper('%' || '$TabName' || '%')
   AND (t1.owner = upper('$TabSchema') or '$TabSchema' = 'TabSchema')
 ORDER BY TabName
