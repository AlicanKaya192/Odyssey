Python'da bölmenin üç ayrı operatörü var ve üçü farklı şey verir. Bu alıştırmada
üçünü aynı sayı çiftinde göreceksin.

```python
a = 17
b = 5
```

Üç değişken oluştur:

| Değişken | Operatör | Ne yapar |
|---|---|---|
| `exact` | `/` | Tam bölme, sonuç ondalıklı |
| `whole` | `//` | Bölümün tam kısmı, ondalık atılır |
| `remainder` | `%` | Kalan |

Üçünü alt alta yazdır. Beklenen çıktı:

```
3.4
3
2
```

> `/` operatörü sonuç tam sayı çıksa bile **her zaman** ondalıklı verir:
> `10 / 2` sonucu `5` değil `5.0`'dır.
