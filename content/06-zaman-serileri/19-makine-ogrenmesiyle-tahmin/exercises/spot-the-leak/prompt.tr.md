Tek bir `shift` unutulunca ne olduğunu ölç.

Başlangıç kodunda doğru tablo (`table`) hazır.

**Yapman gerekenler:**

1. Doğru tabloyla doğrusal regresyon kur (eğitim 2023 sonuna kadar) ve 2024
   test hatasını iki ondalıkla yazdır.
2. Hatalı bir tablo kur: `table`'ın kopyasında `mean7` sütununu
   `s.rolling(7).mean()` ile değiştir (kaydırma yok; `.reindex(table.index)`
   ile hizala). Aynı modeli kur ve test hatasını yazdır.
3. İki tabloda `mean7` ile hedefin (`y`) korelasyonunu üç ondalıkla aynı
   satıra yazdır (önce doğru tablo).
4. Hatalı modelin katsayılarından `mean7`'ninkini ve doğru modeldeki
   karşılığını iki ondalıkla aynı satıra yazdır (önce doğru model).
5. Hatalı özelliğin 10 Mart 2024 değeri hangi günleri kapsıyor? O değeri ve
   4–10 Mart satışlarının ortalamasını bir ondalıkla aynı satıra yazdır.

**Beklenen çıktı:**

```
11.51
10.55
0.662 0.671
0.14 1.19
282.6 282.6
```

Hata "iyileşti" ve hiçbir uyarı çıkmadı. Ama hatalı `mean7`, 10 Mart'ın
kendisini de içeriyor (4–10 Mart); hedefle korelasyonu yükseldi ve model ona
daha çok yaslandı. Gerçek kullanımda 10 Mart'ın satışını bilmeden o ortalamayı
hesaplayamazsın; bu sonuç asla tekrarlanamaz.
