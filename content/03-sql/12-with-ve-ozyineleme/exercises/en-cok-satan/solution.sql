WITH units AS (
    SELECT i.product_id, SUM(i.quantity) AS units
    FROM order_items i
    JOIN orders o ON o.id = i.order_id
    WHERE o.status <> 'cancelled'
    GROUP BY i.product_id
),
ranked AS (
    SELECT p.category_code, p.name, u.units,
           ROW_NUMBER() OVER (PARTITION BY p.category_code
                              ORDER BY u.units DESC) AS rn
    FROM units u
    JOIN products p ON p.id = u.product_id
)
SELECT category_code, name, units
FROM ranked
WHERE rn = 1
ORDER BY category_code;
