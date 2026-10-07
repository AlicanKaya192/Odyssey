Sırasız akışta dakikalık pencereleri 30 saniyelik su işaretiyle say ve
doğru sayılarla karşılaştır.

**Yapman gerekenler:**

1. Doğru sayılar: `payments(5_000)` (sırayla gelen akış) ile her dakikanın
   (`ts // 60 * 60`) ödeme sayısını bir sözlüğe say.
2. `payments(5_000, late=True)` ile aynı ödemeler sırasız geliyor. Açık
   pencereleri say; görülen en yeni `ts`'yi tut; su işareti `newest - 30`.
3. Penceresi su işaretini geçmiş (`start + 60 <= newest - 30`) bir ödeme
   gelirse onu sayma, `dropped`'u artır.
4. Su işareti bir pencerenin sonunu geçince pencereyi `results` sözlüğüne
   taşı. Akış bitince açık kalanları da taşı.
5. Yazdır: kaybolan ödeme sayısı, eksik sayılan pencere sayısı
   (`results`'taki sayı doğrusundan farklı olanlar) ve `results`'taki
   sayıların toplamı ile `dropped`'un toplamının 5000 olup olmadığı.

**Beklenen çıktı:**

```
197
91
True
```
