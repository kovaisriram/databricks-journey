# Get Started with Databricks for Data Engineering — Free Edition lab

A hands-on companion to the Databricks Academy course, built for Databricks Free Edition.
It uses the built-in `samples.tpch` data instead of the course's private lab datasets.

| Course topic | Lab notebook |
| --- | --- |
| Creating and working with tables | `01_tables_basics` |
| Ingesting data into Delta Lake | `02_bronze_ingest` |
| Transforming through the medallion architecture | `03_silver_transform`, `04_gold_aggregate` |
| Orchestrating with Lakeflow Jobs (Workflows) | Step 5 below + `05_land_new_batch` |
| Lakeflow Spark Declarative Pipelines | `06_declarative_pipeline.sql` |
| Databricks SQL and Unity Catalog | Step 7 below |

Assumes your catalog is `learn`. If it is different, find and replace `learn` in every file.

## Steps

1. **Setup** — run `00_setup` once. It creates `learn.get_started`, a `raw` Volume, and lands 3 batches of order files (JSON) plus customers (CSV).
2. **Tables** — run `01_tables_basics` cell by cell. Watch `DESCRIBE HISTORY` after each change.
3. **Bronze** — run `02_bronze_ingest`. Then run the `COPY INTO` cell a second time and note that 0 rows load.
4. **Silver and gold** — run `03_silver_transform`, then `04_gold_aggregate`. Check that duplicates are gone in silver, then open the Lineage tab on a gold table.
5. **Orchestrate with a job**
   1. Go to **Jobs & Pipelines → Create → Job**. Name it `get_started_medallion`.
   2. Task 1 `bronze`: type Notebook, path `02_bronze_ingest`, compute Serverless.
   3. Task 2 `silver`: notebook `03_silver_transform`, depends on `bronze`.
   4. Task 3 `gold`: notebook `04_gold_aggregate`, depends on `silver`.
   5. Click **Run now** and watch the task graph.
   6. Run `05_land_new_batch`, then run the job again. Bronze grows only by batch 4.
   7. Optional: add a **file arrival trigger** on `/Volumes/learn/get_started/raw/orders/`.
6. **Declarative pipeline**
   1. **Jobs & Pipelines → Create → ETL pipeline**. Default catalog `learn`, default schema `get_started_sdp`.
   2. Replace the sample code with the contents of `06_declarative_pipeline.sql`.
   3. Click **Run pipeline**. Explore the graph and the data-quality metrics for each expectation.
   4. Note: this version does not remove the batch 2 duplicates. You will fix that with `AUTO CDC` in Week 6.
7. **Databricks SQL**
   1. Open **SQL Editor** and query `learn.get_started.gold_monthly_revenue`.
   2. Click **+ → Dashboard**, add the gold tables as datasets, and build a revenue-by-month line chart and a revenue-by-segment bar chart.
   3. Optional: create a **Genie space** on the two gold tables and ask "Which market segment grew fastest?"

## Clean up (optional)

```sql
DROP SCHEMA learn.get_started CASCADE;
DROP SCHEMA learn.get_started_sdp CASCADE;
```
