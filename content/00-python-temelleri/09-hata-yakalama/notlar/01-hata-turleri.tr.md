Bu not bir sözlük. Ekranda bir hata gördüğünde adını buradan arayıp ne demek
istediğini bulabilirsin.

## `SyntaxError`

Kod çalışmadan önce çıkıyor. Python yazdığını ayrıştıramıyor.

```python
if score > 70
    print("passed")
```

```
SyntaxError: expected ':'
```

En sık sebepleri: iki nokta unutmak, parantez kapatmamak, koşulda `==` yerine
`=` yazmak.

**Bir tuzak:** Python bazen hatayı **bir sonraki** satırda gösteriyor. Açık
kalan bir parantez varsa, sorun onun olduğu satırda değil, Python'un pes
ettiği satırda görünüyor. Hata satırında bir şey bulamıyorsan bir üstüne bak.

## `IndentationError`

Girinti tutarsız. Python'da girinti sözdiziminin kendisi olduğu için bu ayrı
bir hata.

```python
def greet():
print("hello")
```

```
IndentationError: expected an indented block
```

Sekme ile boşluğu karıştırmak da aynı hataya yol açıyor — gözle aynı
görünüyorlar ama Python için farklılar.

## `NameError`

Tanımlanmamış bir ada ulaşmaya çalışıyorsun.

```python
print(totl)
```

```
NameError: name 'totl' is not defined
```

Genelde yazım yanlışı. Metni tırnak içine almayı unutmak da aynı hatayı
veriyor: `print(Hello)`.

## `TypeError`

İşlem, verilen tiplerle yapılamıyor.

```python
print("5" + 3)
```

```
TypeError: can only concatenate str (not "int") to str
```

Diğer sık hâlleri: fonksiyona eksik ya da fazla parametre vermek, fonksiyon
olmayan bir şeyi çağırmak.

## `ValueError`

Tip doğru ama değer o işlem için uygun değil.

```python
int("abc")
```

```
ValueError: invalid literal for int() with base 10: 'abc'
```

`TypeError` ile farkı önemli: `int([1, 2])` bir `TypeError` (liste sayıya
çevrilemez), `int("abc")` ise `ValueError` (metin çevrilebilir bir tip ama
bu metin çevrilemez).

## `ZeroDivisionError`

```python
100 / 0
```

```
ZeroDivisionError: division by zero
```

`%` ve `//` için de geçerli. Bölen bir değişkense bölmeden önce kontrol etmek
ya da yakalamak gerekiyor.

## `IndexError`

Listede olmayan bir sıra numarası.

```python
items = [1, 2, 3]
print(items[3])
```

```
IndexError: list index out of range
```

Üç elemanlı listede sıra numaraları 0, 1, 2. `items[3]` yok. Son elemana
`items[-1]` ile ulaşmak bu hatayı baştan engelliyor.

## `KeyError`

Sözlükte olmayan bir anahtar.

```python
prices = {"apple": 12}
print(prices["melon"])
```

```
KeyError: 'melon'
```

İki çözüm: önce `in` ile sormak, ya da `prices.get("melon", 0)` kullanmak.

## `AttributeError`

Nesnenin öyle bir özelliği ya da metodu yok.

```python
text = "hello"
text.push("x")
```

```
AttributeError: 'str' object has no attribute 'push'
```

Bu hata çoğu zaman elindeki şeyin sandığın tip olmadığını söylüyor. Bir
fonksiyon `None` döndürmüşse ve sen onun üzerinde metot çağırıyorsan
`'NoneType' object has no attribute ...` görüyorsun — en sık karşılaşılan
hâli bu.

## `FileNotFoundError`

```python
open("data.csv")
```

```
FileNotFoundError: [Errno 2] No such file or directory: 'data.csv'
```

Dosya yok ya da başka bir klasörde. Program hangi klasörde çalışıyorsa yollar
ona göre çözülüyor.

## `ModuleNotFoundError`

```python
import pandas
```

```
ModuleNotFoundError: No module named 'pandas'
```

Modül kurulu değil ya da adını yanlış yazmışsın. Kendi dosyan içinse dosya
çalıştırdığın dosyayla aynı klasörde değildir.

## `RecursionError`

Kendini çağıran bir fonksiyon durmamış.

```
RecursionError: maximum recursion depth exceeded
```

Python belli bir derinlikten sonra duruyor. Çıkış koşulunun eksik ya da hiç
tutmadığı anlamına geliyor.

## Hepsinin ortak atası

Bu hataların hepsi `Exception` denen ortak bir türden geliyor. Bu yüzden
`except Exception:` yazmak neredeyse hepsini yakalıyor.

Neredeyse — çünkü `KeyboardInterrupt` (Ctrl+C) ve `SystemExit` dışarıda
kalıyor. İyi ki de kalıyor: `except Exception:` yazan bir program Ctrl+C ile
kapatılabiliyor.

Yine de `except Exception:` yazmadan önce iki kez düşün. Beklediğin hatayı
yazmak her zaman daha iyi.
