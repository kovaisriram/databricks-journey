# Databricks notebook source
# MAGIC %md
# MAGIC # 04 · Gold — business-ready tables
# MAGIC Aggregates the business will query directly from dashboards and Genie.

# COMMAND ----------

# MAGIC %sql
# MAGIC USE CATALOG learn;
# MAGIC USE SCHEMA get_started;
# MAGIC
# MAGIC CREATE OR REPLACE TABLE gold_monthly_revenue AS
# MAGIC SELECT
# MAGIC   DATE_TRUNC('MONTH', order_date) AS order_month,
# MAGIC   order_priority,
# MAGIC   COUNT(*)         AS orders,
# MAGIC   SUM(total_price) AS revenue
# MAGIC FROM silver_orders
# MAGIC GROUP BY ALL;

# COMMAND ----------

# MAGIC %sql
# MAGIC CREATE OR REPLACE TABLE gold_revenue_by_segment AS
# MAGIC SELECT
# MAGIC   c.market_segment,
# MAGIC   n.n_name              AS nation,
# MAGIC   COUNT(DISTINCT o.customer_id) AS customers,
# MAGIC   COUNT(*)              AS orders,
# MAGIC   SUM(o.total_price)    AS revenue
# MAGIC FROM silver_orders o
# MAGIC JOIN silver_customers c ON o.customer_id = c.customer_id
# MAGIC JOIN samples.tpch.nation n ON c.nation_key = n.n_nationkey
# MAGIC GROUP BY ALL;

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT market_segment, SUM(revenue) AS revenue
# MAGIC FROM gold_revenue_by_segment
# MAGIC GROUP BY market_segment
# MAGIC ORDER BY revenue DESC;

# COMMAND ----------

# MAGIC %md
# MAGIC **Look at lineage:** open **Catalog → learn → get_started → gold_revenue_by_segment → Lineage**. You should see it trace back through silver to bronze and the raw Volume.
