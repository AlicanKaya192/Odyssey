`random_state=51` ile seçilen 60 kişiden sayfa açılış süresinin (`load_ms`)
ortalamasını ve %95 güven aralığını yazdır. Aralık için
`stats.t.interval(0.95, df=n - 1, loc=ortalama, scale=se)` kullan.
Başlangıç kodu 1,96 çarpanını kullanıyor. Ortalama ilk satırda (1 basamak),
sınırlar ikinci satırda (1 basamak).

**Beklenen çıktı:**

```text
843.8
813.9 873.7
```
