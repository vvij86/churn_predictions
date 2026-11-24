We are facing a cluster-level library/classpath issue on:

"mer_wealth_dev_mra_ml_shared_cluster"

The cluster is running Databricks Runtime 18.x with Scala 2.13, but it also has MongoDB libraries compiled for the older Scala 2.12 version.

Conflicting libraries currently include:

- "org.mongodb.spark:mongo-spark-connector_2.12:3.0.1"
- "/Volumes/wealthdev/mer_common/packages/mongo-scala-driver_2.12-4.1.2.jar"
- "/Volumes/wealthdev/mer_common/packages/mongo-scala-bson_2.12-4.1.2.jar"

The cluster also has a Scala 2.13 Mongo Spark connector:

- "/Volumes/wealthdev/mer_common/packages/mongo-spark-connector_2.13-10.4.0.jar"

When Spark initializes or scans datasource providers, the older Scala 2.12 Mongo connector is being loaded and fails with errors such as:

"NoClassDefFoundError: scala/Serializable"

and references to:

"com.mongodb.spark.sql.DefaultSource"

Because Spark scans datasource providers globally, this impacts unrelated Spark SQL / Delta operations as well. Even a simple Delta "CREATE TABLE" operation fails on this ML cluster.

We validated that:

- Scala version on the cluster is "2.13.16"
- Spark version is "4.1.0"
- the target Unity Catalog schema is writable
- the same Delta table write succeeds through Serverless / SQL Warehouse

Requested fix:

Please review the MongoDB libraries on this cluster and remove the incompatible Scala 2.12 Mongo Spark connector / Mongo Scala JARs, while retaining only the Mongo libraries compatible with Scala 2.13 and the current Databricks Runtime.

After the library cleanup, please restart the cluster so the classpath is reloaded.

This issue is currently blocking persistence of Member Retention Analytics ML feature and ground-truth Delta tables.
