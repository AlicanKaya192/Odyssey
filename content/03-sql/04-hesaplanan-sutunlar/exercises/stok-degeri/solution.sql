SELECT ad, fiyat * stok AS stok_degeri
FROM urunler
ORDER BY stok_degeri DESC;
