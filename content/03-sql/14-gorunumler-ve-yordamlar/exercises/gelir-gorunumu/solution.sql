CREATE VIEW dbo.customer_revenue AS
SELECT c.id, c.name,
       SUM(i.quantity * i.unit_price) AS revenue
FROM customers c
JOIN orders o ON o.customer_id = c.id
JOIN order_items i ON i.order_id = o.id
WHERE o.status <> 'cancelled'
GROUP BY c.id, c.name;
