SELECT name, stock, stock / 2.0 AS half_stock
FROM products
WHERE stock > 0
ORDER BY name;
