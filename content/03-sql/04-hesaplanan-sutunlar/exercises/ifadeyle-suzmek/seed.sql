CREATE TABLE categories (
    code NVARCHAR(10) PRIMARY KEY,
    name NVARCHAR(30) NOT NULL
);

INSERT INTO categories (code, name) VALUES
    ('ACC', 'Accessory'),
    ('DIS', 'Display'),
    ('COM', 'Computer'),
    ('SOF', 'Software');

CREATE TABLE suppliers (
    code NVARCHAR(10) PRIMARY KEY,
    name NVARCHAR(40) NOT NULL,
    city NVARCHAR(30) NOT NULL
);

INSERT INTO suppliers (code, name, city) VALUES
    ('S1', 'Anatolia Tech', 'Ankara'),
    ('S2', 'Aegean Systems', 'Izmir'),
    ('S3', 'Marmara Logistics', 'Istanbul');

CREATE TABLE products (
    id INT PRIMARY KEY,
    name NVARCHAR(40) NOT NULL,
    category NVARCHAR(30) NOT NULL,
    price DECIMAL(10,2) NOT NULL,
    stock INT NOT NULL,
    supplier_code NVARCHAR(10) NULL
);

INSERT INTO products (id, name, category, price, stock, supplier_code) VALUES
    (1,  'Keyboard',     'Accessory', 450.00,   32, 'S1'),
    (2,  'Monitor',      'Display',   3200.00,   8, 'S2'),
    (3,  'Mouse',        'Accessory', 220.00,    0, 'S1'),
    (4,  'Laptop',       'Computer',  24500.00,  5, 'S3'),
    (5,  'Headset',      'Accessory', 890.00,   14, NULL),
    (6,  'Webcam',       'Accessory', 1150.00,   3, 'S2'),
    (7,  'Desktop',      'Computer',  18900.00,  2, 'S3'),
    (8,  'Projector',    'Display',   7400.00,   0, NULL),
    (9,  'Cable',        'Accessory', 95.00,    60, 'S1'),
    (10, 'Office Suite', 'Software',  2400.00,  99, NULL),
    (11, 'Antivirus',    'Software',  780.00,   99, 'S2'),
    (12, 'Microphone',   'Accessory', 1320.00,   7, 'S3');
