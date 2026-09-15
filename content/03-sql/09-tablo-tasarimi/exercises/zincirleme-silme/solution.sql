CREATE TABLE order_notes (
    id INT IDENTITY(1,1) PRIMARY KEY,
    order_id INT NOT NULL
        REFERENCES orders(id) ON DELETE CASCADE,
    note NVARCHAR(200) NOT NULL
);
