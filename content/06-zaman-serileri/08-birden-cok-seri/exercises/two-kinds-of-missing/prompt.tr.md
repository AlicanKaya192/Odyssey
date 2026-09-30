Geniş tabloda iki mağazanın `NaN`'leri var ve iki farklı anlama geliyor:
C pazarları **kapalı**, D 1 Mayıs'tan önce **yok**.

**Yapman gerekenler:**

1. `stores.csv` dosyasını oku ve geniş biçime çevir.
2. C'nin `NaN` olduğu günlerin haftanın hangi günü olduğunu göster: o
   tarihlerin `day_name()` değerlerinin farklı olanlarını liste olarak
   yazdır.
3. C için iki ortalamayı bir ondalığa yuvarlayıp aynı satıra yazdır:
   `NaN`'ler atlanarak ve `fillna(0)` ile.
4. D için aynı iki ortalamayı aynı satıra yazdır.
5. Dört mağazanın günlük toplamını hesapla (`wide.sum(axis=1)`) ve 30 Nisan
   ile 1 Mayıs 2024 değerlerini aynı satıra yazdır.
6. Yalnızca yıl boyunca var olan üç mağazanın (A, B, C) toplamını hesapla ve
   aynı iki günün değerlerini aynı satıra yazdır.

**Beklenen çıktı:**

```
['Sunday']
248.5 213.2
170.9 114.4
626.0 775.0
626.0 669.0
```

C'nin iki ortalaması da anlamlı: biri açık gün başına, öteki takvim günü
başına. D'nin ikinci ortalaması ise yanlış: olmayan dört ayı sıfır satışlı
sayıyor. Dört mağazalı toplam 1 Mayıs'ta sıçrıyor çünkü toplama yeni bir seri
girdi; üç mağazalı toplamda böyle bir kırılma yok.
