SELECT category, COUNT(*) AS item_count
FROM products
GROUP BY category
ORDER BY category;
