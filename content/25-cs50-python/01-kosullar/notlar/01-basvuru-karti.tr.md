Hafta 1'de geçen her şey tek sayfada.

## Karşılaştırma işleçleri

Hepsi `True` ya da `False` (`bool`) verir.

| İşleç | Anlamı | `x = 3` için |
|---|---|---|
| `x < 5` / `x > 5` | küçük / büyük | `True` / `False` |
| `x <= 3` / `x >= 4` | küçük ya da eşit / büyük ya da eşit | `True` / `False` |
| `x == 3` | eşit | `True` |
| `x != 3` | eşit değil | `False` |
| `1 < x < 5` | zincirleme: `1 < x and x < 5` | `True` |

## Mantık işleçleri

| İşleç | Ne zaman `True` | Örnek |
|---|---|---|
| `a and b` | ikisi de doğruysa | `True and False` → `False` |
| `a or b` | biri doğruysa | `True or False` → `True` |
| `not a` | `a` yanlışsa | `not True` → `False` |

`or`'un iki yanı da tam koşul olmalı: `name == "Harry" or name == "Ron"`.

## if / elif / else

```python
if score >= 90:
    print("A")
elif score >= 80:
    print("B")
else:
    print("F")
```

- Koşulun sonunda `:`, blok girintili (4 boşluk).
- Sorular sırayla sorulur; **ilk doğru** olanın bloğu çalışır, gerisi atlanır.
- `elif` istediğin kadar olur; `else` en fazla bir tane ve en sonda, koşulsuz.

## Mod

| Yazım | Sonuç |
|---|---|
| `10 % 3` | `1` (bölmeden kalan) |
| `n % 2 == 0` | `n` çiftse `True` |

## bool döndüren fonksiyon

| Yazım | Ne zaman |
|---|---|
| `if ...: return True` / `else: return False` | uzun hâli |
| `return True if n % 2 == 0 else False` | koşullu ifade |
| `return n % 2 == 0` | en kısası: karşılaştırma zaten `bool` |

Koşullu ifade genel olarak `A if koşul else B`: koşul doğruysa `A`, değilse `B`.

## match

```python
match name:
    case "Harry" | "Hermione" | "Ron":
        print("Gryffindor")
    case "Draco":
        print("Slytherin")
    case _:
        print("Who?")
```

- Değer her `case` ile sırayla karşılaştırılır; uyan ilk durum çalışır.
- `|` birkaç değeri tek durumda birleştirir.
- `case _:` her şeye uyar (`else` gibi); en sona yazılır.

## Problem setinde işine yarayacak dize metotları

| Metot | Sonuç |
|---|---|
| `"hello, world".startswith("hello")` | `True` |
| `"cat.gif".endswith(".gif")` | `True` |
| `"1 + 1".split(" ")` | `['1', '+', '1']` |
| `x, y, z = "1 + 1".split(" ")` | üç parçayı üç değişkene açar |
| `"7:30".split(":")` | `['7', '30']` |
