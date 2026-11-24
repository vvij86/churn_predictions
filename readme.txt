# Scala version
scala_version = spark._jvm.scala.util.Properties.versionNumberString()
print("Scala version:", scala_version)

# Spark version
print("Spark version:", spark.version)
