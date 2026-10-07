Siparişleri ay klasörlerine ayır ve DuckDB ile yalnızca bir ayı sorgula.

**Yapman gerekenler:**

1. `orders` ve `month` sütunu hazır. Her ay için
   `lake/month=<ay>/part-0.parquet` dosyasını yaz (`month` sütunu dosyaya
   girmesin).
2. Klasör sayısını yazdır.
3. DuckDB ile göldeki Haziran'ın (`'2024-06'`) en çok ciro yapan üç
   kategorisini, ciroyu iki ondalık yuvarlayarak bul; her satıra kategori ve
   ciro yazdır.
4. Aynı süzmeyle `EXPLAIN ANALYZE SELECT count(*) ...` çalıştır ve plan
   metninden taranan dosya bilgisini yazdır:
   `re.search(r"Scanning Files: \d+/\d+", plan).group()`.

**Beklenen çıktı:**

```
12
electronics 19835690.29
clothing 6965783.83
home 5271617.01
Scanning Files: 1/12
```
