CREATE PROCEDURE dbo.customer_orders
    @customer_id INT
AS
SELECT id, order_date, status
FROM orders
WHERE customer_id = @customer_id
ORDER BY order_date;
