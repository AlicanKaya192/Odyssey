SELECT c.name AS customer
FROM customers c
LEFT JOIN orders o ON c.id = o.customer_id
WHERE o.id IS NULL
ORDER BY c.name;
