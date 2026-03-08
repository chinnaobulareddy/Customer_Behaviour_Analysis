create database customer_analysis;
use customer_analysis;
-- Monthly Revenue KPI
SELECT
  DATE_FORMAT(event_time, '%Y-%m') AS month,
  ROUND(SUM(price), 2) AS monthly_revenue
FROM oct_table
WHERE event_type = 'purchase'
  AND event_time >= '2019-10-01' AND event_time < '2019-11-01'
GROUP BY DATE_FORMAT(event_time, '%Y-%m');

-- Purchase conversion rate (sessions with purchase / total sessions) KPI
SELECT
  ROUND(
    100 * COUNT(DISTINCT CASE WHEN event_type = 'purchase' THEN user_session END)
    / NULLIF(COUNT(DISTINCT user_session), 0)
  , 2) AS session_purchase_conversion_rate_pct,
  COUNT(DISTINCT user_session) AS total_sessions,
  COUNT(DISTINCT CASE WHEN event_type = 'purchase' THEN user_session END) AS purchasing_sessions
FROM oct_table
WHERE event_time >= '2019-10-01' AND event_time < '2019-11-01';

-- Daily Revenue 
USE customer_analysis;

SELECT
  DATE(event_time) AS day,
  ROUND(SUM(price), 2) AS revenue
FROM oct_table
WHERE event_type = 'purchase'
  AND event_time >= '2019-10-01' AND event_time < '2019-11-01'
GROUP BY DATE(event_time)
ORDER BY day;

-- Top 10 Products
SELECT
  product_id,
  ROUND(SUM(price), 2) AS revenue,
  COUNT(*) AS units_sold
FROM oct_table
WHERE event_type = 'purchase'
  AND event_time >= '2019-10-01' AND event_time < '2019-11-01'
GROUP BY product_id
ORDER BY revenue DESC
LIMIT 10;