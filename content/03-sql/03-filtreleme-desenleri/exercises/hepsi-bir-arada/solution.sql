SELECT ad, kategori, fiyat
FROM urunler
WHERE kategori IN ('Aksesuar', 'Ekran')
  AND fiyat BETWEEN 200 AND 2000
  AND tedarikci_kod IS NOT NULL
ORDER BY fiyat DESC;
