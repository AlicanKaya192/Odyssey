SELECT t.customer_id, t.order_count
FROM (
    SELECT customer_id, COUNT(*) AS order_count
    FROM orders
    GROUP BY customer_id
) t
WHERE t.order_count >= 2
ORDER BY t.order_count DESC, t.customer_id;
