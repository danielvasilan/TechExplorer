CREATE TEMP FUNCTION MakePartitionByExpression(
  column_name STRING, data_type STRING
) AS (
  IF(
    column_name = '_PARTITIONTIME',
    'DATE(_PARTITIONTIME)',
    IF(
      data_type = 'TIMESTAMP',
      CONCAT('DATE(', column_name, ')'),
      column_name
    )
  )
);

CREATE TEMP FUNCTION MakePartitionByClause(
  columns ARRAY<STRUCT<column_name STRING, data_type STRING, is_nullable STRING,  is_partitioning_column STRING, clustering_ordinal_position INT64>>
) AS (
  IFNULL(
    CONCAT(
      'PARTITION BY ',
      (SELECT MakePartitionByExpression(column_name, data_type)
       FROM UNNEST(columns) WHERE is_partitioning_column = 'YES'),
      '\n'),
    ''
  )
);

CREATE TEMP FUNCTION MakeClusterByClause(
  columns ARRAY<STRUCT<column_name STRING, data_type STRING, is_nullable STRING,  is_partitioning_column STRING, clustering_ordinal_position INT64>>
) AS (
  IFNULL(
    CONCAT(
      'CLUSTER BY ',
      (SELECT STRING_AGG(column_name, ', ' ORDER BY clustering_ordinal_position)
        FROM UNNEST(columns) WHERE clustering_ordinal_position IS NOT NULL),
      '\n'
    ),
    ''
  )
);

CREATE TEMP FUNCTION MakeNullable(data_type STRING, is_nullable STRING)
AS (
  IF(not STARTS_WITH(data_type, 'ARRAY<') and is_nullable = 'NO', ' NOT NULL', '')
);

CREATE TEMP FUNCTION MakeColumnList(
  columns ARRAY<STRUCT<column_name STRING, data_type STRING, is_nullable STRING,  is_partitioning_column STRING, clustering_ordinal_position INT64>>
) AS (
  IFNULL(
    CONCAT(
      '(\n',
      (SELECT STRING_AGG(CONCAT('  ', column_name, ' ', data_type,  MakeNullable(data_type, is_nullable)), ',\n')
       FROM UNNEST(columns)),
      '\n)\n'
    ),
    ''
  )
);

CREATE TEMP FUNCTION MakeOptionList(
  options ARRAY<STRUCT<option_name STRING, option_value STRING>>
) AS (
  IFNULL(
    CONCAT(
      'OPTIONS (\n',
      (SELECT STRING_AGG(CONCAT('  ', option_name, '=', option_value), ',\n') FROM UNNEST(options)),
      '\n)\n'),
    ''
  )
);

WITH Components AS (
  SELECT
    CONCAT('`', table_catalog, '.', table_schema, '.', table_name, '`') AS table_name,
    ARRAY_AGG(
      STRUCT(column_name, data_type, is_nullable, is_partitioning_column, clustering_ordinal_position)
      ORDER BY ordinal_position
    ) AS columns,
    (SELECT ARRAY_AGG(STRUCT(option_name, option_value))
     FROM bl_edw.INFORMATION_SCHEMA.TABLE_OPTIONS AS t2
     WHERE t.table_name = t2.table_name) AS options
  FROM bl_edw.INFORMATION_SCHEMA.TABLES AS t
  LEFT JOIN bl_edw.INFORMATION_SCHEMA.COLUMNS
  USING (table_catalog, table_schema, table_name)
  WHERE table_type = 'BASE TABLE'
  GROUP BY table_catalog, table_schema, t.table_name
)
SELECT
  CONCAT(
    'CREATE OR REPLACE TABLE ',
    table_name,
    '\n',
    MakeColumnList(columns),
    MakePartitionByClause(columns),
    MakeClusterByClause(columns),
    MakeOptionList(options))
FROM Components

