ALTER TABLE order_items
ADD CONSTRAINT fk_items_order
    FOREIGN KEY (order_id) REFERENCES orders(id);
