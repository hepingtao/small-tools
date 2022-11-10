SELECT RTRIM(t1.TABSCHEMA)||'.'||RTRIM(t1.TABNAME)       TabName,
       t1.REMARKS                                        TabDesc,
       t1.TYPE                                           TabType,
       to_char(t1.CREATE_TIME,'YYYY-MM-DD HH24:MI:SS')   CreateDate
  FROM SYSCAT.TABLES t1
 WHERE 1 = 1
   AND t1.TABNAME like upper('%' || '$TabName' || '%')
   AND (t1.TABSCHEMA = upper('$TabSchema') or '$TabSchema' = 'TabSchema')
 ORDER BY TabName
with ur
