SELECT name
FROM products
WHERE supplier_code IN (
    SELECT code FROM suppliers WHERE city = 'Istanbul'
)
ORDER BY name;
