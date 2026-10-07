Ödemeleri `minilog` konusuna yaz, ofsetlerle parça parça oku ve kopyaları
ayıklayarak ciroyu bul.

**Yapman gerekenler:**

1. `topic = Topic("payments", partitions=3)`. `payments(3_000, duplicates=True)`
   akışındaki her ödemeyi anahtarı kart, değeri olayın kendisi olacak
   şekilde gönder.
2. Bölüm başına kayıt sayısını (`end_offset`) bir liste olarak yazdır.
3. Tüketici: `offsets = {0: 0, 1: 0, 2: 0}`. Her bölümü, sonuna gelene
   kadar `read(bölüm, ofset, max_records=250)` ile oku; her partiden sonra
   ofseti son kaydın ofsetinin bir fazlası yap.
4. Okunan kayıt sayısını ve kopyaları `event_id` ile ayıklayarak farklı
   ödeme sayısını yazdır.
5. Ayıklanmış ciroyu (iki ondalık) yazdır ve kopyasız akışın
   (`payments(3_000)`) cirosuyla aynı olup olmadığını yazdır (ikisini de iki
   ondalığa yuvarla).

**Beklenen çıktı:**

```
[949, 949, 1199]
3097 3000
360332.69
True
```
