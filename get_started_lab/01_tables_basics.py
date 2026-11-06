# Databricks notebook source
# MAGIC %md
# MAGIC # 01 · Working with tables (Delta Lake basics)
# MAGIC Create, change, inspect and time-travel a managed Delta table.

# COMMAND ----------

# MAGIC %sql
# MAGIC USE CATALOG learn;
# MAGIC USE SCHEMA get_started;
# MAGIC
# MAGIC CREATE OR REPLACE TABLE demo_products (
# MAGIC   product_id INT,
# MAGIC   product_name STRING,
# MAGIC   price DECIMAL(10,2)
# MAGIC );
# MAGIC
# MAGIC INSERT INTO demo_products VALUES
# MAGIC   (1, 'Laptop stand', 49.99),
# MAGIC   (2, 'USB-C hub', 29.50),
# MAGIC   (3, 'Desk lamp', 35.00);
# MAGIC
# MAGIC SELECT * FROM demo_products;

# COMMAND ----------

# MAGIC %sql
# MAGIC UPDATE demo_products SET price = 44.99 WHERE product_id = 1;
# MAGIC DELETE FROM demo_products WHERE product_id = 3;
# MAGIC SELECT * FROM demo_products;

# COMMAND ----------

# MAGIC %md
# MAGIC ## Every change is a version in the transaction log

# COMMAND ----------

# MAGIC %sql
# MAGIC DESCRIBE HISTORY demo_products;

# COMMAND ----------

# MAGIC %sql
# MAGIC -- Time travel: the table as it was right after the INSERT
# MAGIC SELECT * FROM demo_products VERSION AS OF 1;

# COMMAND ----------

# MAGIC %sql
# MAGIC -- Undo the UPDATE and DELETE
# MAGIC RESTORE TABLE demo_products TO VERSION AS OF 1;
# MAGIC SELECT * FROM demo_products;

# COMMAND ----------

# MAGIC %sql
# MAGIC -- Where and how the table is stored (format, location, size, managed vs external)
# MAGIC DESCRIBE DETAIL demo_products;

# COMMAND ----------

# MAGIC %md
# MAGIC **Try it yourself:** add a column with `ALTER TABLE demo_products ADD COLUMN category STRING`, fill it with an `UPDATE`, then check `DESCRIBE HISTORY` again.
