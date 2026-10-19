
-- 1. Check row counts in all staging tables
SELECT 'customers' AS dataset, COUNT(*) AS total_rows FROM stg_customers
UNION ALL
SELECT 'orders', COUNT(*) FROM stg_orders
UNION ALL
SELECT 'order_items', COUNT(*) FROM stg_order_items
UNION ALL
SELECT 'order_payments', COUNT(*) FROM stg_order_payments
UNION ALL
SELECT 'order_reviews', COUNT(*) FROM stg_order_reviews
UNION ALL
SELECT 'products', COUNT(*) FROM stg_products
UNION ALL
SELECT 'sellers', COUNT(*) FROM stg_sellers
UNION ALL
SELECT 'geolocation', COUNT(*) FROM stg_geolocation;


-- 2. Monthly order count
SELECT
    DATE_TRUNC('month', order_purchase_timestamp::timestamp) AS order_month,
    COUNT(*) AS total_orders
FROM stg_orders
GROUP BY 1
ORDER BY 1;


-- 3. Monthly sales revenue
SELECT
    DATE_TRUNC('month', o.order_purchase_timestamp::timestamp) AS order_month,
    ROUND(SUM(oi.price::numeric), 2) AS product_revenue
FROM stg_orders o
JOIN stg_order_items oi
    ON o.order_id = oi.order_id
GROUP BY 1
ORDER BY 1;


-- 4. Top 10 product categories by revenue
SELECT
    COALESCE(p.product_category_name, 'unknown') AS product_category,
    ROUND(SUM(oi.price::numeric), 2) AS total_revenue
FROM stg_order_items oi
JOIN stg_products p
    ON oi.product_id = p.product_id
GROUP BY 1
ORDER BY total_revenue DESC
LIMIT 10;


-- 5. Top 10 customer states by number of customers
SELECT
    customer_state,
    COUNT(DISTINCT customer_unique_id) AS total_customers
FROM stg_customers
GROUP BY customer_state
ORDER BY total_customers DESC
LIMIT 10;


-- 6. Average customer review score
SELECT
    ROUND(AVG(review_score::numeric), 2) AS average_review_score,
    COUNT(*) AS total_reviews
FROM stg_order_reviews;


-- 7. Average delivery time in days
SELECT
    ROUND(
        AVG(
            EXTRACT(
                EPOCH FROM (
                    order_delivered_customer_date::timestamp
                    - order_purchase_timestamp::timestamp
                )
            ) / 86400
        )::numeric,
        2
    ) AS average_delivery_days
FROM stg_orders
WHERE order_delivered_customer_date IS NOT NULL
  AND order_purchase_timestamp IS NOT NULL;


-- 8. Top 10 sellers by product revenue
SELECT
    oi.seller_id,
    ROUND(SUM(oi.price::numeric), 2) AS total_revenue,
    COUNT(DISTINCT oi.order_id) AS total_orders
FROM stg_order_items oi
GROUP BY oi.seller_id
ORDER BY total_revenue DESC
LIMIT 10;
