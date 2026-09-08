CREATE TABLE sehirler (
    id INT PRIMARY KEY,
    ad NVARCHAR(30) NOT NULL,
    ulke NVARCHAR(30) NOT NULL,
    nufus INT NOT NULL
);

INSERT INTO sehirler (id, ad, ulke, nufus) VALUES
    (1, 'Istanbul', 'Turkiye', 15840900),
    (2, 'Ankara', 'Turkiye', 5803482),
    (3, 'Izmir', 'Turkiye', 4462056),
    (4, 'Berlin', 'Almanya', 3576873),
    (5, 'Amsterdam', 'Hollanda', 921402);
