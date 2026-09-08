SELECT category, COUNT(*) AS item_count
FROM products
WHERE stock > 0
GROUP BY category
HAVING COUNT(*) >= 2
ORDER BY item_count DESC, category;
