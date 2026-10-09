Bir algoritma yazarken ve yazdıktan sonra elinin altında dursun diye kısa
bir kart.

## Beş özellik

| Özellik | Soru |
|---|---|
| Girdi | Algoritma neyle çalışıyor? Hangi türde, hangi aralıkta? |
| Çıktı | Ne döndürüyor? Girdi beklenmedikse ne döndürüyor? |
| Belirlilik | Her adım tek anlamlı mı? "Biraz bekle" değil, "8 dakika bekle". |
| Sonluluk | Her girdide bitiyor mu? Sonsuz döngüye girebileceği bir yol var mı? |
| Doğruluk | Her girdide doğru sonucu veriyor mu, yalnızca örnekte değil? |

## Yazmadan önce

1. Problemi kendi cümlenle yaz: girdi ne, çıktı ne?
2. Küçük bir örneği **elle** çöz ve ne yaptığını adım adım not et.
3. O adımları sözde kodla yaz.
4. Sözde kodu bir uç durumla (boş liste gibi) kâğıt üstünde dene.
5. Ancak sonra Python'a çevir.

## Uç durum kontrol listesi

- Boş girdi: `[]`, `""`, `0`
- Tek eleman: `[5]`
- Hepsi aynı: `[7, 7, 7]`
- Negatifler ve sıfır: `[-5, -2, 0]`
- Cevabın yeri: baş, son, orta
- Tekrar eden değerler: "ilk" mi "son" mu isteniyor?
- Çok büyük girdi: algoritma hâlâ makul sürede bitiyor mu?

## Başlangıç değeri tuzağı

"En büyük", "en küçük" gibi bir şeyi ararken başlangıç değerini **sabit
bir sayıyla** (`0`, `1000`) başlatma; verinin hangi aralıkta olduğunu
bilemezsin. İki güvenli yol var:

- İlk elemanla başlat: `largest = numbers[0]`.
- "Henüz yok" anlamına gelen değerle başlat: `largest = None` ve döngüde
  `if largest is None or number > largest:`.

Toplama işlemi gibi bir şeyde ise doğru başlangıç işlemin **etkisiz
elemanıdır**: toplamada `0`, çarpmada `1`.
