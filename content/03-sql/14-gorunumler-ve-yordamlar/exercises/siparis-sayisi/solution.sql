CREATE PROCEDURE dbo.customer_order_count
    @customer_id INT,
    @order_count INT OUTPUT,
    @status NVARCHAR(20) = NULL
AS
SELECT @order_count = COUNT(*)
FROM orders
WHERE customer_id = @customer_id
  AND (@status IS NULL OR status = @status);
