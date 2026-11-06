# Databricks notebook source
# MAGIC %md
# MAGIC # 03 · Silver — clean, type, de-duplicate
# MAGIC * Rename columns to business-friendly names and cast to proper types.
# MAGIC * Remove the duplicate orders planted in batch 2.
# MAGIC * Load incrementally with `MERGE` (an upsert), the workhorse of warehouse loading.

# COMMAND ----------

# MAGIC %sql
# MAGIC USE CATALOG learn;
# MAGIC USE SCHEMA get_started;
# MAGIC
# MAGIC CREATE TABLE IF NOT EXISTS silver_orders (
# MAGIC   order_id BIGINT,
# MAGIC   customer_id BIGINT,
# MAGIC   order_status STRING,
# MAGIC   total_price DECIMAL(12,2),
# MAGIC   order_date DATE,
# MAGIC   order_priority STRING,
# MAGIC   ingested_at TIMESTAMP
# MAGIC );
# MAGIC
# MAGIC MERGE INTO silver_orders AS t
# MAGIC USING (
# MAGIC   SELECT
# MAGIC     CAST(o_orderkey AS BIGINT)          AS order_id,
# MAGIC     CAST(o_custkey AS BIGINT)           AS customer_id,
# MAGIC     o_orderstatus                       AS order_status,
# MAGIC     CAST(o_totalprice AS DECIMAL(12,2)) AS total_price,
# MAGIC     CAST(o_orderdate AS DATE)           AS order_date,
# MAGIC     o_orderpriority                     AS order_priority,
# MAGIC     ingested_at
# MAGIC   FROM bronze_orders
# MAGIC   WHERE o_totalprice > 0
# MAGIC   QUALIFY ROW_NUMBER() OVER (PARTITION BY o_orderkey ORDER BY ingested_at DESC, source_file DESC) = 1
# MAGIC ) AS s
# MAGIC ON t.order_id = s.order_id
# MAGIC WHEN MATCHED THEN UPDATE SET *
# MAGIC WHEN NOT MATCHED THEN INSERT *;

# COMMAND ----------

# MAGIC %sql
# MAGIC -- Bronze has duplicates; silver should not.
# MAGIC SELECT
# MAGIC   (SELECT COUNT(*) FROM bronze_orders) AS bronze_rows,
# MAGIC   (SELECT COUNT(*) FROM silver_orders) AS silver_rows,
# MAGIC   (SELECT COUNT(*) - COUNT(DISTINCT order_id) FROM silver_orders) AS duplicates_left_in_silver;

# COMMAND ----------

# MAGIC %sql
# MAGIC CREATE OR REPLACE TABLE silver_customers AS
# MAGIC SELECT
# MAGIC   CAST(c_custkey AS BIGINT)        AS customer_id,
# MAGIC   c_name                           AS customer_name,
# MAGIC   c_mktsegment                     AS market_segment,
# MAGIC   CAST(c_acctbal AS DECIMAL(12,2)) AS account_balance,
# MAGIC   CAST(c_nationkey AS INT)         AS nation_key
# MAGIC FROM bronze_customers;
# MAGIC
# MAGIC SELECT * FROM silver_customers LIMIT 10;
