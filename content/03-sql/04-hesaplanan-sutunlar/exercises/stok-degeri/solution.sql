SELECT name, price * stock AS stock_value
FROM products
ORDER BY stock_value DESC;
