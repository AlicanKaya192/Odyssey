SELECT s.name
FROM suppliers s
WHERE NOT EXISTS (
    SELECT 1 FROM products p WHERE p.supplier_code = s.code
)
ORDER BY s.name;
