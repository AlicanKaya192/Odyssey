SELECT category_code, name, price
FROM (
    SELECT category_code, name, price,
           ROW_NUMBER() OVER (PARTITION BY category_code
                              ORDER BY price DESC) AS rn
    FROM products
) AS ranked
WHERE rn = 1
ORDER BY category_code;
