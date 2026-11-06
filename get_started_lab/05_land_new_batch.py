# Databricks notebook source
# MAGIC %md
# MAGIC # 05 · Simulate new data arriving
# MAGIC Lands batch 4 (1998 orders). Then re-run your job (or notebooks 02 → 03 → 04) and watch only the new files load.

# COMMAND ----------

RAW = "/Volumes/learn/get_started/raw"

new_orders = (spark.table("samples.tpch.orders")
              .filter("year(o_orderdate) = 1998")
              .orderBy("o_orderkey")
              .limit(2000))
new_orders.write.mode("overwrite").json(f"{RAW}/orders/batch_4")

new_customers = spark.table("samples.tpch.customer").join(
    new_orders.select("o_custkey").distinct(),
    spark.table("samples.tpch.customer").c_custkey == new_orders.o_custkey,
    "left_semi",
)
new_customers.write.mode("append").option("header", True).csv(f"{RAW}/customers")

display(dbutils.fs.ls(f"{RAW}/orders"))
