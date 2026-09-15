CREATE TABLE returns (
    id INT IDENTITY(1,1) PRIMARY KEY,
    order_id INT NOT NULL REFERENCES orders (id),
    reason NVARCHAR(100) NOT NULL,
    quantity INT NOT NULL CHECK (quantity > 0)
);

INSERT INTO returns (order_id, reason, quantity) VALUES
    (1005, 'Damaged screen', 1),
    (1009, 'Wrong item', 1);
