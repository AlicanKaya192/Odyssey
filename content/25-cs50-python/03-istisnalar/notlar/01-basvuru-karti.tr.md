Hafta 3'te geçen her şey tek sayfada.

## Hata türleri

| Hata | Ne zaman | Örnek |
|---|---|---|
| `SyntaxError` | kod okunamıyor, hiçbir satır çalışmaz | `print("hello)` |
| `ValueError` | değer uygun değil | `int("cat")`, `int("1.5")`, `int("")` |
| `NameError` | ad tanımlı değil | atanamamış `x`'i yazdırmak |
| `ZeroDivisionError` | sıfıra bölme | `10 / 0` |
| `IndexError` | listede o konum yok | `[1, 2][5]` |
| `KeyError` | sözlükte o anahtar yok | `{"a": 1}["b"]` |
| `EOFError` | girdi bitti (`Ctrl+D`, Windows'ta `Ctrl+Z` + Enter) | `input()` |

`int` baştaki/sondaki boşlukları ve eksiyi kabul eder: `int(" 42 ")` → `42`,
`int("-7")` → `-7`.

## try / except / else

```python
try:
    x = int(input("What's x? "))
except ValueError:
    print("x is not an integer")
else:
    print(f"x is {x}")
```

- `try`: dene; yalnızca hata verebilecek en az satır.
- `except Tür:` o tür hata çıkarsa çalışır; `try`'ın kalanı atlanır.
- `else:` hiç hata çıkmazsa çalışır.
- Türü yaz; çıplak `except:` beklemediğin hataları da yutar.

## Birden çok istisna

| Yazım | Ne yapar |
|---|---|
| `except ValueError:` + `except ZeroDivisionError:` | her türe ayrı cevap |
| `except (ValueError, ZeroDivisionError):` | ikisine aynı cevap |

## Yeniden sormak

```python
def get_int(prompt):
    while True:
        try:
            return int(input(prompt))
        except ValueError:
            pass
```

| Yazım | Ne yapar |
|---|---|
| `else: break` | döngüden çıkar |
| `return ...` | döngüden ve fonksiyondan çıkar, değeri verir |
| `pass` | hiçbir şey yapmaz, boş blok yerine |
| `continue` | döngünün başına döner |

## Girdi bitene kadar okumak

```python
while True:
    try:
        line = input()
    except EOFError:
        break
```
