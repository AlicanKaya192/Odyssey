SELECT ad, stok, stok / 2.0 AS yari_stok
FROM urunler
WHERE stok > 0
ORDER BY ad;
