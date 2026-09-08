SELECT name, category, price
FROM products
WHERE category IN ('Accessory', 'Display')
  AND price BETWEEN 200 AND 2000
  AND supplier_code IS NOT NULL
ORDER BY price DESC;
