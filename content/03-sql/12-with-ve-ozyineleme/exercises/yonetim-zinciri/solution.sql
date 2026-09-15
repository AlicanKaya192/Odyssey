WITH chain AS (
    SELECT id, CAST(name AS NVARCHAR(200)) AS path
    FROM employees
    WHERE manager_id IS NULL
    UNION ALL
    SELECT e.id, CAST(c.path + N' > ' + e.name AS NVARCHAR(200))
    FROM employees e
    JOIN chain c ON e.manager_id = c.id
)
SELECT id, path
FROM chain
ORDER BY path;
