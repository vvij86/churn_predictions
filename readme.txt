We are facing a cluster-level library/classpath issue on:

"mer_wealth_dev_mra_ml_shared_cluster"

The cluster is running with:

- Scala "2.13.16"
- Spark "4.1.0"

However, the cluster currently has MongoDB libraries compiled for both Scala 2.12 and Scala 2.13.

The following Scala 2.12 Mongo libraries are installed and appear to be incompatible with the current Scala 2.13 runtime:

- "org.mongodb.spark:mongo-spark-connector_2.12:3.0.1"
- "/Volumes/wealthdev/mer_common/packages/mongo-scala-driver_2.12-4.1.2.jar"
- "/Volumes/wealthdev/mer_common/packages/mongo-scala-bson_2.12-4.1.2.jar"

The cluster also has the Scala 2.13 Mongo connector:

- "/Volumes/wealthdev/mer_common/packages/mongo-spark-connector_2.13-10.4.0.jar"

When Spark initializes/scans datasource providers, the older Scala 2.12 Mongo connector is being loaded and fails with errors such as:

"NoClassDefFoundError: scala/Serializable"

and:

"com.mongodb.spark.sql.DefaultSource"

Because Spark scans datasource providers globally, this is also impacting unrelated Delta/Spark SQL operations. Even a very small Delta "CREATE TABLE" test fails on this shared ML cluster.

We validated that:

- the Unity Catalog schema "mer_wealth_dev.mer_wealth_mra_mlops" is writable
- the same Delta write succeeds through Serverless / SQL Warehouse
- the issue is isolated to this ML cluster configuration rather than schema permissions or ML feature logic

Requested action:

Please uninstall/remove the following Scala 2.12 Mongo libraries from "mer_wealth_dev_mra_ml_shared_cluster":

- "org.mongodb.spark:mongo-spark-connector_2.12:3.0.1"
- "/Volumes/wealthdev/mer_common/packages/mongo-scala-driver_2.12-4.1.2.jar"
- "/Volumes/wealthdev/mer_common/packages/mongo-scala-bson_2.12-4.1.2.jar"

Please retain the Scala 2.13-compatible Mongo connector:

"/Volumes/wealthdev/mer_common/packages/mongo-spark-connector_2.13-10.4.0.jar"

After the library cleanup, please restart the cluster so the classpath is fully reloaded and confirm once completed.

This issue is currently blocking persistence of the Member Retention Analytics ML feature and ground-truth Delta tables.
