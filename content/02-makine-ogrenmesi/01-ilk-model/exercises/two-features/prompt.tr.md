Dosyada `age` sütunu da var — evin yaşı. Modele ekleyince ne oluyor?

**Yapman gerekenler:**

1. Dosyayı oku. Bu kez `X`'e **iki sütun** al: `area` ve `age`.
2. Aynı şekilde ayır (dörtte biri test, `random_state=42`) ve modeli eğit.
3. İki katsayıyı **yan yana** yazdır (iki ondalık): önce `area`'nınki,
   sonra `age`'inki.
4. Ortalama mutlak hatayı yazdır (iki ondalık).
5. Tek özellikli modelin hatası **18.5** idi. Yeni model bundan iyiyse
   `better`, değilse `worse` yazdır.

**Beklenen çıktı:**

```
2.77 -3.35
7.13
better
```

**Kodun ne kadar az değiştiğine dikkat et:** yalnızca `X`'i kurduğun satır.
Ayırma, eğitme, ölçme aynı. sklearn'in tasarımı bunu böyle ucuz hâle
getiriyor.

**Katsayıların işareti bir şey anlatıyor:** metrekare artınca fiyat artıyor
(+2.77), yaş artınca düşüyor (-3.35). Kimse modele "eski evler ucuzdur"
demedi; sayılar veriden çıktı.

**İki uyarı:**

- **Katsayı sebep söylemiyor.** Doğru cümle "yaşı büyük olan evlerin fiyatı
  düşük çıkıyor"; "yaş fiyatı düşürüyor" değil.
- **3.35 > 2.77 diye "yaş daha önemli" denmiyor.** Metrekare 45 ile 165
  arasında, yaş 0 ile 30 arasında geziniyor. Katsayı sütunun birimine
  bağlı; birimleri farklı iki sayı kıyaslanmıyor. Kıyaslamak için önce
  ölçeklemek gerekiyor.
