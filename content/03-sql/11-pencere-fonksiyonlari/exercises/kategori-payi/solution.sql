SELECT p.category_code,
       SUM(i.quantity * i.unit_price) AS revenue,
       CAST(100.0 * SUM(i.quantity * i.unit_price)
            / SUM(SUM(i.quantity * i.unit_price)) OVER ()
            AS DECIMAL(5,2)) AS share
FROM order_items i
JOIN products p ON p.id = i.product_id
JOIN orders o ON o.id = i.order_id
WHERE o.status <> 'cancelled'
GROUP BY p.category_code
ORDER BY revenue DESC;
