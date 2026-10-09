`count_errors(path)` fonksiyonunu yaz: `.gz` ile sıkıştırılmış kayıt
dosyasını diske çıkarmadan, `gzip.open(path, "rt",
encoding="utf-8")` ile satır satır okusun ve `ERROR` ile başlayan satırları
saysın. Alttaki satırlar dosyayı oluşturuyor.

**Beklenen çıktı:**

```
3
```
