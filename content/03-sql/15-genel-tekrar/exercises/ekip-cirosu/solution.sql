WITH team AS (
    SELECT id AS manager_id, id AS member_id FROM employees
    UNION ALL
    SELECT t.manager_id, e.id
    FROM employees e
    JOIN team t ON e.manager_id = t.member_id
),
sales AS (
    SELECT o.employee_id, SUM(i.quantity * i.unit_price) AS revenue
    FROM orders o
    JOIN order_items i ON i.order_id = o.id
    WHERE o.status <> 'cancelled'
    GROUP BY o.employee_id
)
SELECT m.name,
       COUNT(*) AS team_size,
       COALESCE(SUM(s.revenue), 0) AS team_revenue
FROM team t
JOIN employees m ON m.id = t.manager_id
LEFT JOIN sales s ON s.employee_id = t.member_id
WHERE t.member_id <> t.manager_id
GROUP BY m.id, m.name
ORDER BY team_revenue DESC, m.name;
