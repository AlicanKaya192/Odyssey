SELECT p.name AS product, c.name AS category
FROM products p
JOIN categories c ON p.category_code = c.code
ORDER BY p.name;
