Bir tablonun tek bir sütununu almak, veri işlerinin en sık yapılan
adımlarından biri.

**Yapman gerekenler:**

1. `records` listesi başlangıç kodunda hazır.
2. Bütün kayıtların `city` değerlerini bir listede topla ve `cities` adlı
   değişkende tut. Sıra bozulmasın.
3. `cities` listesini yazdır.
4. Kaç **farklı** şehir olduğunu yazdır.

**Beklenen çıktı:**

```
['Ankara', 'Izmir', 'Ankara', 'Izmir', 'Bursa']
3
```

pandas'ta bu iş `data["city"]` ve `data["city"].nunique()` olacak.
