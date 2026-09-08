SELECT name, category
FROM products
WHERE category IN ('Display', 'Software')
ORDER BY name;
