Hafta 0'da geçen her şey tek sayfada.

## Terminal

| Komut | Ne yapar |
|---|---|
| `python hello.py` | `hello.py` dosyasını çalıştırır |
| `python` | etkileşimli kipi açar (`>>>`); çıkmak için `exit()` |
| yukarı ok | son komutu geri getirir |

## Fonksiyonlar

| Yazım | Ne yapar | Örnek |
|---|---|---|
| `print(a, b)` | argümanları aralarına boşlukla yazar, sona satır sonu koyar | `print("hello,", name)` |
| `print(a, end="")` | sona satır sonu koymaz (boşluk da koymaz) | `print("hello, ", end="")` |
| `print(a, b, sep="-")` | araya `-` koyar | `a-b` |
| `input("soru ")` | soruyu yazar, yazılanı **metin** olarak döndürür | `name = input("Name: ")` |
| `int(x)` / `float(x)` | metni sayıya çevirir | `int("42")` → `42` |
| `round(x)` / `round(x, 2)` | yuvarlar (sayı döndürür) | `round(2/3, 2)` → `0.67` |

## Dize metotları

Hepsi **yeni** bir dize döndürür; sonucu bir değişkene ata.

| Metot | Sonuç (`s = " Hello, World "`) |
|---|---|
| `s.strip()` | `"Hello, World"` |
| `s.lower()` / `s.upper()` | `" hello, world "` / `" HELLO, WORLD "` |
| `s.title()` | her kelimenin ilk harfi büyük |
| `s.replace(" ", "...")` | her boşluğun yerine `...` |
| `"$5".removeprefix("$")` | `"5"` |
| `"15%".removesuffix("%")` | `"15"` |

## Biçimli dize (f-string)

| Yazım | Sonuç |
|---|---|
| `f"hello, {name}"` | değişkenin değeri metne girer |
| `f"{z:,}"` | binlik ayırıcı: `1,000` |
| `f"{z:.2f}"` | virgülden sonra iki basamak: `0.67` |

## İşlemler

| İşlem | Anlamı | `7 ? 2` |
|---|---|---|
| `+ - *` | toplama, çıkarma, çarpma | `9`, `5`, `14` |
| `/` | bölme (her zaman float) | `3.5` |
| `//` | tam sayı bölmesi (aşağı yuvarlar) | `3` |
| `%` | bölmeden kalan | `1` |
| `**` | üs alma | `49` |

## Kendi fonksiyonun

```python
def main():
    x = int(input("What's x? "))
    print("x squared is", square(x))


def square(n):
    return n * n


main()
```

- `def ad(parametre):` tanımlar; gövde **girintili**.
- `return` değeri çağıran yere geri verir; `print` yalnızca ekrana yazar.
- Dosyanın sonundaki `main()` çağrısı olmadan hiçbir şey çalışmaz.
- `def hello(to="world"):` argüman verilmezse varsayılan değer kullanılır.
