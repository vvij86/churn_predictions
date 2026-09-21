SELECT 
    SCHEMA_NAME(schema_id) AS SchemaName,
    COUNT(*) AS TableCount
FROM sys.tables
GROUP BY schema_id
ORDER BY SchemaName;
