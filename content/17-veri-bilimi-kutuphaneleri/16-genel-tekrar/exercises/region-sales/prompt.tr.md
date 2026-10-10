`region_sales(orders, regions)` siparişler (`[no, şehir, tutar]`, şehir adları
dağınık) ve şehir → bölge tablosu (`[şehir, bölge]`) alıyor. Şunu yapsın:

1. Şehir adlarını `str.strip().str.title()` ile temizle.
2. Bölgeyi `how="left"` ile ekle (sipariş kaybolmasın).
3. Bölge başına toplam tutarı hesapla.

`{"sales": {bölge: toplam}, "unmatched": [bölgesi bulunmayan sipariş
numaraları]}` döndürsün. **Döngü yazma.**

**Beklenen çıktı:**

```
{'Aegean': 200, 'Central': 50}
[4]
```
