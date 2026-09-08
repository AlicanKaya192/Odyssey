CREATE TABLE cities (
    id INT PRIMARY KEY,
    name NVARCHAR(30) NOT NULL,
    country NVARCHAR(30) NOT NULL,
    population INT NOT NULL
);

INSERT INTO cities (id, name, country, population) VALUES
    (1, 'Istanbul', 'Turkey', 15840900),
    (2, 'Ankara', 'Turkey', 5803482),
    (3, 'Izmir', 'Turkey', 4462056),
    (4, 'Berlin', 'Germany', 3576873),
    (5, 'Amsterdam', 'Netherlands', 921402);
