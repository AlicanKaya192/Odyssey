Bir satış hesabı yazacaksın.

`total_price` adında bir fonksiyon tanımla. Üç parametre alsın:

| Parametre | Anlamı |
|---|---|
| `price` | ürünün birim fiyatı |
| `count` | kaç adet alındığı |
| `discount` | uygulanacak indirim — **varsayılan değeri 0** |

Fonksiyon toplam tutarı hesaplayıp `return` ile geri versin:
birim fiyat çarpı adet, eksi indirim.

Sonra fonksiyonu iki kez çağır:

- `full` değişkenine, 50 liralık üründen 3 adet **indirimsiz** al.
- `reduced` değişkenine, aynı alışverişi **20 lira indirimle** al.

İkisini alt alta ekrana yazdır.

Beklenen çıktı:

```
150
130
```

> Fonksiyonun içinde `print` kullanma. Sonucu `return` ile geri ver, yazdırma
> işini dışarıda yap.
