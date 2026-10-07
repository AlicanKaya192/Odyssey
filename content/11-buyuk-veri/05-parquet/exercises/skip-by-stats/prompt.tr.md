Yalnızca Mart 2024 siparişlerini, gereken satır gruplarını okuyarak bul.

**Yapman gerekenler:**

1. Başlangıç kodu 200 000 siparişi 20 000 satırlık gruplarla yazıyor
   (10 grup).
2. `start = pd.Timestamp("2024-03-01")` ve
   `end = pd.Timestamp("2024-04-01")` tanımla.
3. Mart siparişi **içerebilecek** grupları seç: grubun en büyük zamanı
   `start`'tan küçük **değilse** ve en küçük zamanı `end`'den küçükse.
   Seçilen grup numaralarını liste olarak yazdır.
4. Yalnızca o grupları `read_row_group` ile oku ve birleştir; okunan satır
   sayısını yazdır.
5. Okunanları `start <= order_time < end` ile süz; Mart sipariş sayısını
   yazdır.

**Beklenen çıktı:**

```
[1, 2]
40000
16591
```

On grubun yalnızca bir kısmı okundu; geri kalanı istatistikten anlaşılıp
atlandı.
