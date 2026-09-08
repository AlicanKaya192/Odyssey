SELECT p.name AS product, s.name AS supplier
FROM products p
LEFT JOIN suppliers s ON p.supplier_code = s.code
ORDER BY p.name;
