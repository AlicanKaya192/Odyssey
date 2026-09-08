SELECT category,
       COUNT(*) AS item_count,
       MIN(price) AS cheapest,
       MAX(price) AS priciest
FROM products
GROUP BY category
ORDER BY category;
