SELECT name AS product, price AS amount
FROM products
WHERE stock > 0
ORDER BY amount DESC;
