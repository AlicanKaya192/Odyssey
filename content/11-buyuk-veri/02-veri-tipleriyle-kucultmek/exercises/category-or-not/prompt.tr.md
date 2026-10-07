Dört metin sütununun her biri için `category`'nin işe yarayıp
yaramadığını ölçerek karar ver.

**Yapman gerekenler:**

1. `make_orders(100_000)` ile `df` tablosunu kur.
2. `order_time`, `city`, `category` ve `payment` sütunlarını döngüyle gez.
3. Her sütun için:
   - farklı değer sayısını (`nunique()`),
   - `str` olarak kilobaytını,
   - `category` olarak kilobaytını,
   - `category` daha küçükse `yes`, değilse `no` yazısını
   bir satıra yazdır. Kilobaytlar `memory_usage(deep=True) / 1024`, bir
   ondalık.

**Beklenen çıktı:**

```
order_time 99830 2636.8 3035.2 no
city 8 1412.8 97.9 yes
category 6 1393.5 97.9 yes
payment 3 1249.7 97.8 yes
```

Üç sütunda kazanç onda birin altına iniyor; neredeyse her değeri farklı
olan `order_time`'da ise kategori daha pahalı.
