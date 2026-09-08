SELECT name, category
FROM products
WHERE supplier_code IS NULL
ORDER BY name;
