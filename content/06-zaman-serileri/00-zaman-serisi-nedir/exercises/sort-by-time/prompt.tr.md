Satış kayıtları bir sistemden **karışık sırayla** gelmiş:
`sales_shuffled.csv`. İlk iş sırayı düzeltmek.

Tarihler `2022-01-01` biçiminde (ISO 8601). Bu biçim metin olarak
sıralandığında da takvim sırasına giriyor; yani `sort_values("date")` burada
doğru çalışıyor.

**Yapman gerekenler:**

1. `sales_shuffled.csv` dosyasını oku.
2. Tarihe göre sırala ve index'i baştan numaralandır
   (`reset_index(drop=True)`).
3. İlk tarihi, son tarihi, satır sayısını ve ilk üç günün satışını liste
   olarak alt alta yazdır.

**Beklenen çıktı:**

```
2022-01-01
2024-12-31
1096
[305, 277, 201]
```

`reset_index(drop=True)` neden gerekli: sıralama satırları taşıyor ama eski
index numaralarını da yanlarında götürüyor. `iloc[0]` konuma baktığı için
yine doğru çalışırdı, ama sıralanmış bir tabloyu eski numaralarıyla bırakmak
ileride `loc` kullanınca kafa karıştırıyor.
