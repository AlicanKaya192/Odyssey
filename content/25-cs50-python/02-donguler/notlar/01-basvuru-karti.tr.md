Hafta 2'de geçen her şey tek sayfada.

## while

```python
i = 0
while i < 3:
    print("meow")
    i += 1
```

- Koşul doğru olduğu sürece blok yeniden çalışır.
- Koşulu bir gün yanlış yapacak satırı unutma (`i += 1`); yoksa sonsuz döngü.
- Sonsuz döngüyü durdurmak: terminalde `Ctrl+C`.

## for ve range

| Yazım | Değerler |
|---|---|
| `range(3)` | `0, 1, 2` |
| `range(1, 4)` | `1, 2, 3` |
| `range(0, 10, 3)` | `0, 3, 6, 9` (üçer üçer) |
| `range(5, 0, -1)` | `5, 4, 3, 2, 1` (geriye) |
| `for _ in range(3):` | değer kullanılmıyorsa `_` |
| `for c in "cat":` | bir dizeyi harf harf gezer |

## Döngü denetimi

| Anahtar kelime | Ne yapar |
|---|---|
| `break` | döngüden hemen çıkar |
| `continue` | turun kalanını atlayıp sonraki tura geçer |
| `return` (fonksiyonda) | fonksiyondan, dolayısıyla döngüden de çıkar |

Girdi denetimi kalıbı:

```python
while True:
    n = int(input("What's n? "))
    if n > 0:
        break
```

## Liste

| Yazım | Sonuç (`s = ["Hermione", "Harry", "Ron"]`) |
|---|---|
| `s[0]` | `"Hermione"` (konum 0'dan başlar) |
| `s[2]` | `"Ron"` |
| `s[3]` | `IndexError` |
| `len(s)` | `3` |
| `for x in s:` | elemanları sırayla gezer |
| `for i in range(len(s)):` | konumları gezer (`0, 1, 2`) |

## Sözlük

| Yazım | Sonuç |
|---|---|
| `d = {"Harry": "Gryffindor"}` | anahtar `"Harry"`, değer `"Gryffindor"` |
| `d["Harry"]` | `"Gryffindor"` |
| `d["Luna"]` | `KeyError` (anahtar yok) |
| `for k in d:` | **anahtarları** gezer; değer `d[k]` |
| `None` | "değer yok" |

## Dizeyle tekrar

| Yazım | Sonuç |
|---|---|
| `"-" * 5` | `"-----"` |
| `print("meow\n" * 3, end="")` | üç satır `meow`, sonda boş satır yok |
| `print("#", end="")` | satır sonu koymadan yazar |
| `print()` | yalnızca satır sonu |
