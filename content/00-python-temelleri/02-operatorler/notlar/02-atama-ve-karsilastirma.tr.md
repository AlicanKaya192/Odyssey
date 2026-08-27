Bu notta iki grup operatör var: bir değişkeni güncelleyenler ve iki değeri karşılaştıranlar.

## Kısaltılmış atama

Bir değişkenin üzerine ekleme yapmanın uzun yolu şudur:

```python
total = 0
total = total + 5
```

Kısası:

```python
total = 0
total += 5
```

İkisi aynı şeyi yapar. `+=` operatörü "önce topla, sonra geri ata" demek.

Bütün aritmetik operatörlerin kısaltılmış hâli var:

| Kısa | Uzun karşılığı |
|---|---|
| `x += 3` | `x = x + 3` |
| `x -= 3` | `x = x - 3` |
| `x *= 3` | `x = x * 3` |
| `x /= 3` | `x = x / 3` |
| `x //= 3` | `x = x // 3` |
| `x %= 3` | `x = x % 3` |
| `x **= 3` | `x = x ** 3` |

Bu kısaltmalar özellikle döngülerde işe yarar — bir sonraki bölümde bir listedeki sayıları toplarken `total += number` yazacaksın.

## Karşılaştırma operatörleri

Bunlar bir soru sorar ve cevabı `True` ya da `False` olarak verir:

| Operatör | Sorusu | Örnek | Sonuç |
|---|---|---|---|
| `==` | eşit mi? | `5 == 5` | `True` |
| `!=` | farklı mı? | `5 != 3` | `True` |
| `>` | büyük mü? | `5 > 3` | `True` |
| `<` | küçük mü? | `5 < 3` | `False` |
| `>=` | büyük veya eşit mi? | `5 >= 5` | `True` |
| `<=` | küçük veya eşit mi? | `5 <= 3` | `False` |

## En sık yapılan hata

`=` ile `==` farklı şeyler:

```python
age = 18      # ATAMA:      age değişkenine 18 koy
age == 18     # KARŞILAŞTIRMA: age 18'e eşit mi? (True/False üretir)
```

Bir koşul yazarken yanlışlıkla `=` kullanırsan Python sana `SyntaxError` verir. Bu aslında iyi haber — hata sessizce geçmiyor.

## Mantıksal operatörler

Birden fazla koşulu birleştirmek için `and`, `or` ve `not` kullanılır:

```python
age = 25
has_ticket = True

print(age >= 18 and has_ticket)   # True  -> ikisi de doğru olmalı
print(age >= 65 or has_ticket)    # True  -> biri yeterli
print(not has_ticket)             # False -> tersini alır
```

Türkçe karşılıkları düşünmek işi kolaylaştırır: `and` = "ve", `or` = "veya", `not` = "değil".

Bir sonraki bölümde bunları `if` ile birlikte kullanacaksın; asıl işe yaradıkları yer orası.
