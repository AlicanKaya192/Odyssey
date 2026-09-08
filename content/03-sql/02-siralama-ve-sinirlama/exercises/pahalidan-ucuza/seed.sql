CREATE TABLE categories (
    code NVARCHAR(10) PRIMARY KEY,
    name NVARCHAR(30) NOT NULL
);

INSERT INTO categories (code, name) VALUES
    ('ACC', 'Accessory'),
    ('DIS', 'Display'),
    ('COM', 'Computer');

CREATE TABLE products (
    id INT PRIMARY KEY,
    name NVARCHAR(40) NOT NULL,
    category NVARCHAR(30) NOT NULL,
    price DECIMAL(10,2) NOT NULL,
    stock INT NOT NULL
);

INSERT INTO products (id, name, category, price, stock) VALUES
    (1, 'Keyboard',  'Accessory', 450.00,   32),
    (2, 'Monitor',   'Display',   3200.00,   8),
    (3, 'Mouse',     'Accessory', 220.00,    0),
    (4, 'Laptop',    'Computer',  24500.00,  5),
    (5, 'Headset',   'Accessory', 890.00,   14),
    (6, 'Webcam',    'Accessory', 1150.00,   3),
    (7, 'Desktop',   'Computer',  18900.00,  2),
    (8, 'Projector', 'Display',   7400.00,   0);
