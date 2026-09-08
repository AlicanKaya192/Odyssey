SELECT COUNT(*) AS total_rows,
       COUNT(supplier_code) AS with_supplier,
       COUNT(DISTINCT category) AS distinct_categories
FROM products;
