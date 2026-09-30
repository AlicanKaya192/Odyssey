Satış günlük, hedef aylık (`targets.csv`: `month`, `store`, `target`).
İkisini aynı sıklığa getirip hedefin ne kadarının tutturulduğunu bul.

**Yapman gerekenler:**

1. İki dosyayı oku (`stores.csv` için `parse_dates=["date"]`).
2. Satış tablosuna ay sütunu ekle:
   `long["date"].dt.to_period("M").astype(str)`.
3. Ay ve mağaza bazında toplam satışı hesapla
   (`groupby(["month", "store"])["sales"].sum().reset_index()`).
4. Hedef tablosuyla `on=["month", "store"]` üzerinden birleştir ve
   `pct = sales / target * 100` sütununu bir ondalığa yuvarlayarak ekle.
5. Haziran 2024 için her mağazanın `pct` değerini `mağaza pct` biçiminde alt
   alta yazdır.
6. Hedefin tutturulduğu (`pct >= 100`) satır sayısını ve toplam satır
   sayısını aynı satıra yazdır.
7. En düşük `pct` değerine sahip satırın ayını, mağazasını ve `pct` değerini
   aynı satıra yazdır.

**Beklenen çıktı:**

```
A 93.2
B 92.4
C 94.4
D 89.8
27 44
2024-06 D 89.8
```

Günlük satış aya indirildi; aylık hedef günlere kopyalanmadı. Hedef bir
toplam: günlere kopyalasaydın her ay hedefi gün sayısı kadar şişerdi.
