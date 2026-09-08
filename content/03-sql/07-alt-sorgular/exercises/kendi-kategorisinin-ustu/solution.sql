SELECT p.name, p.category_code, p.price
FROM products p
WHERE p.price > (
    SELECT AVG(p2.price) FROM products p2
    WHERE p2.category_code = p.category_code
)
ORDER BY p.name;
