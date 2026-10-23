# İstisnalar

CS50 Python'un dördüncü haftası. Videoyu **Video** sekmesinden izleyebilirsin;
bu sayfa dersin yazılı hâli. **İstisnalar** (exceptions) program çalışırken
ortaya çıkan sorunlardır: kodun içinde bir şeylerin ters gitmesi.

## Sözdizimi hataları

`hello.py` adında bir dosya açıp bilerek bir hata yapalım, tırnaklardan birini
unutalım:

```python
print("hello, world)
```

```text
$ python hello.py
  File "hello.py", line 1
    print("hello, world)
          ^
SyntaxError: unterminated string literal (detected at line 1)
```

Python bir **sözdizimi hatası** (syntax error) bildiriyor. Python dosyayı
çalıştırmadan önce baştan sona okur; sözdizimi hatası varsa hiçbir satır
çalışmaz. Bu tür hataların çaresi kodu dikkatle gözden geçirip düzeltmektir;
bu hafta göreceğimiz araçlar onlara işe yaramaz.

## Çalışma anı hataları

**Çalışma anı hataları** (runtime errors) ise kod beklenmedik bir şeyle
karşılaşınca çıkar. Örneğin kullanıcıdan sayı bekliyorsun, o bir harf yazıyor.
`number.py`:

```python
x = int(input("What's x? "))
print(f"x is {x}")
```

```text
$ python number.py
What's x? 50
x is 50
```

Başındaki `f`, süslü parantezlerin içindekinin (`x`'in değerinin) metne
yazılacağını söylüyor. Kullanıcının sayı yerine kolayca bir kelime yazacağını,
hatta hiçbir şey yazmadan Enter'a basacağını düşünebilirsin. `cat` yazınca:

```text
$ python number.py
What's x? cat
Traceback (most recent call last):
  File "number.py", line 1, in <module>
    x = int(input("What's x? "))
ValueError: invalid literal for int() with base 10: 'cat'
```

`int` fonksiyonu `cat` metnini sayıya çeviremiyor ve bir `ValueError`
(değer hatası) fırlatıyor. Programcı olarak **savunmacı** olmalıyız:
kullanıcının beklediğimiz şeyi yazdığından emin olmalıyız. Bunun yolu
**hata yakalamak** (error handling).

## try

Python'da `try` (dene) ve `except` (hariç, şu hata olursa) kullanıcının
girdisini bir şey ters gitmeden önce sınamanın yoludur:

```python
try:
    x = int(input("What's x? "))
    print(f"x is {x}")
except ValueError:
    print("x is not an integer")
```

```text
$ python number.py
What's x? cat
x is not an integer
```

`50` yazınca kabul edilir; `cat` yazınca kullanıcı neden kabul edilmediğini
söyleyen bir mesaj görür. Hata yine olur, ama Python programı çökertmek
yerine `except` bloğuna atlar.

Yine de bu en iyi yazım değil: `try` içinde iki satır var. İyi alışkanlık,
`try`'a yalnızca **hata verebileceğinden endişe ettiğin en az satırı**
koymaktır. Öyle yapalım:

```python
try:
    x = int(input("What's x? "))
except ValueError:
    print("x is not an integer")

print(f"x is {x}")
```

```text
$ python number.py
What's x? cat
x is not an integer
Traceback (most recent call last):
  File "number.py", line 6, in <module>
    print(f"x is {x}")
                  ^
NameError: name 'x' is not defined
```

Amacımıza ulaştık ama yeni bir hata çıktı: `NameError`, `x` tanımlı değil.
Neden? Atama **sağdan sola** çalışır: önce `int(input(...))` hesaplanır, sonra
sonuç `x`'e atanır. `int` başarısız olunca atama hiç gerçekleşmez; son satırda
yazdırılacak bir `x` yoktur.

## else

`try`'ın bu tür bir durumu ele almanın başka bir yolu var: `else`. `try`
bloğunda hiç hata çıkmazsa `else` bloğu çalışır.

```python
try:
    x = int(input("What's x? "))
except ValueError:
    print("x is not an integer")
else:
    print(f"x is {x}")
```

```text
$ python number.py
What's x? 50
x is 50
```

```text
$ python number.py
What's x? cat
x is not an integer
```

<figure class="fig"><div class="flow"><span class="node">try: dene</span><span class="arrow">→</span><span class="node no">hata çıktı mı?</span><span class="arrow">→</span><span class="node">evetse except</span><span class="arrow">→</span><span class="node ok">hayırsa else</span></div><figcaption><code>try</code> bloğundaki satırlar denenir. Bir <code>ValueError</code> çıkarsa Python bloğun kalanını bırakıp <code>except</code>'e atlar; hiç hata çıkmazsa <code>except</code> atlanır ve <code>else</code> çalışır.</figcaption></figure>

Bir de şuna bak: kullanıcıya biraz kaba davranıyoruz. Sayı yazmazsa program
bitiveriyor. Bir döngüyle sayı gelene kadar yeniden soralım:

```python
while True:
    try:
        x = int(input("What's x? "))
    except ValueError:
        print("x is not an integer")
    else:
        break

print(f"x is {x}")
```

```text
$ python number.py
What's x? cat
x is not an integer
What's x? dog
x is not an integer
What's x? 50
x is 50
```

`while True` sonsuza kadar döner; kullanıcı doğru girdiyi verince `else`
içindeki `break` döngüden çıkar ve sonuç yazılır. Yanlış yazan kullanıcıya
yeniden sorulur.

## Tam sayı alan bir fonksiyon

Kullanıcıdan tam sayı almak istediğimiz çok yer olacak. İşi bir fonksiyona
verelim:

```python
def main():
    x = get_int()
    print(f"x is {x}")


def get_int():
    while True:
        try:
            x = int(input("What's x? "))
        except ValueError:
            print("x is not an integer")
        else:
            break
    return x


main()
```

```text
$ python number.py
What's x? cat
x is not an integer
What's x? 7
x is 7
```

Tam sayı alma işini soyutladık; programın kendisi artık ilk üç satırdan
ibaret. Daha da iyileşir: `return` yalnızca fonksiyondan değer döndürmekle
kalmaz, içindeki döngüden de çıkar. `break` ile ayrı bir `return`'e gerek
yok:

```python
def main():
    x = get_int()
    print(f"x is {x}")


def get_int():
    while True:
        try:
            x = int(input("What's x? "))
        except ValueError:
            print("x is not an integer")
        else:
            return x


main()
```

Bazıları şunu da savunur: çevirme başarılıysa değeri `try`'ın içinden
doğrudan döndürmek. Aynı işi daha az satırla yapar:

```python
def main():
    x = get_int()
    print(f"x is {x}")


def get_int():
    while True:
        try:
            return int(input("What's x? "))
        except ValueError:
            print("x is not an integer")


main()
```

```text
$ python number.py
What's x? cat
x is not an integer
What's x? 7
x is 7
```

## pass

Kullanıcıyı her seferinde uyarmak yerine sorusunu sessizce yeniden sormak
istersek `pass` kullanırız. `pass` "hiçbir şey yapma" demek; Python boş bir
blok kabul etmediği için onun yerine yazılır:

```python
def main():
    x = get_int()
    print(f"x is {x}")


def get_int():
    while True:
        try:
            return int(input("What's x? "))
        except ValueError:
            pass


main()
```

```text
$ python number.py
What's x? cat
What's x? 7
x is 7
```

Bazen kullanıcıya hatanın ne olduğunu açıkça söylemek istersin, bazen yalnızca
yeniden sormak yeter. Son bir iyileştirme: soru metni şu an `get_int`'in içine
gömülü. Fonksiyona soruyu argüman olarak verelim; böylece her çağrıda başka
bir soru sorabilir:

```python
def main():
    x = get_int("What's x? ")
    print(f"x is {x}")


def get_int(prompt):
    while True:
        try:
            return int(input(prompt))
        except ValueError:
            pass


main()
```

```text
$ python number.py
What's x? cat
What's x? 7
x is 7
```

## Problem seti için iki ek

Bu haftanın problem setinde CS50'nin derste kısaca geçtiği iki şey daha
gerekiyor.

**Birden çok istisna.** Bir `try`'a birden çok `except` yazılabilir; Python
çıkan hataya uyan ilkini çalıştırır. Sıfıra bölmek `ZeroDivisionError`
fırlatır:

```python
try:
    x = int(input("x: "))
    y = int(input("y: "))
    print(x / y)
except ValueError:
    print("not an integer")
except ZeroDivisionError:
    print("cannot divide by zero")
```

```text
$ python divide.py
x: 1
y: 0
cannot divide by zero
```

Aynı şeyi yapacaksan iki türü tek satırda da yakalayabilirsin:
`except (ValueError, ZeroDivisionError):`.

**Girdinin sonu.** Kullanıcı girdiyi bitirmek için `Ctrl+D` (Windows'ta
`Ctrl+Z` ve Enter) basınca `input()` bir `EOFError` fırlatır (EOF, *end of
file*, dosyanın sonu). Kaç satır geleceğini bilmediğin programlarda döngü
bununla biter:

```python
total = 0
while True:
    try:
        n = int(input("Number: "))
    except EOFError:
        print()
        break
    total += n

print("Total:", total)
```

```text
$ python total.py
Number: 3
Number: 4
Number: 
Total: 7
```

Odyssey'de alıştırmaları denetlerken girdiyi sen yazmıyorsun: denetim her
durumun satırlarını veriyor ve sonunda girdiyi bitiriyor.

## Özet

Hatalar kaçınılmazdır; ama bugün öğrendiklerinle önüne geçebilirsin:

- İstisnalar, sözdizimi ve çalışma anı hataları
- `ValueError`, `NameError`, `ZeroDivisionError`, `EOFError`
- `try`, `except` ve `try`'a en az satırı koymak
- `else` ve `while True` ile yeniden sormak
- `return` ile döngüden çıkmak, `pass` ile sessizce devam etmek

## Bu haftanın problem seti

**Alıştırma** sekmesindeki yedi alıştırma bu dersin konularını tek tek
çalıştırıyor. **Problem Seti** sekmesindeki dördü CS50'nin bu haftaki ödevi
(Problem Set 3):

| Problem | Ne istiyor | Dersteki konu |
|---|---|---|
| Yakıt Göstergesi | `3/4` → `75%`, geçersizse yeniden sor | iki istisna, `round` |
| Felipe's Taqueria | siparişin toplamını tutmak | `EOFError`, sözlük |
| Alışveriş Listesi | ürünleri sayıp sıralamak | `EOFError`, sözlükle sayma |
| Eski Usul Tarih | `9/8/1636` → `1636-09-08` | `ValueError` ile yeniden sor |

Alışveriş listesi dersin göstermediği `sorted`'ı, tarih problemi `index`'i
kullanıyor; yönergelerde ipucu olarak yazılı.

---

*Bu bölüm, Harvard Üniversitesi'nin [CS50's Introduction to Programming with Python](https://cs50.harvard.edu/python/) dersinin 3. haftasından (ders notu ve problem seti) çevrilip uyarlanmıştır; örnekler ve alıştırmalar değiştirildi, problem seti CS50'nin check50'siyle değil Odyssey'nin denetimiyle sınanıyor. Özgün içerik ve bu uyarlama [CC BY-NC-SA 4.0](https://creativecommons.org/licenses/by-nc-sa/4.0/) lisanslıdır. Harvard bu uyarlamayı onaylamış değildir.*
