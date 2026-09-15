SELECT o.id, o.order_date,
       SUM(i.quantity * i.unit_price) AS total,
       SUM(SUM(i.quantity * i.unit_price))
           OVER (ORDER BY o.order_date) AS running_total
FROM orders o
JOIN order_items i ON i.order_id = o.id
WHERE o.status <> 'cancelled'
GROUP BY o.id, o.order_date
ORDER BY o.order_date;
