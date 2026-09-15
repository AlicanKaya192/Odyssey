SELECT id,
       LEFT(name, CHARINDEX(' ', name) - 1) AS first_name,
       SUBSTRING(name, CHARINDEX(' ', name) + 1, LEN(name)) AS last_name
FROM employees
ORDER BY id;
