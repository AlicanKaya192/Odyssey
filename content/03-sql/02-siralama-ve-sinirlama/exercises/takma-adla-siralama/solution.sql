SELECT ad AS urun, fiyat AS tutar
FROM urunler
WHERE stok > 0
ORDER BY tutar DESC;
