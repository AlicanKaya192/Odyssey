Bu kez iki anahtara göre grupla: hem şehir, hem not harfi.

**Yapman gerekenler:**

1. `city` **ve** `grade` sütunlarına göre grupla, not ortalamasını hesapla
   ve **bir basamağa yuvarla**; sonucu `result` adlı seride tut.
2. `result` serisini yazdır.
3. `result` serisini düzleştirip **boyutunu** yazdır.

**Beklenen çıktı:**

```
city    grade
Ankara  A        86.5
        B        88.0
Bursa   B        70.0
        C        68.0
Izmir   A        76.0
        B        74.0
        C        64.0
Name: score, dtype: float64
(7, 3)
```

**İki şeyi fark edeceksin:**

- Index'te **iki seviye** var. Boş görünen hücreler bir öncekiyle aynı
  demek; pandas tekrar yazmıyor.
- `reset_index()` bu seviyeleri sütuna çeviriyor ve elinde normal bir tablo
  kalıyor: 7 satır, 3 sütun (`city`, `grade`, `score`).

Çok seviyeli index'le çalışmak zahmetli; genelde ilk iş onu düzleştirmek
oluyor.
