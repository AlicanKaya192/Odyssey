Bir depodaki stok sayıları `int8`'e zorlanırsa ne olur? Bozulan
değerleri bul, sonra doğru yolla küçült.

**Yapman gerekenler:**

1. `stock = pd.Series([90, 120, 250, 300, 40])` serisini kur.
2. `stock.astype("int8")` sonucunu `forced` adıyla al ve liste olarak
   yazdır.
3. Kaç değerin bozulduğunu yazdır: `(forced != stock).sum()`.
4. Bozulan değerlerin **asıl** hâllerini liste olarak yazdır.
5. Doğru yol: `pd.to_numeric(stock, downcast="integer")` sonucunun türünü
   ve listesini aynı satıra yazdır.

**Beklenen çıktı:**

```
[90, 120, -6, 44, 40]
2
[250, 300]
int16 [90, 120, 250, 300, 40]
```

`astype` sessizce bozdu; `downcast` değerlerin sığdığı türü (`int16`)
seçti.
