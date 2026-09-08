SELECT c.name AS customer, COUNT(o.id) AS order_count
FROM customers c
LEFT JOIN orders o ON c.id = o.customer_id
GROUP BY c.name
ORDER BY order_count DESC, customer;
