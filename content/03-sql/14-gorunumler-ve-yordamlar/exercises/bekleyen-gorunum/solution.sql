CREATE VIEW dbo.pending_orders AS
SELECT id, customer_id, order_date, status
FROM orders
WHERE status = 'pending'
WITH CHECK OPTION;
