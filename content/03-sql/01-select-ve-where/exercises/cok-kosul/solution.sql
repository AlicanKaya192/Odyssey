SELECT name
FROM products
WHERE (category = 'Accessory' OR category = 'Display')
  AND stock > 0;
