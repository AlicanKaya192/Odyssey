SELECT ad, ISNULL(tedarikci_kod, 'YOK') AS tedarikci
FROM urunler
ORDER BY ad;
