# Fonksiyonlar ve Değişkenler

CS50 Python'un ilk haftası. Videoyu **Video** sekmesinden izleyebilirsin; bu
sayfa dersin yazılı hâli. Kodları Odyssey'nin alıştırma ekranında ya da kendi
bilgisayarında deneyebilirsin. Hafta bitince adını soran, metni düzelten,
hesap yapan ve kendi fonksiyonlarını yazan programların olacak.

## Python ile kod yazmak

Bir program, bilgisayarın sırayla yaptığı komutların listesidir. Python
programı düz bir metin dosyasıdır ve adı `.py` ile biter. CS50'de ilk dosyanın
adı `hello.py`; içine tek satır yazılıyor:

```python
print("hello, world")
```

Programı çalıştırmak için **terminal** (komut satırı) kullanılır. Terminal,
bilgisayara yazıyla komut verdiğin penceredir. `$` işareti "komut yazabilirsin"
demek; sen `python hello.py` yazıp Enter'a basıyorsun:

```text
$ python hello.py
hello, world
```

Bilgisayar aslında yalnızca sıfırları ve birleri anlar. `python` komutu bir
**yorumlayıcı** (interpreter) çalıştırır: senin yazdığın metni okuyup
bilgisayarın yapabileceği adımlara çevirir. Neredeyse her programcının ilk
programı budur: ekrana `hello, world` yazmak. Tebrikler, ilk programın hazır.

## Fonksiyonlar

**Fonksiyon** (function), bilgisayarın ya da dilin zaten bildiği bir iştir;
bir fiil gibi düşün. `print` "ekrana yaz" fiilidir. Parantezin içine verdiğin
değere **argüman** (argument) denir: burada argüman `"hello, world"` metni ve
`print` onu terminale yazıyor.

## Hatalar (bug)

Koddaki yanlışlara **bug** denir ve programlamanın doğal bir parçasıdır;
herkes yapar. Kapanış parantezini unuttuğunu düşün:

```python
print("hello, world"
```

```text
$ python hello.py
  File "hello.py", line 1
    print("hello, world"
         ^
SyntaxError: '(' was never closed
```

Python dosyayı çalıştırmadan önce baştan sona okur ve kapanmamış bir parantez
görünce durur. Mesaj hatanın yerini (`line 1`) ve sebebini (`'(' was never
closed`, "parantez hiç kapanmadı") söylüyor. Hata mesajları çoğu zaman ipucu
verir; her zaman bu kadar açık olmasalar da önce son satırı okumak iyi bir
alışkanlıktır.

## İlk programı kişiselleştirmek

Programın kullanıcıyla konuşsun. `input` başka bir fonksiyon: argüman olarak
bir **soru metni** (prompt) alır, onu yazar ve kullanıcının yazıp Enter'a
basmasını bekler.

```python
input("What's your name? ")
print("hello, world")
```

```text
$ python hello.py
What's your name? David
hello, world
```

Soru soruldu, `David` yazıldı ama program yine `hello, world` dedi: yazılan
ad hiçbir yerde saklanmadı. Saklamak için değişken gerekiyor.

### Değişkenler

**Değişken** (variable), programın içinde bir değeri tutan kaptır; bir
etiket gibi bir ad verirsin, değeri o adla kullanırsın.

```python
name = input("What's your name? ")
print("hello, name")
```

Ortadaki `=` matematikteki eşittir değil, **atama**dır: önce sağ taraf
çalışır (`input` soruyu sorar, yazılanı **döndürür**), sonra o değer soldaki
`name` adına bağlanır. Ama çıktıya bak:

```text
$ python hello.py
What's your name? David
hello, name
```

Tırnak içindeki her şey düz metindir; oradaki `name` kelimesinin değişkenle
ilgisi yok. Değişkeni kullanmak için tırnağın dışına yazmak gerekiyor:

```python
name = input("What's your name? ")
print("hello,")
print(name)
```

```text
$ python hello.py
What's your name? David
hello,
David
```

Ad artık geliyor, ama iki ayrı satırda. Buna birazdan bakacağız.

### Yorumlar

**Yorum** (comment), `#` ile başlayan ve Python'un hiç çalıştırmadığı
satırdır. Kendine ve kodu okuyacak başkalarına not bırakırsın: bu kod ne
yapıyor, neden böyle.

```python
# Kullanıcıya adını sor
name = input("What's your name? ")
print("hello,")
print(name)
```

Yorumlar bir yapılacaklar listesi gibi de kullanılabilir.

### Sözde kod

**Sözde kod** (pseudocode), bir işi nasıl yapacağını henüz bilmediğinde
adımları önce düz cümlelerle yorum olarak yazmaktır. Sonra her yorumun altına
o adımın kodunu yazarsın:

```python
# Kullanıcıya adını sor
name = input("What's your name? ")

# "hello," yaz
print("hello,")

# Yazılan adı yaz
print(name)
```

## Programı biraz daha iyileştirmek

İki dizeyi `+` ile **birleştirebilirsin** (concatenation). `"hello, "`
sonundaki boşluğa dikkat; o olmasa ad virgüle yapışırdı:

```python
name = input("What's your name? ")
print("hello, " + name)
```

Bazı fonksiyonlar birden çok argüman alır. `print`'e virgülle ayrılmış iki
argüman verince ikisini **aralarına bir boşluk koyarak** yazar:

```python
name = input("What's your name? ")
print("hello,", name)
```

```text
$ python hello.py
What's your name? David
hello, David
```

## Dizeler ve parametreler

**Dize** (string), Python'da `str`, bir metin parçasıdır: harfler,
rakamlar, boşluklar, hepsi bir arada.

Fonksiyonların davranışını değiştiren **parametreleri** vardır. `print`'in
belgesine bakınca iki önemli parametresini görürsün:

- `end`: yazdıktan sonra sona ne konacağı. Varsayılanı `"\n"`, yani **satır
  sonu**. Bu yüzden her `print` yeni bir satıra geçiyor; iki `print` ad ile
  selamı iki satıra bölmüştü.
- `sep`: argümanların arasına ne konacağı. Varsayılanı tek boşluk `" "`.

`end=""` verince satır sonu kalkar:

```python
name = input("What's your name? ")
print("hello,", end="")
print(name)
```

```text
$ python hello.py
What's your name? David
hello,David
```

Aynı satıra geldi ama `hello,` ile `David` bitişti: `end=""` satır sonunu
siler, yerine boşluk koymaz. (CS50'nin notu burada `hello, David` yazıyor;
çalıştırınca bitişik çıkıyor.) Boşluğu kendin koyarsan düzelir:

```python
name = input("What's your name? ")
print("hello, ", end="")
print(name)
```

```text
$ python hello.py
What's your name? David
hello, David
```

`sep` ile araya ne geleceğini seçersin:

```python
print("hello", "world", sep=", ")
print("a", "b", "c", sep="-")
```

```text
$ python hello.py
hello, world
a-b-c
```

Kısacası **parametre**, fonksiyonun kabul ettiği argümanın adıdır (`end`,
`sep`); **argüman**, çağırırken ona verdiğin değerdir (`""`, `", "`).

### Tırnak işaretiyle küçük bir sorun

Dizenin içine çift tırnak koymak istersen Python dizenin nerede bittiğini
karıştırır:

```python
print("hello,"friend"")
```

```text
$ python hello.py
  File "hello.py", line 1
    print("hello,"friend"")
                  ^^^^^^
SyntaxError: invalid syntax. Is this intended to be part of the string?
```

İki çözüm var: dizeyi **tek tırnakla** aç, ya da içerideki tırnağın önüne
**ters bölü** (`\`) koy. Ters bölü "bir sonraki karakter dizenin sonu değil,
dizenin parçası" demektir; buna **kaçış** (escape) denir.

```python
print('hello, "friend"')
print("hello, \"friend\"")
```

```text
$ python hello.py
hello, "friend"
hello, "friend"
```

## Biçimli dizeler (f-string)

Dizeyle değişkeni birleştirmenin en okunur yolu **biçimli dize**dir
(formatted string, kısaca f-string). Dizenin başına `f` yazarsın; süslü
parantezin `{}` içindeki değişkenin değeri metne yerleşir:

```python
name = input("What's your name? ")
print(f"hello, {name}")
```

```text
$ python hello.py
What's your name? David
hello, David
```

Bu derste f-string'i çok sık kullanacaksın.

## Dizelerle daha fazlası

Kullanıcının hep istediğin gibi yazacağını **asla** varsayma. Adından önce ve
sonra boşluk bırakabilir, küçük harfle yazabilir. Dizelerin hazır
**metotları** (method) var: bir dizeye nokta koyup çağırdığın fonksiyonlar.
`strip` baştaki ve sondaki boşlukları siler:

```python
name = input("What's your name? ")

# Baştaki ve sondaki boşlukları sil
name = name.strip()

print(f"hello, {name}")
```

```text
$ python hello.py
What's your name?     David   
hello, David
```

Dikkat: `name.strip()` `name`'i değiştirmez, temizlenmiş **yeni** bir dize
döndürür. O yüzden sonucu yine `name`'e atıyoruz (`name = name.strip()`).
`title` her kelimenin ilk harfini büyütür:

```python
name = input("What's your name? ")
name = name.strip()

# Her kelimenin ilk harfini büyüt
name = name.title()

print(f"hello, {name}")
```

```text
$ python hello.py
What's your name?    david malan  
hello, David Malan
```

Metotlar art arda çağrılabilir; her biri öncekinin döndürdüğü dizeyle
çalışır. Hatta `input`'un döndürdüğü dizeye doğrudan uygulanabilir:

```python
name = input("What's your name? ").strip().title()
print(f"hello, {name}")
```

Hangisinin daha iyi olduğu tartışılır: tek satır kısa ama yoğun, ayrı satırlar
uzun ama okunur. Terminalde yukarı ok tuşu son komutunu geri getirir;
`python hello.py`'yi her seferinde yeniden yazman gerekmez.

Problem setinde işine yarayacak birkaç metot daha:

```python
text = "Hello, World"
print(text.lower())
print(text.upper())
print(text.replace("World", "CS50"))
print("$50.00".removeprefix("$"))
print("15%".removesuffix("%"))
```

```text
$ python methods.py
hello, world
HELLO, WORLD
Hello, CS50
50.00
15
```

- `lower` / `upper`: bütün harfleri küçük / büyük yapar.
- `replace(eski, yeni)`: her `eski`'nin yerine `yeni` koyar.
- `removeprefix` / `removesuffix`: baştaki / sondaki belirli metni atar
  (yoksa dizeye dokunmaz).

## Tam sayılar (int)

Python'da tam sayının türü `int` (integer). Bildiğin işlemler var: `+`, `-`,
`*`, `/`. İki tane de yeni:

- `//` **tam sayı bölmesi**: sonucu aşağı yuvarlar.
- `%` **mod**: bölmeden kalanı verir (`7 = 2 × 3 + 1`, kalan 1).

```python
print(7 + 2)
print(7 - 2)
print(7 * 2)
print(7 / 2)
print(7 // 2)
print(7 % 2)
```

```text
$ python calculator.py
9
5
14
3.5
3
1
```

Terminale yalnızca `python` yazarsan `>>>` işaretli **etkileşimli kip**
(interactive mode) açılır ve `1 + 1` gibi satırları anında çalıştırırsın. Bu
derste çok kullanılmayacak ama hızlı denemeler için kullanışlı.

Bir hesap makinesi yazalım, `calculator.py`:

```python
x = 1
y = 2

z = x + y

print(z)
```

```text
$ python calculator.py
3
```

Kullanıcıdan alalım:

```python
x = input("What's x? ")
y = input("What's y? ")

z = x + y

print(z)
```

```text
$ python calculator.py
What's x? 1
What's y? 2
12
```

1 artı 2, 12 çıktı. Sebebi şu: klavyeden gelen her şey **metindir**.
`input` her zaman `str` döndürür ve iki dizeyi `+` yan yana ekler: `"1" +
"2"` = `"12"`. Metni sayıya çevirmek gerekiyor; `int(x)` bunu yapar. Bir
değeri bir türden başka türe çevirmeye **tür dönüşümü** (casting) denir.

```python
x = input("What's x? ")
y = input("What's y? ")

z = int(x) + int(y)

print(z)
```

```text
$ python calculator.py
What's x? 1
What's y? 2
3
```

Daha kısası: fonksiyonların içine fonksiyon koyabilirsin.

```python
x = int(input("What's x? "))
y = int(input("What's y? "))

print(x + y)
```

<figure class="fig"><div class="flow"><span class="node">input("What's x? ")</span><span class="arrow">→</span><span class="node">"1"</span><span class="arrow">→</span><span class="node">int("1")</span><span class="arrow">→</span><span class="node ok">1</span></div><figcaption>İç içe çağrıda <b>içteki</b> önce çalışır: önce <code>input</code> metni döndürür, sonra <code>int</code> onu sayıya çevirir.</figcaption></figure>

## Okunabilirlik kazanır

Aynı işi yapmanın birçok makul yolu vardır; hangisini seçersen seç kod
**okunur** olmalı. Yorumlarla neyi neden yaptığını söyle, tek satıra çok şey
sıkıştırma. Altı ay sonra kodu okuyacak kişi büyük ihtimalle sensin.

## Ondalıklı sayılar (float)

**Kayan noktalı sayı** (floating point, kısaca float), `0.52` gibi virgülden
sonrası olan sayıdır. Python'da ondalık ayırıcı nokta (`.`):

```python
x = float(input("What's x? "))
y = float(input("What's y? "))

print(x + y)
```

```text
$ python calculator.py
What's x? 1.2
What's y? 3.4
4.6
```

Toplamı en yakın tam sayıya yuvarlamak istersen `round` var. Belgesinde
`round(number[, ndigits])` yazıyor; köşeli parantez "isteğe bağlı" demek:

```python
x = float(input("What's x? "))
y = float(input("What's y? "))

# Toplamı en yakın tam sayıya yuvarla
z = round(x + y)

print(z)
```

```text
$ python calculator.py
What's x? 1.2
What's y? 3.4
5
```

Büyük sayıları okunur yazmak için f-string içinde `:,` biçimi binlik ayırıcı
olarak virgül koyar:

```python
x = float(input("What's x? "))
y = float(input("What's y? "))

z = round(x + y)

print(f"{z:,}")
```

```text
$ python calculator.py
What's x? 999
What's y? 1
1,000
```

## Ondalıklılarla daha fazlası

Bölme sonsuz devam edebilir:

```python
x = float(input("What's x? "))
y = float(input("What's y? "))

z = x / y

print(z)
```

```text
$ python calculator.py
What's x? 2
What's y? 3
0.6666666666666666
```

İki basamağa yuvarlamanın iki yolu var. `round`'a ikinci argüman:

```python
x = float(input("What's x? "))
y = float(input("What's y? "))

z = round(x / y, 2)

print(z)
```

```text
$ python calculator.py
What's x? 2
What's y? 3
0.67
```

Ya da f-string'de `:.2f` ("virgülden sonra iki basamaklı float"):

```python
x = float(input("What's x? "))
y = float(input("What's y? "))

z = x / y

print(f"{z:.2f}")
```

```text
$ python calculator.py
What's x? 2
What's y? 3
0.67
```

İkisinin farkı: `round` bir **sayı** döndürür, `:.2f` bir **metin** üretir
(`round(2.5, 2)` `2.5` verir, `f"{2.5:.2f}"` ise `2.50` yazar).

## def: kendi fonksiyonların

Kendi fonksiyonunu yazabilseydin güzel olmazdı mı? Önce olmayan bir
fonksiyonu çağıralım:

```python
name = input("What's your name? ")
hello()
print(name)
```

```text
$ python hello.py
What's your name? David
Traceback (most recent call last):
  File "hello.py", line 2, in <module>
    hello()
    ^^^^^
NameError: name 'hello' is not defined. Did you mean: 'help'?
```

`NameError`: Python `hello` diye bir ad bilmiyor (ve yakın gördüğü `help`'i
öneriyor). Fonksiyonu **tanımlamak** (define) için `def` yazılır:

```python
def hello():
    print("hello")


name = input("What's your name? ")
hello()
print(name)
```

```text
$ python hello.py
What's your name? David
hello
David
```

`def hello():` satırının altındaki her şey **girintili** (indented). Python
girintiyle hangi satırların fonksiyonun **gövdesi** (body) olduğunu anlar;
girintisiz satır artık fonksiyonun dışındadır. Çıktı henüz istediğimiz gibi
değil. Fonksiyona bir **parametre** verelim, kime selam vereceğini alsın:

```python
# Kendi fonksiyonumuz: kime selam verileceğini parametre olarak alıyor
def hello(to):
    print("hello,", to)


name = input("What's your name? ")
hello(name)
```

```text
$ python hello.py
What's your name? David
hello, David
```

`hello(name)` çağrılınca `name`'in değeri fonksiyonun içine `to` adıyla
gider. Parametreye **varsayılan değer** (default value) de verebilirsin;
argüman verilmezse o kullanılır:

```python
def hello(to="world"):
    print("hello,", to)


name = input("What's your name? ")
hello(name)

# Argüman vermeden: varsayılan değer kullanılır
hello()
```

```text
$ python hello.py
What's your name? David
hello, David
hello, world
```

Fonksiyonları dosyanın başına yazmak zorunda değilsin. Programcılar genellikle
programın ana akışını `main` adlı bir fonksiyona koyar ve diğer fonksiyonları
altına yazar:

```python
def main():
    name = input("What's your name? ")
    hello(name)


def hello(to="world"):
    print("hello,", to)
```

```text
$ python hello.py
```

Hiçbir şey olmadı. Hata değil: `def` yalnızca **tanımlar**, çalıştırmaz.
`main`'i kimse çağırmadığı için soru bile sorulmadı. Dosyanın sonuna tek satır
yeter:

```python
def main():
    name = input("What's your name? ")
    hello(name)
    hello()


def hello(to="world"):
    print("hello,", to)


main()
```

```text
$ python hello.py
What's your name? David
hello, David
hello, world
```

Bu düzende `main` çalışana kadar `hello` zaten tanımlanmış oluyor, yani
fonksiyonların dosyadaki sırası sorun olmuyor.

## Dönüş değerleri

Bazen fonksiyonun bir şey yazmasını değil, bir değer hesaplayıp **geri
vermesini** istersin; buna **dönüş değeri** (return value) denir. `return`
değeri fonksiyonu çağıran yere gönderir:

```python
def main():
    x = int(input("What's x? "))
    print("x squared is", square(x))


def square(n):
    return n * n


main()
```

```text
$ python calculator.py
What's x? 3
x squared is 9
```

`square(x)` çağrısı `x`'i `n` olarak alır, `n * n`'i döndürür; `print` o
değeri yazar. `print` ile `return` farkı önemli: `print` ekrana yazar ve
değer kaybolur, `return` değeri programın kullanabileceği şekilde geri verir.

## Özet

Bu hafta öğrendiklerin, yazacağın her programda tekrar tekrar karşına
çıkacak:

- Python'da ilk programını yazmak ve terminalde çalıştırmak
- Fonksiyonlar, argümanlar ve parametreler (`print`, `input`, `end`, `sep`)
- Hatalar ve hata mesajını okumak
- Değişkenler ve atama (`=`)
- Yorumlar ve sözde kod
- Dizeler, f-string ve dize metotları (`strip`, `title`, `lower`, `replace`)
- Tam sayılar, ondalıklı sayılar ve tür dönüşümü (`int`, `float`, `round`)
- Okunabilirlik
- Kendi fonksiyonların (`def`, `main`) ve dönüş değerleri (`return`)

## Bu haftanın problem seti

Bölümde iki tür alıştırma var. **Alıştırma** sekmesindeki yedisi bu dersin
konularını tek tek çalıştırıyor. **Problem Seti** sekmesindeki beşi CS50'nin
bu haftaki ödevi (Problem Set 0); her biri dersteki bir konuyu kullanıyor:

| Problem | Ne istiyor | Dersteki konu |
|---|---|---|
| Kapalı Alan Sesi | girdiyi küçük harfle yazmak | `lower` |
| Oynatma Hızı | boşlukların yerine `...` | `replace` |
| Yüz İfadeleri | `:)` ve `:(` yerine yazı, `main` ve `convert` | kendi fonksiyonların, `return` |
| Einstein | E = mc² | `int`, `**` |
| Bahşiş Hesaplayıcı | iki eksik fonksiyonu tamamlamak | `removeprefix`, `float`, `return` |

CS50'den farkı:

- CS50'de her problem kendi dosyasında (`indoor.py`, `tip.py`...) yazılıp
  `check50` ile denetleniyor. Burada **Çalıştır**'a basınca Odyssey programını
  CS50'nin "How to Test" bölümündeki girdilerle tek tek çalıştırıp çıktını
  karşılaştırıyor.
- Soru metnini (`input("...")` içindeki yazı) istediğin gibi yazabilirsin;
  yalnızca programın yazdıkları denetleniyor.
- Yüz İfadeleri'nde emoji yerine `[happy]` / `[sad]` var (yazılan her şey
  klavyedeki karakterlerle olsun diye).

---

*Bu bölüm, Harvard Üniversitesi'nin [CS50's Introduction to Programming with Python](https://cs50.harvard.edu/python/) dersinin 0. haftasından (ders notu ve problem seti) çevrilip uyarlanmıştır; örnekler ve alıştırmalar değiştirildi, problem seti CS50'nin check50'siyle değil Odyssey'nin denetimiyle sınanıyor. Özgün içerik ve bu uyarlama [CC BY-NC-SA 4.0](https://creativecommons.org/licenses/by-nc-sa/4.0/) lisanslıdır. Harvard bu uyarlamayı onaylamış değildir.*
