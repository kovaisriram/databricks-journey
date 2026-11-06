# Databricks notebook source
# MAGIC %md
# MAGIC # 00 · Setup — Get Started with Databricks for Data Engineering (Free Edition lab)
# MAGIC
# MAGIC Creates a schema and a Volume, then lands "raw" source files that simulate data arriving from an operational system.
# MAGIC
# MAGIC * Catalog: `learn` (change `CATALOG` below if yours is different)
# MAGIC * Schema: `get_started`
# MAGIC * Raw files: `/Volumes/learn/get_started/raw/`
# MAGIC
# MAGIC Run this notebook **once**. Use `05_land_new_batch` later to simulate new data arriving.

# COMMAND ----------

CATALOG = "learn"
SCHEMA = "get_started"
RAW = f"/Volumes/{CATALOG}/{SCHEMA}/raw"

spark.sql(f"CREATE SCHEMA IF NOT EXISTS {CATALOG}.{SCHEMA}")
spark.sql(f"CREATE VOLUME IF NOT EXISTS {CATALOG}.{SCHEMA}.raw")
print(f"Ready: {CATALOG}.{SCHEMA} and {RAW}")

# COMMAND ----------

# MAGIC %md
# MAGIC ## Land three batches of orders as JSON files
# MAGIC Batch 2 deliberately contains 50 duplicate orders from batch 1, so the silver layer has something to clean.

# COMMAND ----------

orders = spark.table("samples.tpch.orders")

def year_slice(year, n):
    return orders.filter(f"year(o_orderdate) = {year}").orderBy("o_orderkey").limit(n)

batches = {1: year_slice(1995, 2000), 2: year_slice(1996, 2000), 3: year_slice(1997, 2000)}

for n, df in batches.items():
    df.write.mode("overwrite").json(f"{RAW}/orders/batch_{n}")

year_slice(1995, 50).write.mode("append").json(f"{RAW}/orders/batch_2")

display(dbutils.fs.ls(f"{RAW}/orders"))

# COMMAND ----------

# MAGIC %md
# MAGIC ## Land the matching customers as CSV

# COMMAND ----------

order_customers = batches[1].unionByName(batches[2]).unionByName(batches[3]).select("o_custkey").distinct()
customers = spark.table("samples.tpch.customer").join(
    order_customers, spark.table("samples.tpch.customer").c_custkey == order_customers.o_custkey, "left_semi"
)
customers.write.mode("overwrite").option("header", True).csv(f"{RAW}/customers")

display(dbutils.fs.ls(f"{RAW}/customers"))
