SELECT category, COUNT(*) AS item_count
FROM products
GROUP BY category
HAVING COUNT(*) > 2
ORDER BY category;
