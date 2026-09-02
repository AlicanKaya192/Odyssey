Aykırı değeri gözle değil **kuralla** bulacaksın.

Başlangıç kodunda bir `values` serisi var: bir haftalık günlük sipariş
sayıları.

**Yapman gerekenler:**

1. Birinci ve üçüncü çeyreği hesapla, ikisini **yan yana** yazdır.
2. Alt ve üst sınırı hesapla (çeyrekler açıklığının 1.5 katı), **yan yana**
   yazdır.
3. Sınırların dışında kalan değerleri **liste hâlinde** yazdır.
4. Serinin ortalamasını (iki ondalık) ve medyanını **yan yana** yazdır.

**Beklenen çıktı:**

```
49.75 52.25
46.0 56.0
[140]
61.62 50.5
```

**IQR kuralı nedir:** `quantile(0.25)` verinin dörtte birinin altında kaldığı
değer, `quantile(0.75)` dörtte üçünün. Aradaki mesafeye **çeyrekler
açıklığı** deniyor ve verinin orta yarısının yayılımını gösteriyor. Bu
mesafenin 1.5 katı dışına çıkan her şey aykırı sayılıyor.

**Son satır neden önemli:** 140 tek bir değer, ama ortalamayı 50'den 61.6'ya
çıkarıyor. Medyan 50.5'te duruyor. Aykırı değer şüphesi varken medyan daha
güvenilir bir özet.

Ve şunu unutma: kural aykırıyı **buluyor**, silinip silinmeyeceğine karar
vermiyor. 140 sipariş bir veri hatası da olabilir, kampanya günü de.
