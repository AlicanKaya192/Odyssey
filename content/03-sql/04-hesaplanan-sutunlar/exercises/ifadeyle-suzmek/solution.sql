SELECT ad, fiyat, stok, fiyat * stok AS stok_degeri
FROM urunler
WHERE fiyat * stok > 50000
ORDER BY stok_degeri DESC;
