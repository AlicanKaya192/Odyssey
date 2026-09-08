-- Orta Seviye semasi: sekiz tablolu bir siparis veritabani.
--
-- Baslangic seviyesinde tek tablo yetiyordu; buradan itibaren tablolar
-- birbirine baglaniyor ve JOIN'siz cevaplanamayan sorular basliyor.

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
    city NVARCHAR(30) NOT NULL,
    country NVARCHAR(30) NOT NULL
);

INSERT INTO suppliers (code, name, city, country) VALUES
    ('S1', 'Anatolia Tech',     'Ankara',    'Turkey'),
    ('S2', 'Aegean Systems',    'Izmir',     'Turkey'),
    ('S3', 'Marmara Logistics', 'Istanbul',  'Turkey'),
    ('S4', 'Rhine Components',  'Berlin',    'Germany');

CREATE TABLE products (
    id INT PRIMARY KEY,
    name NVARCHAR(40) NOT NULL,
    category_code NVARCHAR(10) NOT NULL,
    supplier_code NVARCHAR(10) NULL,
    price DECIMAL(10,2) NOT NULL,
    stock INT NOT NULL
);

INSERT INTO products (id, name, category_code, supplier_code, price, stock) VALUES
    (1,  'Keyboard',     'ACC', 'S1', 450.00,   32),
    (2,  'Monitor',      'DIS', 'S2', 3200.00,   8),
    (3,  'Mouse',        'ACC', 'S1', 220.00,    0),
    (4,  'Laptop',       'COM', 'S3', 24500.00,  5),
    (5,  'Headset',      'ACC', NULL, 890.00,   14),
    (6,  'Webcam',       'ACC', 'S2', 1150.00,   3),
    (7,  'Desktop',      'COM', 'S3', 18900.00,  2),
    (8,  'Projector',    'DIS', NULL, 7400.00,   0),
    (9,  'Cable',        'ACC', 'S1', 95.00,    60),
    (10, 'Office Suite', 'SOF', NULL, 2400.00,  99),
    (11, 'Antivirus',    'SOF', 'S2', 780.00,   99),
    (12, 'Microphone',   'ACC', 'S3', 1320.00,   7);

CREATE TABLE customers (
    id INT PRIMARY KEY,
    name NVARCHAR(40) NOT NULL,
    city NVARCHAR(30) NOT NULL,
    country NVARCHAR(30) NOT NULL,
    joined DATE NOT NULL
);

INSERT INTO customers (id, name, city, country, joined) VALUES
    (1, 'Nova Retail',     'Istanbul',  'Turkey',      '2024-03-11'),
    (2, 'Bright Office',   'Ankara',    'Turkey',      '2024-07-02'),
    (3, 'Delta Systems',   'Izmir',     'Turkey',      '2025-01-20'),
    (4, 'Helix Studio',    'Berlin',    'Germany',     '2025-04-08'),
    (5, 'Orion Labs',      'Amsterdam', 'Netherlands', '2025-09-15'),
    (6, 'Quiet Partners',  'Istanbul',  'Turkey',      '2026-02-01');

CREATE TABLE employees (
    id INT PRIMARY KEY,
    name NVARCHAR(40) NOT NULL,
    title NVARCHAR(30) NOT NULL,
    manager_id INT NULL,
    hired DATE NOT NULL
);

INSERT INTO employees (id, name, title, manager_id, hired) VALUES
    (1, 'Ada Kilic',    'Director',       NULL, '2021-01-15'),
    (2, 'Bora Yilmaz',  'Sales Manager',  1,    '2022-03-01'),
    (3, 'Ceren Aksoy',  'Sales Rep',      2,    '2023-06-12'),
    (4, 'Deniz Kaya',   'Sales Rep',      2,    '2024-02-05'),
    (5, 'Emre Sahin',   'Support Lead',   1,    '2022-11-20'),
    (6, 'Fulya Demir',  'Support Agent',  5,    '2025-05-30');

CREATE TABLE orders (
    id INT PRIMARY KEY,
    customer_id INT NOT NULL,
    employee_id INT NULL,
    order_date DATE NOT NULL,
    status NVARCHAR(20) NOT NULL
);

INSERT INTO orders (id, customer_id, employee_id, order_date, status) VALUES
    (1001, 1, 3,    '2026-01-08', 'shipped'),
    (1002, 2, 3,    '2026-01-15', 'shipped'),
    (1003, 1, 4,    '2026-02-02', 'shipped'),
    (1004, 3, NULL, '2026-02-11', 'pending'),
    (1005, 4, 4,    '2026-02-19', 'shipped'),
    (1006, 1, 3,    '2026-03-03', 'cancelled'),
    (1007, 5, 4,    '2026-03-14', 'shipped'),
    (1008, 2, 3,    '2026-03-22', 'pending'),
    (1009, 4, NULL, '2026-04-01', 'shipped'),
    (1010, 3, 4,    '2026-04-17', 'pending');

CREATE TABLE order_items (
    order_id INT NOT NULL,
    product_id INT NOT NULL,
    quantity INT NOT NULL,
    unit_price DECIMAL(10,2) NOT NULL,
    PRIMARY KEY (order_id, product_id)
);

INSERT INTO order_items (order_id, product_id, quantity, unit_price) VALUES
    (1001, 1,  2, 450.00),
    (1001, 3,  2, 220.00),
    (1001, 9,  5, 95.00),
    (1002, 4,  1, 24500.00),
    (1002, 2,  2, 3200.00),
    (1003, 11, 3, 780.00),
    (1004, 1,  1, 450.00),
    (1004, 6,  1, 1150.00),
    (1005, 7,  1, 18900.00),
    (1005, 2,  1, 3200.00),
    (1005, 12, 2, 1320.00),
    (1006, 10, 1, 2400.00),
    (1007, 5,  4, 890.00),
    (1007, 9,  10, 95.00),
    (1008, 2,  1, 3200.00),
    (1009, 4,  1, 24500.00),
    (1009, 1,  1, 450.00),
    (1010, 11, 2, 780.00),
    (1010, 10, 1, 2400.00),
    (1010, 6,  1, 1150.00);

CREATE TABLE shipments (
    order_id INT PRIMARY KEY,
    shipped_date DATE NOT NULL,
    carrier NVARCHAR(30) NOT NULL
);

INSERT INTO shipments (order_id, shipped_date, carrier) VALUES
    (1001, '2026-01-10', 'FastLine'),
    (1002, '2026-01-18', 'FastLine'),
    (1003, '2026-02-05', 'CityMove'),
    (1005, '2026-02-22', 'FastLine'),
    (1007, '2026-03-17', 'CityMove'),
    (1009, '2026-04-04', 'NorthWay');
