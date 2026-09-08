CREATE TABLE kategoriler (
    kod NVARCHAR(10) PRIMARY KEY,
    ad NVARCHAR(30) NOT NULL
);

INSERT INTO kategoriler (kod, ad) VALUES
    ('AKS', 'Aksesuar'),
    ('EKR', 'Ekran'),
    ('BIL', 'Bilgisayar');

CREATE TABLE urunler (
    id INT PRIMARY KEY,
    ad NVARCHAR(40) NOT NULL,
    kategori NVARCHAR(30) NOT NULL,
    fiyat DECIMAL(10,2) NOT NULL,
    stok INT NOT NULL
);

INSERT INTO urunler (id, ad, kategori, fiyat, stok) VALUES
    (1, 'Klavye', 'Aksesuar', 450.00, 32),
    (2, 'Monitor', 'Ekran', 3200.00, 8),
    (3, 'Fare', 'Aksesuar', 220.00, 0),
    (4, 'Laptop', 'Bilgisayar', 24500.00, 5),
    (5, 'Kulaklik', 'Aksesuar', 890.00, 14),
    (6, 'Webcam', 'Aksesuar', 1150.00, 3),
    (7, 'Masaustu', 'Bilgisayar', 18900.00, 2),
    (8, 'Projeksiyon', 'Ekran', 7400.00, 0);
