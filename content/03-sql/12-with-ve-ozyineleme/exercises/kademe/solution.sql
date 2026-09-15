WITH chain AS (
    SELECT id, name, 0 AS level
    FROM employees
    WHERE manager_id IS NULL
    UNION ALL
    SELECT e.id, e.name, c.level + 1
    FROM employees e
    JOIN chain c ON e.manager_id = c.id
)
SELECT id, name, level
FROM chain
ORDER BY level, id;
