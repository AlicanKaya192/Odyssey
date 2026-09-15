SELECT id, order_date,
       DATEADD(day, 7, order_date) AS due_date
FROM orders
ORDER BY id;
