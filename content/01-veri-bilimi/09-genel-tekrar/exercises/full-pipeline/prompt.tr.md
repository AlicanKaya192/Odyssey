Modülün tamamı bu alıştırmada. Ham tablo yedi satır ve üç ayrı sorun
taşıyor: tutarsız şehir adları, metin gelen notlar, tekrar eden bir kayıt ve
iki eksik değer.

**Yapman gerekenler:**

1. Ham veriden bir kopya al.
2. `city` sütununu temizle ve baş harfleri büyük olacak şekilde tekleştir.
3. `score` sütununu sayıya çevir — çevrilemeyen değer boş olsun.
4. **Kaç satırla başladığını** bir değişkende tut.
5. `id` sütununa göre tekrar eden kayıtları at, kalan satır sayısını bir
   değişkende tut.
6. Notu boş olan **kaç kayıt kaldığını** say.
7. Notu boş olan satırları at.
8. Dört sayıyı **tek satırda yan yana** yazdır: başlangıç, tekrarsız,
   eksik, kalan.
9. Şehre göre sayı ve ortalamayı yazdır.

**Beklenen çıktı:**

```
7 6 2 4
        count  mean
city
Ankara      2  86.5
Izmir       2  71.0
```

**Dikkat edilecek üç şey:**

- **Sıra:** şehri düzeltmeden gruplarsan `"Izmir "` ile `"Izmir"` ayrı grup
  oluyor.
- **`"abc"` bir hata değil**, veriden gelen kirlilik. `errors="coerce"` onu
  boşa çevirip programı yürütüyor.
- **Sayılar rapora giriyor:** yedi kayıtla başlayıp dörtle bitirdin. Bunu
  yazmayan bir analiz, okuyanın bilmediği bir şeyi saklıyor.

Ve son satıra bak: Bursa tamamen kayboldu, çünkü tek kaydının notu boştu.
