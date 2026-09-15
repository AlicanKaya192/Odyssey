SELECT category_code,
       STRING_AGG(name, ', ') WITHIN GROUP (ORDER BY name) AS products
FROM products
GROUP BY category_code
ORDER BY category_code;
