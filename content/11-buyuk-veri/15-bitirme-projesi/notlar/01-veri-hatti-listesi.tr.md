Büyük bir veriyle karşılaşınca sırayla sorulacak sorular. Her maddenin yanında
patikadaki bölümü var.

## 1. Ölç

- Dosya diskte ne kadar? (`os.path.getsize`)
- On bin satırlık örnek bellekte satır başına ne kadar? Tamamı için tahmin?
  (`memory_usage(deep=True)`, Bölüm 1)
- Bilgisayarın boş belleği ne kadar? Tahmin onun yarısını geçiyorsa tek
  seferde okuma.

## 2. Küçült

- Sayı sütunlarına yetecek en küçük tür (`int8`, `int32`), tekrar eden
  metne `category` (Bölüm 2).
- Gerekmeyen sütunları hiç okuma (`usecols`, Parquet'te `columns`).

## 3. Biçimi seç

- Her gün sorgulanacaksa CSV'yi bir kez Parquet'e çevir (Bölüm 4, 5).
- Büyük dosyayı parça parça çevir (`chunksize` + `ParquetWriter`, Bölüm 3).
- Sıkıştırma: `zstd` küçük, `snappy` hızlı.

## 4. Bölümle

- Sorular hep aynı sütunla mı başlıyor (ay, şehir)? O sütunla klasörlere
  ayır (Bölüm 6).
- Çok küçük dosya üretme: her bölümde makul miktarda satır olsun.

## 5. Aracı seç

| Durum | Araç |
|---|---|
| Belleğe rahat sığıyor | pandas |
| Dosyada SQL, tek makine | DuckDB (Bölüm 7, 8) |
| pandas yazımı, bellekten büyük | dask (Bölüm 11) |
| Birçok makine | Spark (Bölüm 13) |
| Veri canlı geliyor | Akış: pencereler, Kafka (Bölüm 14) |

## 6. Doğrula

- Sonucu ikinci bir yoldan hesapla (kısmi toplam + birleştirme, Bölüm 12).
- Ondalıkları `==` ile değil, küçük bir toleransla karşılaştır.
- Satır sayılarını kontrol et: çevirmeden önce ve sonra aynı mı?

## 7. Hız mı kesinlik mi?

- Hızlı fikir: örneklem (Bölüm 9), yaklaşık farklı sayısı.
- Yayımlanacak sonuç: kesin sorgu.
