# Databricks notebook source
# MAGIC %md
# MAGIC # 02 · Bronze — ingest raw files into Delta
# MAGIC * Orders (JSON) with `COPY INTO`: incremental and idempotent — re-running loads only new files.
# MAGIC * Customers (CSV) with `read_files`.
# MAGIC
# MAGIC Bronze keeps data close to the source and adds lineage columns: which file, when loaded.

# COMMAND ----------

# MAGIC %sql
# MAGIC USE CATALOG learn;
# MAGIC USE SCHEMA get_started;
# MAGIC
# MAGIC CREATE TABLE IF NOT EXISTS bronze_orders;
# MAGIC
# MAGIC COPY INTO bronze_orders
# MAGIC FROM (
# MAGIC   SELECT *, _metadata.file_path AS source_file, current_timestamp() AS ingested_at
# MAGIC   FROM '/Volumes/learn/get_started/raw/orders'
# MAGIC )
# MAGIC FILEFORMAT = JSON
# MAGIC PATTERN = 'batch_*/part-*'
# MAGIC COPY_OPTIONS ('mergeSchema' = 'true');

# COMMAND ----------

# MAGIC %sql
# MAGIC -- Run the COPY INTO cell again: num_inserted_rows will be 0, because loaded files are skipped.
# MAGIC SELECT source_file, COUNT(*) AS row_count
# MAGIC FROM bronze_orders
# MAGIC GROUP BY source_file
# MAGIC ORDER BY source_file;

# COMMAND ----------

# MAGIC %sql
# MAGIC CREATE OR REPLACE TABLE bronze_customers AS
# MAGIC SELECT *, _metadata.file_path AS source_file, current_timestamp() AS ingested_at
# MAGIC FROM read_files(
# MAGIC   '/Volumes/learn/get_started/raw/customers',
# MAGIC   format => 'csv',
# MAGIC   header => true
# MAGIC );
# MAGIC
# MAGIC SELECT COUNT(*) AS customers FROM bronze_customers;
