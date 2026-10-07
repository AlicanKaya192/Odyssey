Örneklem büyüdükçe tahminlerin ne kadar dağıldığını ölç.

**Yapman gerekenler:**

1. `orders = make_orders(200_000)`.
2. `n` için 200, 2 000 ve 20 000 değerlerini gez. Her `n` için
   `random_state` 0'dan 99'a 100 örneklem al ve her birinin ortalama
   `unit_price`'ını bir listeye koy.
3. Her `n` için bir satıra `n`'yi ve tahminlerin standart sapmasını
   (`np.std`, iki ondalık) yazdır.
4. Son satıra 200'lük örneklemdeki dağılımın 20 000'liktekine oranını (bir
   ondalık) yazdır.

**Beklenen çıktı:**

```
200 60.06
2000 19.37
20000 5.95
10.1
```

Örneklem yüz kat büyüdü, dağılım yaklaşık onda birine indi: karekök
kuralı.
