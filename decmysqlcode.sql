use customer_analysis;
-- Top products by purchases and revenue
USE customer_analysis;

SELECT
  product_id,
  COUNT(*) AS purchase_events,
  ROUND(SUM(price), 2) AS revenue
FROM dec_data
WHERE event_type = 'purchase'
  AND product_id IS NOT NULL
GROUP BY product_id
ORDER BY revenue DESC
LIMIT 10;

-- Funnel counts (view → cart → purchase) and rates
SELECT
  views,
  carts,
  purchases,
  ROUND(100.0 * carts / NULLIF(views, 0), 2) AS view_to_cart_rate_pct,
  ROUND(100.0 * purchases / NULLIF(views, 0), 2) AS view_to_purchase_rate_pct,
  ROUND(100.0 * purchases / NULLIF(carts, 0), 2) AS cart_to_purchase_rate_pct
FROM (
  SELECT
    SUM(CASE WHEN event_type = 'view' THEN 1 ELSE 0 END) AS views,
    SUM(CASE WHEN event_type = 'cart' THEN 1 ELSE 0 END) AS carts,
    SUM(CASE WHEN event_type = 'purchase' THEN 1 ELSE 0 END) AS purchases
  FROM dec_data
) f;