Bu bölümün hataları çoğunlukla **sessiz**: sorgu çalışıyor, sonuç geliyor,
ama sorduğun soruyu cevaplamıyor. Sunucu bunu söyleyemez.

## "Zaten sıralı geliyordu"

En pahalı hata bu.

`ORDER BY` yazmadığın bir sorgu bugün `id` sırasında gelebilir. Sunucu
tabloyu en hızlı bulduğu yoldan okuyor ve bu yol; tablo büyüyünce, bir
indeks eklenince ya da sunucu sürümü değişince başkalaşıyor.

Geliştirme sırasında doğru görünen bir rapor, aylar sonra üretimde
karışık sırada çıkıyor ve kimse ne değiştiğini bulamıyor. Değişen şey
sorgu değil, sunucunun tercihi.

**Sıra önemliyse yaz.** Önemli değilse de yazmakta bir zarar yok.

## `TOP` var, `ORDER BY` yok

```sql
SELECT TOP 5 ad FROM urunler;
```

Bu sorgu "beş ürün" getiriyor ama **hangi beşi** belirsiz. "En pahalı
beş" ya da "en yeni beş" demek istiyorsan sıralamayı yazman gerekiyor.

Hata vermiyor, bir sonuç veriyor — bu yüzden gözden kaçıyor.

## `DESC` yalnızca bir sütuna uygulandı

```sql
ORDER BY kategori, fiyat DESC
```

Buradaki `DESC` **yalnızca `fiyat`** için. `kategori` hâlâ artan. İkisini
de tersine çevirmek istiyorsan:

```sql
ORDER BY kategori DESC, fiyat DESC
```

Bu, sonuç sırası biraz tuhaf göründüğünde ilk bakılacak yer.

## `DISTINCT` beklendiği kadar elemedi

```sql
SELECT DISTINCT kategori, ad FROM urunler;
```

"Kategorileri tekilleştireyim" diye yazılıyor ama sekiz satırın sekizi de
geliyor. Çünkü `DISTINCT` **satırın tamamına** bakıyor ve her `ad` farklı.

Tek bir sütunun benzersiz değerlerini istiyorsan yalnızca o sütunu seç.

## `WHERE` içinde takma ad

```sql
SELECT fiyat AS tutar FROM urunler WHERE tutar > 1000;
```

Bu **hata veriyor** — `Invalid column name 'tutar'`. Sunucu `WHERE`'i
`SELECT`'ten önce çalıştırıyor, o sırada takma ad yok.

Aynı takma ad `ORDER BY` içinde çalışıyor, çünkü o en sonda.

Bu bölümde bu ikisini yan yana görmek işe yarıyor: aynı ad, aynı sorgu,
bir yerde çalışıyor bir yerde çalışmıyor. Sebep tek: **çalışma sırası**.

## Kontrol alışkanlığı

Sıralamalı bir sorguda üç şeye bak:

1. **Kaç satır geldi?** Beklediğin sayıyla aynı mı?
2. **İlk satır doğru mu?** En pahalıyı istediysen gerçekten en pahalı mı?
3. **Son satır doğru mu?** Sıralamanın yönünü en hızlı bu gösteriyor.

Üçü de tutuyorsa sıralama neredeyse kesin doğrudur.
