use customer_analysis;
-- KPI 1: View → Purchase conversion rate (session-based)

WITH session_flags AS (
  SELECT
    user_session,
    MAX(event_type = 'view') AS has_view,
    MAX(event_type = 'purchase') AS has_purchase
  FROM nov_data
  WHERE user_session IS NOT NULL
  GROUP BY user_session
)
SELECT
  ROUND(
    100 * SUM(has_view = 1 AND has_purchase = 1) / NULLIF(SUM(has_view = 1), 0),
    2
  ) AS view_to_purchase_conversion_rate_pct
FROM session_flags;

-- KPI 2: ARPPU (Average Revenue Per Purchasing User)
SELECT
  ROUND(AVG(user_revenue), 2) AS arppu
FROM (
  SELECT
    user_id,
    SUM(price) AS user_revenue
  FROM nov_data
  WHERE event_type = 'purchase'
    AND user_id IS NOT NULL
    AND price IS NOT NULL
  GROUP BY user_id
) t;

-- Top 10 Products by Revenue
USE customer_analysis;

SELECT
  product_id,
  COUNT(*) AS purchase_events,
  ROUND(SUM(price), 2) AS revenue
FROM nov_data
WHERE event_type = 'purchase'
  AND product_id IS NOT NULL
  AND price IS NOT NULL
GROUP BY product_id
ORDER BY revenue DESC
LIMIT 10;

-- Funnel counts and rates (view → cart → purchase)
SELECT
  SUM(event_type = 'view') AS views,
  SUM(event_type = 'cart') AS carts,
  SUM(event_type = 'purchase') AS purchases,
  ROUND(100 * SUM(event_type = 'cart') / NULLIF(SUM(event_type = 'view'), 0), 2) AS view_to_cart_rate_pct,
  ROUND(100 * SUM(event_type = 'purchase') / NULLIF(SUM(event_type = 'cart'), 0), 2) AS cart_to_purchase_rate_pct
FROM nov_data;