SELECT s.carrier,
       ROUND(AVG(CAST(DATEDIFF(day, o.order_date, s.shipped_date)
                      AS DECIMAL(10,2))), 2) AS avg_days
FROM shipments s
JOIN orders o ON o.id = s.order_id
GROUP BY s.carrier
ORDER BY s.carrier;
