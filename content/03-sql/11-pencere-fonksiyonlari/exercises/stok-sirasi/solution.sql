SELECT name, stock,
       DENSE_RANK() OVER (ORDER BY stock DESC) AS stock_rank
FROM products
ORDER BY stock DESC, name;
