# Databricks notebook source
# MAGIC %md
# MAGIC # Project setup
# MAGIC
# MAGIC Run this notebook once to create your project's catalog, medallion schemas, and a landing Volume for raw files.
# MAGIC
# MAGIC Every statement uses `IF NOT EXISTS`, so re-running it is safe. Unlike our lesson notebooks, this one never drops anything: your project catalog holds a semester of work.

# COMMAND ----------

CATALOG = "final_project"

spark.sql(f"CREATE CATALOG IF NOT EXISTS {CATALOG}")
for schema in ["bronze", "silver", "gold"]:
    spark.sql(f"CREATE SCHEMA IF NOT EXISTS {CATALOG}.{schema}")

spark.sql(f"CREATE VOLUME IF NOT EXISTS {CATALOG}.bronze.landing")

print(f"Catalog : {CATALOG}")
print(f"Landing : /Volumes/{CATALOG}/bronze/landing")

# COMMAND ----------

# MAGIC %md
# MAGIC ## Check your secrets
# MAGIC
# MAGIC List the secret keys in your `dat342` scope. Only key names are shown, never values. Every credential your project uses should appear here before you write any Bronze code that needs it.

# COMMAND ----------

for s in dbutils.secrets.list("dat342"):
    print(s.key)
