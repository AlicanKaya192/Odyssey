`find ... -delete` ve `find ... -exec rm {} \;` güçlüdür: yüzlerce dosyayı tek
satırda siler ve **geri alınmaz**. Terminalde çöp kutusu yoktur.

## Üç adım

1. **Listele.** Komutu silmeden çalıştır:
   `find project -name '*.bak'`
2. **Oku.** Listede yalnızca silmek istediklerin mi var? Sayısı beklediğin gibi
   mi? Gerekirse `| wc -l`.
3. **Aynı komuta** `-delete` ekle. Yeniden yazma; ok tuşuyla önceki komutu
   getirip sonuna ekle. Böylece listelediğin ile sildiğin aynı olur.

## Sık yapılan hatalar

- **Kalıpta tırnak yok.** `find . -name *.bak -delete` bulunduğun klasördeki
  bir dosyanın adına dönüşebilir ve beklemediğin şeyi siler (ya da hiçbir şeyi).
- **`-delete` öne yazılmış.** find koşulları soldan sağa işler; `-delete`
  koşullardan önce gelirse koşul uygulanmadan **her şeyi** siler. `-delete` hep
  en sonda.
- **Koşulsuz -delete.** `find project -delete` projenin tamamını siler.
- **Yanlış başlangıç yolu.** `find / ...` bütün diske bakar. Başlangıç yolunu
  olabildiğince dar tut.

## Silmeden önce taşımak

Emin değilsen silme, taşı:

```bash
mkdir ../trash
find project -name '*.bak' -exec mv {} ../trash/ \;
```

Bir şey eksik çıkarsa geri getirirsin.
