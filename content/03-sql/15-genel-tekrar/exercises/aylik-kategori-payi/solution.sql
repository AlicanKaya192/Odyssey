WITH monthly AS (
    SELECT DATEFROMPARTS(YEAR(o.order_date), MONTH(o.order_date), 1) AS month,
           p.category_code,
           SUM(i.quantity * i.unit_price) AS revenue
    FROM orders o
    JOIN order_items i ON i.order_id = o.id
    JOIN products p ON p.id = i.product_id
    WHERE o.status <> 'cancelled'
    GROUP BY DATEFROMPARTS(YEAR(o.order_date), MONTH(o.order_date), 1),
             p.category_code
)
SELECT month, category_code, revenue,
       CAST(100.0 * revenue / SUM(revenue) OVER (PARTITION BY month)
            AS DECIMAL(5,2)) AS share
FROM monthly
ORDER BY month, revenue DESC;
