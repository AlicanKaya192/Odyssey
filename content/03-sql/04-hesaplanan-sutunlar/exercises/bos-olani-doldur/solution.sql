SELECT name, ISNULL(supplier_code, 'NONE') AS supplier
FROM products
ORDER BY name;
