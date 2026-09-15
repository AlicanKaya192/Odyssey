SELECT c.name,
       COUNT(*) AS orders,
       MIN(o.order_date) AS first_order,
       MAX(o.order_date) AS last_order,
       DATEDIFF(day, MIN(o.order_date), MAX(o.order_date)) AS span_days
FROM customers c
JOIN orders o ON o.customer_id = c.id
WHERE o.status <> 'cancelled'
GROUP BY c.id, c.name
HAVING COUNT(*) >= 2
ORDER BY span_days DESC, c.name;
