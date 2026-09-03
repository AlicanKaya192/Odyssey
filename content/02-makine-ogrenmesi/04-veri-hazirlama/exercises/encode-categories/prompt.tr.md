Önceki alıştırmada iki sütunu dışarıda bıraktık: `fuel` ve `gearbox`.
Metin oldukları için modele giremiyorlardı. Şimdi girecekler.

**Yapman gerekenler:**

1. Dosyayı oku. Bu kez **beş** sütun al: `age`, `km`, `engine`, `fuel`,
   `gearbox`. Hedef yine `price`.
2. `fuel` ve `gearbox` sütunlarını **one-hot** kodla — her kategori kendi
   sütunu olsun.
3. Kodlamadan sonra kaç sütun olduğunu yazdır.
4. Sütun adlarını **sıralı** olarak yazdır.
5. Ayır (`random_state=42`), `engine` eksiklerini **eğitim** ortalamasıyla
   doldur, modeli eğit.
6. MAE'yi yazdır (iki ondalık).
7. Önceki alıştırmada MAE **32.58** idi. Yeni model bundan iyiyse `better`,
   değilse `worse` yazdır.

**Beklenen çıktı:**

```
8
['age', 'engine', 'fuel_diesel', 'fuel_lpg', 'fuel_petrol', 'gearbox_auto', 'gearbox_manual', 'km']
16.42
better
```

**Hata yarıya indi:** 32.58 → 16.42. Yakıt türü ve vites fiyatı gerçekten
belirliyormuş; sayısal olmadıkları için dışarıda kalmışlardı.

**Neden her kategoriye ayrı sütun:** `petrol=0, diesel=1, lpg=2` demek
modele `lpg`'nin `petrol`'ün iki katı, `diesel`'in tam ortası olduğunu
öğretirdi. Böyle bir sıra yok. One-hot kodlama, sıra uydurmadan üç
kategoriyi de anlatıyor.

**Sıra gerçekten varsa durum değişiyor:** `düşük < orta < yüksek` ya da
`ilkokul < lise < üniversite` için `0, 1, 2` doğru — buna sıralı (ordinal)
kodlama deniyor.

**Bir tuzak:** yüzlerce kategorisi olan bir sütun (şehir, ürün kodu)
one-hot ile yüzlerce sütun üretiyor. 120 satırlık bir veride bu, özellik
sayısını örnek sayısına yaklaştırıyor ve model ezberlemeye başlıyor.
