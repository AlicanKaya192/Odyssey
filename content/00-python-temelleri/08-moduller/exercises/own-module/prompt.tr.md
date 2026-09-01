Bu alıştırmada senin dosyanın **yanında** `toolbox.py` diye ikinci bir dosya
duruyor. İçeriği şu:

```python
# toolbox.py

TAX_RATE = 0.20


def with_tax(price):
    return price + price * TAX_RATE


def discount(price, percent):
    return price - price * percent / 100
```

Bu dosyayı sen yazmadın ama o da bir modül — `math` ile arasında hiçbir fark
yok. İçindekileri kullanmak için önce getirmen gerekiyor.

Dikkat et: modülün içinde sadece fonksiyon yok, `TAX_RATE` diye bir **değer**
de var. Ona da aynı şekilde ulaşabilirsin.

**Yapman gerekenler:**

1. `toolbox` modülünü getir.
2. `price` değişkeni `250`. Üç değişken oluştur:

| Değişken | İçinde ne olacak |
|---|---|
| `final_price` | Fiyatın vergili hâli |
| `sale_price` | Fiyata yüzde 10 indirim uygulanmış hâli |
| `rate` | Modüldeki vergi oranı |

3. Üçünü **alt alta** yazdır.

**Beklenen çıktı:**

```
300.0
225.0
0.2
```
