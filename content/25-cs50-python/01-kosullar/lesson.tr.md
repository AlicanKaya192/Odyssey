# Koşullar

CS50 Python'un ikinci haftası. Videoyu **Video** sekmesinden izleyebilirsin;
bu sayfa dersin yazılı hâli. Şimdiye kadar programların her satırı sırayla
çalışıyordu. Bu hafta programın **karar vermesini** öğreniyoruz: bir koşula
göre bir yolu ya da ötekini seçmek, yol ayrımında sağa ya da sola sapmak gibi.

## Karşılaştırma işleçleri

Python iki değeri karşılaştıran **işleçlerle** (operator) gelir. Her biri bir
soru sorar ve cevabı `True` (doğru) ya da `False` (yanlış) olur:

| İşleç | Anlamı |
|---|---|
| `>` / `<` | büyüktür / küçüktür |
| `>=` / `<=` | büyük ya da eşit / küçük ya da eşit |
| `==` | eşittir |
| `!=` | eşit değildir |

`==`'deki çift eşittir işaretine dikkat: tek `=` **atama** yapar (sağdakini
soldaki ada bağlar), çift `==` **karşılaştırır**. Bu ikisini karıştırmak bu
haftanın en sık hatası.

## if

`compare.py` adında bir dosya açalım:

```python
x = int(input("What's x? "))
y = int(input("What's y? "))

if x < y:
    print("x is less than y")
```

```text
$ python compare.py
What's x? 1
What's y? 2
x is less than y
```

Program iki sayıyı alıp tam sayıya çeviriyor, sonra `if` (eğer) satırında
`x < y` diye soruyor. Cevap `True` ise altındaki **girintili** satır çalışır;
`False` ise atlanır. `if` satırının sonundaki iki nokta (`:`) "blok başlıyor"
demek; bloğa ait satırlar içeri itilir.

`True` ile `False`'un türü `bool`'dur (Boolean, adını mantıkçı George Boole'dan
alır). `if` her zaman bir `bool`'a bakarak karar verir.

## Akış denetimi: elif ve else

Üç durumu da ele alalım:

```python
x = int(input("What's x? "))
y = int(input("What's y? "))

if x < y:
    print("x is less than y")
if x > y:
    print("x is greater than y")
if x == y:
    print("x is equal to y")
```

```text
$ python compare.py
What's x? 2
What's y? 1
x is greater than y
```

Çıktı doğru, ama program her seferinde **üç soruyu da** soruyor. Oysa üçü
birden doğru olamaz: `x < y` doğruysa ötekileri sormanın anlamı yok. Kodun
hangi sırayla çalıştığına **akış denetimi** (control flow) denir ve burada
gereğinden uzun bir akış var. `elif` ("değilse eğer") önceki koşul yanlışsa
sorulur:

```python
x = int(input("What's x? "))
y = int(input("What's y? "))

if x < y:
    print("x is less than y")
elif x > y:
    print("x is greater than y")
elif x == y:
    print("x is equal to y")
```

<figure class="fig"><div class="flow"><span class="node">x &lt; y ?</span><span class="arrow">→</span><span class="node">hayırsa x &gt; y ?</span><span class="arrow">→</span><span class="node">hayırsa else</span></div><figcaption>Bir <code>if</code> / <code>elif</code> / <code>else</code> zincirinde sorular sırayla sorulur ve <b>ilk doğru olanın</b> bloğu çalışır; sonrakiler hiç sorulmaz.</figcaption></figure>

Bir adım daha: `x` ne küçük ne büyükse, eşit olmak zorundadır. Son soruyu
sormaya gerek yok; `else` (değilse) "geri kalan her durum" demek ve koşulu
yoktur:

```python
x = int(input("What's x? "))
y = int(input("What's y? "))

if x < y:
    print("x is less than y")
elif x > y:
    print("x is greater than y")
else:
    print("x is equal to y")
```

```text
$ python compare.py
What's x? 2
What's y? 2
x is equal to y
```

Bilgisayarın için bu birkaç soru fark etmez; ama günde milyarlarca kez çalışan
bir sunucuda gereksiz her soru zaman demek. Az soru soran kod hem hızlı hem
okunur.

## or

`or` (ya da) iki koşuldan **biri** doğruysa doğrudur:

```python
x = int(input("What's x? "))
y = int(input("What's y? "))

if x < y or x > y:
    print("x is not equal to y")
else:
    print("x is equal to y")
```

```text
$ python compare.py
What's x? 1
What's y? 2
x is not equal to y
```

Daha da iyisi: "küçük ya da büyük" demek "eşit değil" demektir. Tek soru yeter:

```python
x = int(input("What's x? "))
y = int(input("What's y? "))

if x != y:
    print("x is not equal to y")
else:
    print("x is equal to y")
```

```text
$ python compare.py
What's x? 3
What's y? 3
x is equal to y
```

## and

`and` (ve) iki koşul da doğruysa doğrudur. Bir not programı, `grade.py`:

```python
score = int(input("Score: "))

if score >= 90 and score <= 100:
    print("Grade: A")
elif score >= 80 and score < 90:
    print("Grade: B")
elif score >= 70 and score < 80:
    print("Grade: C")
elif score >= 60 and score < 70:
    print("Grade: D")
else:
    print("Grade: F")
```

```text
$ python grade.py
Score: 95
Grade: A
```

Python karşılaştırmaları **zincirlemeye** izin verir; `score >= 90 and score
<= 100` yerine matematikteki gibi yazılabilir (başka dillerde pek yoktur):

```python
score = int(input("Score: "))

if 90 <= score <= 100:
    print("Grade: A")
elif 80 <= score < 90:
    print("Grade: B")
elif 70 <= score < 80:
    print("Grade: C")
elif 60 <= score < 70:
    print("Grade: D")
else:
    print("Grade: F")
```

```text
$ python grade.py
Score: 85
Grade: B
```

Daha da sadeleşir. Bir `elif`'e gelindiyse üstteki koşulun yanlış olduğunu
biliyoruz: `score >= 80`'e ulaşan biri zaten 90'ın altında. Üst sınırları
yazmaya gerek yok:

```python
score = int(input("Score: "))

if score >= 90:
    print("Grade: A")
elif score >= 80:
    print("Grade: B")
elif score >= 70:
    print("Grade: C")
elif score >= 60:
    print("Grade: D")
else:
    print("Grade: F")
```

```text
$ python grade.py
Score: 72
Grade: C
```

Daha az soru, daha kolay okunan ve ileride değiştirmesi daha kolay bir
program. (CS50'nin notunda bu iki örneğin satırları fazladan girintili
yazılmış; o hâliyle Python `IndentationError` verir. Burada çalıştırılarak
doğrulanmış hâlleri var.)

Üç mantık işlecinin hepsi bir arada, `not` (değil) de dahil:

```python
print(True and False)
print(True or False)
print(not True)
print(1 < 2 < 3)
print(3 > 2 > 2)
```

```text
$ python logic.py
False
True
False
True
False
```

Son satır `3 > 2 and 2 > 2` demek; ikinci kısım yanlış olduğu için `False`.

## Mod

Matematikte **parite** (parity) bir sayının tek mi çift mi olduğudur. Mod
işleci `%` bölmeden kalanı verir: bir sayı 2'ye tam bölünüyorsa kalan 0'dır.

```python
print(4 % 2)
print(3 % 2)
print(10 % 3)
```

```text
$ python parity.py
0
1
1
```

`parity.py`:

```python
x = int(input("What's x? "))

if x % 2 == 0:
    print("Even")
else:
    print("Odd")
```

```text
$ python parity.py
What's x? 7
Odd
```

## Kendi parite fonksiyonumuz

Geçen hafta gördüğümüz gibi işi bir fonksiyona vermek kodu düzenler.
`is_even` (çift mi?) `True` ya da `False` **döndürsün**:

```python
def main():
    x = int(input("What's x? "))
    if is_even(x):
        print("Even")
    else:
        print("Odd")


def is_even(n):
    if n % 2 == 0:
        return True
    else:
        return False


main()
```

```text
$ python parity.py
What's x? 4
Even
```

`if is_even(x):` satırında hiçbir karşılaştırma işleci yok, ama çalışıyor:
fonksiyon bir `bool` döndürüyor ve `if` doğrudan ona bakıyor.

## Pythonic

Bir şeyi Python'a özgü, okunur ve kısa biçimde yazmaya **Pythonic** denir.
Dört satırlık `if` / `else`, tek satırlık bir **koşullu ifadeye** dönüşebilir:
`A if koşul else B` (koşul doğruysa A, değilse B):

```python
def is_even(n):
    return True if n % 2 == 0 else False


print(is_even(4), is_even(7))
```

```text
$ python parity.py
True False
```

Neredeyse İngilizce bir cümle gibi okunuyor. Ama bir adım daha var:
`n % 2 == 0` zaten `True` ya da `False`. Onu doğrudan döndürmek yeter:

```python
def is_even(n):
    return n % 2 == 0


print(is_even(4), is_even(7))
print(4 % 2 == 0)
```

```text
$ python parity.py
True False
True
```

## match

Uzun bir `if` / `elif` zinciri bir değeri sırayla birkaç olasılıkla
karşılaştırıyorsa `match` daha okunur olabilir. Önce `if` ile, *Harry
Potter*'daki binalar:

```python
name = input("What's your name? ")

if name == "Harry":
    print("Gryffindor")
elif name == "Hermione":
    print("Gryffindor")
elif name == "Ron":
    print("Gryffindor")
elif name == "Draco":
    print("Slytherin")
else:
    print("Who?")
```

```text
$ python house.py
What's your name? Hermione
Gryffindor
```

İlk üç koşul aynı şeyi yazıyor; `or` ile birleşir:

```python
name = input("What's your name? ")

if name == "Harry" or name == "Hermione" or name == "Ron":
    print("Gryffindor")
elif name == "Draco":
    print("Slytherin")
else:
    print("Who?")
```

```text
$ python house.py
What's your name? Draco
Slytherin
```

Burada sık yapılan bir hataya dikkat: `or`'un iki yanı da tam bir koşul
olmalı. `name == "Harry" or "Hermione"` yazarsan sağ taraf `name ==
"Hermione"` değil, yalnızca `"Hermione"` olur ve boş olmayan her metin doğru
sayılır. Sonuç: herkes Gryffindor'a düşer.

```python
name = input("What's your name? ")

# Yanlış: "Hermione" tek başına her zaman doğru sayılır
if name == "Harry" or "Hermione":
    print("Gryffindor")
else:
    print("Who?")
```

```text
$ python house.py
What's your name? Draco
Gryffindor
```

Aynı programı `match` ile yazalım. `match` değeri sırayla her `case`
(durum) ile karşılaştırır; uyan ilk durumun bloğu çalışır ve eşleşme biter.
`case _:` her şeye uyar, yani `else`'in görevini görür:

```python
name = input("What's your name? ")

match name:
    case "Harry":
        print("Gryffindor")
    case "Hermione":
        print("Gryffindor")
    case "Ron":
        print("Gryffindor")
    case "Draco":
        print("Slytherin")
    case _:
        print("Who?")
```

```text
$ python house.py
What's your name? Padma
Who?
```

Birkaç değer aynı `case`'te `|` (ya da) ile birleşebilir:

```python
name = input("What's your name? ")

match name:
    case "Harry" | "Hermione" | "Ron":
        print("Gryffindor")
    case "Draco":
        print("Slytherin")
    case _:
        print("Who?")
```

```text
$ python house.py
What's your name? Ron
Gryffindor
```

## Özet

Artık programların sorular sorup cevaba göre davranabiliyor:

- Karşılaştırma işleçleri (`<`, `>`, `<=`, `>=`, `==`, `!=`) ve `bool`
- `if`, `elif`, `else` ve akış denetimi
- `or`, `and`, `not` ve zincirleme karşılaştırma
- Mod (`%`) ile tek/çift
- `bool` döndüren kendi fonksiyonların
- Pythonic yazım ve koşullu ifade
- `match`, `case`, `|` ve `case _`

## Bu haftanın problem seti

**Alıştırma** sekmesindeki yedi alıştırma bu dersin konularını tek tek
çalıştırıyor. **Problem Seti** sekmesindeki beşi CS50'nin bu haftaki ödevi
(Problem Set 1):

| Problem | Ne istiyor | Dersteki konu |
|---|---|---|
| Derin Düşünce | `42` ya da `forty-two` ise `Yes` | `or`, `lower`, `strip` |
| Home Federal Tasarruf Bankası | selama göre `$0`, `$20`, `$100` | `if` / `elif`, `startswith` |
| Dosya Uzantıları | uzantıya göre ortam türü | uzun `elif` zinciri, `endswith` |
| Matematik Yorumlayıcısı | `1 + 1` gibi ifadeyi hesaplamak | `split`, `if` / `elif` |
| Yemek Vakti | saate göre öğün | `convert`, zincirleme karşılaştırma |

Bazı problemler dersin göstermediği küçük bir metodu (`startswith`,
`endswith`, `split`) kullanıyor; CS50 de öğrenciyi belgeye yolluyor.
Yönergelerde ipucu olarak yazılı.

---

*Bu bölüm, Harvard Üniversitesi'nin [CS50's Introduction to Programming with Python](https://cs50.harvard.edu/python/) dersinin 1. haftasından (ders notu ve problem seti) çevrilip uyarlanmıştır; örnekler ve alıştırmalar değiştirildi, problem seti CS50'nin check50'siyle değil Odyssey'nin denetimiyle sınanıyor. Özgün içerik ve bu uyarlama [CC BY-NC-SA 4.0](https://creativecommons.org/licenses/by-nc-sa/4.0/) lisanslıdır. Harvard bu uyarlamayı onaylamış değildir.*
