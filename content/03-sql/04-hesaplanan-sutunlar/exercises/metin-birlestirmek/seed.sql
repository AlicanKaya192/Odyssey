CREATE TABLE kategoriler (
    kod NVARCHAR(10) PRIMARY KEY,
    ad NVARCHAR(30) NOT NULL
);

INSERT INTO kategoriler (kod, ad) VALUES
    ('AKS', 'Aksesuar'),
    ('EKR', 'Ekran'),
    ('BIL', 'Bilgisayar'),
    ('YAZ', 'Yazilim');

CREATE TABLE tedarikciler (
    kod NVARCHAR(10) PRIMARY KEY,
    ad NVARCHAR(40) NOT NULL,
    sehir NVARCHAR(30) NOT NULL
);

INSERT INTO tedarikciler (kod, ad, sehir) VALUES
    ('T1', 'Anadolu Teknoloji', 'Ankara'),
    ('T2', 'Ege Bilisim', 'Izmir'),
    ('T3', 'Marmara Dagitim', 'Istanbul');

CREATE TABLE urunler (
    id INT PRIMARY KEY,
    ad NVARCHAR(40) NOT NULL,
    kategori NVARCHAR(30) NOT NULL,
    fiyat DECIMAL(10,2) NOT NULL,
    stok INT NOT NULL,
    tedarikci_kod NVARCHAR(10) NULL
);

INSERT INTO urunler (id, ad, kategori, fiyat, stok, tedarikci_kod) VALUES
    (1,  'Klavye',      'Aksesuar',   450.00,   32, 'T1'),
    (2,  'Monitor',     'Ekran',      3200.00,   8, 'T2'),
    (3,  'Fare',        'Aksesuar',   220.00,    0, 'T1'),
    (4,  'Laptop',      'Bilgisayar', 24500.00,  5, 'T3'),
    (5,  'Kulaklik',    'Aksesuar',   890.00,   14, NULL),
    (6,  'Webcam',      'Aksesuar',   1150.00,   3, 'T2'),
    (7,  'Masaustu',    'Bilgisayar', 18900.00,  2, 'T3'),
    (8,  'Projeksiyon', 'Ekran',      7400.00,   0, NULL),
    (9,  'Kablo',       'Aksesuar',   95.00,    60, 'T1'),
    (10, 'Ofis Paketi', 'Yazilim',    2400.00,  99, NULL),
    (11, 'Antivirus',   'Yazilim',    780.00,   99, 'T2'),
    (12, 'Mikrofon',    'Aksesuar',   1320.00,   7, 'T3');
