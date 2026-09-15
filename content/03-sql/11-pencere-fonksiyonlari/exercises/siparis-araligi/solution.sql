SELECT customer_id, id, order_date,
       DATEDIFF(day,
                LAG(order_date) OVER (PARTITION BY customer_id
                                      ORDER BY order_date),
                order_date) AS gap_days
FROM orders
ORDER BY customer_id, order_date;
