CREATE VIEW dbo.order_summary AS
SELECT o.id, o.order_date,
       c.name AS customer,
       COALESCE(e.name, 'Unassigned') AS employee,
       COUNT(*) AS item_count,
       SUM(i.quantity * i.unit_price) AS total
FROM orders o
JOIN customers c ON c.id = o.customer_id
LEFT JOIN employees e ON e.id = o.employee_id
JOIN order_items i ON i.order_id = o.id
GROUP BY o.id, o.order_date, c.name, e.name;
