Günlük satışı eğitim ve test olarak ayır ve tahminin indeksini kur.

Başlangıç kodunda seri 3 Aralık 2024'e kadar kesilmiş hâlde `s` olarak hazır.

**Yapman gerekenler:**

1. Son 28 günü test, öncesini eğitim yap: `train = s.iloc[:-28]`,
   `test = s.iloc[-28:]`.
2. Eğitim ve test uzunluklarını aynı satıra yazdır.
3. Eğitimin son tarihini ve testin ilk tarihini aynı satıra yazdır
   (`.date()`).
4. Ufku `h = len(test)` al ve gelecek tarihlerin indeksini kur:
   `pd.date_range(train.index[-1] + pd.Timedelta(days=1), periods=h, freq="D")`.
5. Bu indeksin ilk ve son tarihini aynı satıra yazdır.
6. Kurduğun indeks testin indeksiyle aynı mı? `future.equals(test.index)`
   sonucunu yazdır.
7. Eğitim ve testin ortalamasını bir ondalığa yuvarlayıp aynı satıra yazdır.

**Beklenen çıktı:**

```
1040 28
2024-11-05 2024-11-06
2024-11-06 2024-12-03
True
255.1 331.1
```

Test, eğitimin bittiği günün ertesi günü başlıyor ve aralarında hiçbir
çakışma yok. Testin ortalaması eğitimden belirgin biçimde yüksek: seri
büyüyor ve yıl sonuna yaklaşıyoruz. Geçmişin ortalamasını tahmin olarak
kullanmak bu yüzden kötü bir fikir olacak.
