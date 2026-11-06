-- 06 · The same medallion flow as a Lakeflow Spark Declarative Pipeline
-- Use this as the source file of a new pipeline (see README, step 6).
-- Pipeline settings: default catalog = learn, default schema = get_started_sdp

CREATE OR REFRESH STREAMING TABLE sdp_bronze_orders
COMMENT 'Raw orders, loaded incrementally from the Volume with Auto Loader'
AS SELECT
  *,
  _metadata.file_path AS source_file,
  current_timestamp() AS ingested_at
FROM STREAM read_files('/Volumes/learn/get_started/raw/orders', format => 'json');

CREATE OR REFRESH STREAMING TABLE sdp_silver_orders (
  CONSTRAINT positive_price EXPECT (total_price > 0) ON VIOLATION DROP ROW,
  CONSTRAINT has_order_date EXPECT (order_date IS NOT NULL)
)
COMMENT 'Typed and validated orders'
AS SELECT
  CAST(o_orderkey AS BIGINT)          AS order_id,
  CAST(o_custkey AS BIGINT)           AS customer_id,
  o_orderstatus                       AS order_status,
  CAST(o_totalprice AS DECIMAL(12,2)) AS total_price,
  CAST(o_orderdate AS DATE)           AS order_date,
  o_orderpriority                     AS order_priority,
  ingested_at
FROM STREAM(sdp_bronze_orders);

CREATE OR REFRESH MATERIALIZED VIEW sdp_gold_monthly_revenue
COMMENT 'Monthly revenue by order priority'
AS SELECT
  DATE_TRUNC('MONTH', order_date) AS order_month,
  order_priority,
  COUNT(*)         AS orders,
  SUM(total_price) AS revenue
FROM sdp_silver_orders
GROUP BY ALL;
