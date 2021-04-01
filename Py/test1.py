q = """
RESTORE DATABASE REPLACE_ME
  FROM DISK = 'C:\Program Files\Microsoft SQL Server\MSSQL12.MSSQLSERVER\MSSQL\Backup\REPLACE_ME.bak'
	WITH 
		MOVE 'hammerdb_2019_1' TO 'C:\Program Files\Microsoft SQL Server\MSSQL12.MSSQLSERVER\MSSQL\DATA\REPLACE_ME.mdf',
		MOVE 'hammerdb_2019_1_Log' TO 'D:\logs\REPLACE_ME_log.mdf'
GO

ALTER DATABASE REPLACE_ME SET RECOVERY FULL ;

"""

for i in range(1,17):
    sql = q.replace("REPLACE_ME", "hammerdb_2014_{}".format(i))
    print(sql)