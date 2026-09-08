SELECT name, price, stock, price * stock AS stock_value
FROM products
WHERE price * stock > 50000
ORDER BY stock_value DESC;
