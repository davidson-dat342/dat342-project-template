"""Create the final_project catalog, its medallion schemas, and a landing Volume.

Safe to re-run: every statement uses IF NOT EXISTS, and nothing is ever dropped,
because this catalog holds a semester of work.
"""

from pyspark.sql import SparkSession

CATALOG = "final_project"
SCHEMAS = ["bronze", "silver", "gold"]
SECRET_SCOPE = "dat342"


def create_catalog(spark: SparkSession) -> None:
    spark.sql(f"CREATE CATALOG IF NOT EXISTS {CATALOG}")
    for schema in SCHEMAS:
        spark.sql(f"CREATE SCHEMA IF NOT EXISTS {CATALOG}.{schema}")
    spark.sql(f"CREATE VOLUME IF NOT EXISTS {CATALOG}.bronze.landing")
    print(f"Catalog : {CATALOG} ({', '.join(SCHEMAS)})")
    print(f"Landing : /Volumes/{CATALOG}/bronze/landing")


def list_secret_keys() -> None:
    # Shows key names only, never values. Every credential your project uses
    # should be listed here before you write code that needs it.
    from databricks.sdk.runtime import dbutils

    keys = [s.key for s in dbutils.secrets.list(SECRET_SCOPE)]
    print(f"Secrets in '{SECRET_SCOPE}': {', '.join(keys) or '(none)'}")


if __name__ == "__main__":
    spark = SparkSession.builder.getOrCreate()
    create_catalog(spark)
    list_secret_keys()
