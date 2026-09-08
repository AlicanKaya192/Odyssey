SELECT o.id AS order_id, c.name AS customer, p.name AS product,
       i.quantity
FROM orders o
JOIN customers c ON o.customer_id = c.id
JOIN order_items i ON o.id = i.order_id
JOIN products p ON i.product_id = p.id
WHERE o.id = 1005
ORDER BY p.name;
