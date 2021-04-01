
#### History
Initially developed by Facebook, took up by Apache Software Foundation as open source Apache Hive.  
Distributed data warehouse infra on top of Hadoop HDFS, making querying and analyzing structured data easy.


#### Architecture

![Hive Architecture](media/hive-architecture.jpg)

#### HiveQL (HQL)

#### Table types
##### External 
- not managed by Hive
- just metadata - delete doesn't delete data files
##### Internal (managed)
- can be TRUNCATED
- data moved inside user/warehouse location
- when table is deleted, also data is lost
- support ACID
- query result caching

#### Metastore
Types
- Embedded in the sme JVM using Derby db (single instance)
- Local - the metastore service is still local, but the DB can be remote or on another JVM
- Remote - Thrift access to remote metastore server

Can use MSSQL, Oracle, Mysql, Postgres, Derby

#### Data Model
![Hive Architecture](media/hive-data-model.jpg)
