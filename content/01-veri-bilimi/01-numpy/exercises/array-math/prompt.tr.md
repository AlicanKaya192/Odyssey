Dört ürünün birim fiyatı ve satış adedi elinde. Her ürünün cirosunu ve
vergili hâlini hesaplayacaksın — **döngü yazmadan.**

**Yapman gerekenler:**

1. `prices` ve `counts` dizileri başlangıç kodunda hazır.
2. Her ürünün cirosunu hesapla (`fiyat x adet`) ve `totals` adlı diziye koy.
3. Cirolara %20 vergi ekle ve `with_tax` adlı diziye koy.
4. Şunları yazdır: `totals`, virgülden sonra bir basamağa yuvarlanmış
   `with_tax`, ve toplam ciro.

**Beklenen çıktı:**

```
[300 250 400 800]
[360. 300. 480. 960.]
1750
```

**Kural:** boş liste kurup `append` ile doldurmak yok. Bütün işi dizi
üzerinde tek satırda yapabilirsin — bölümün konusu bu.
