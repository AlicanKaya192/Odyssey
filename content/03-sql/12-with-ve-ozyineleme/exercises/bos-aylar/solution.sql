WITH months AS (
    SELECT CAST('2026-01-01' AS DATE) AS month
    UNION ALL
    SELECT DATEADD(month, 1, month)
    FROM months
    WHERE month < '2026-06-01'
),
revenue AS (
    SELECT DATEFROMPARTS(YEAR(o.order_date), MONTH(o.order_date), 1) AS month,
           SUM(i.quantity * i.unit_price) AS revenue
    FROM orders o
    JOIN order_items i ON i.order_id = o.id
    WHERE o.status <> 'cancelled'
    GROUP BY DATEFROMPARTS(YEAR(o.order_date), MONTH(o.order_date), 1)
)
SELECT m.month, COALESCE(r.revenue, 0) AS revenue
FROM months m
LEFT JOIN revenue r ON r.month = m.month
ORDER BY m.month;
