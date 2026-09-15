CREATE PROCEDURE dbo.ship_order
    @order_id INT
AS
BEGIN
    SET NOCOUNT ON;
    IF NOT EXISTS (SELECT 1 FROM orders
                   WHERE id = @order_id AND status = 'pending')
        THROW 50001, N'Order is not pending.', 1;
    UPDATE orders SET status = 'shipped' WHERE id = @order_id;
END;
