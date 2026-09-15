WITH customer_totals AS (
    SELECT o.customer_id,
           SUM(i.quantity * i.unit_price) AS total
    FROM orders o
    JOIN order_items i ON i.order_id = o.id
    WHERE o.status <> 'cancelled'
    GROUP BY o.customer_id
)
SELECT c.name, ct.total,
       ct.total - (SELECT AVG(total) FROM customer_totals) AS vs_avg
FROM customer_totals ct
JOIN customers c ON c.id = ct.customer_id
ORDER BY ct.total DESC;
