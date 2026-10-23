# Birim Testleri

CS50 Python'un altıncı haftası. Videoyu **Video** sekmesinden izleyebilirsin;
bu sayfa dersin yazılı hâli. Şimdiye kadar kodunu muhtemelen `print`
satırlarıyla ya da Odyssey'nin denetimiyle sınadın. Yazılımcılar ise çoğu
zaman **kendi programlarını sınayan kod** yazar: buna **test** denir.
Programın küçük bir parçasını, çoğunlukla tek bir fonksiyonu sınayan teste
**birim testi** (unit test) denir.

## Test edilecek program

Bir sayının karesini alan küçük bir program, `calculator.py`:

```python
def main():
    x = int(input("What's x? "))
    print("x squared is", square(x))


def square(n):
    return n * n


if __name__ == "__main__":
    main()
```

```text
$ python calculator.py
What's x? 2
x squared is 4
```

`square(2)` 4 verdi, doğru görünüyor. Peki 3 için, eksi sayılar için, 0 için?
Her seferinde programı çalıştırıp elle bir sayı yazmak yerine `square`'i
kendisi deneyen bir program yazacağız.

## Modülü içe aktarınca main çalışmasın

`calculator.py`'nin son iki satırı yeni:

```python
if __name__ == "__main__":
    main()
```

Python her dosyaya `__name__` adında gizli bir değişken verir. Dosyayı
doğrudan çalıştırırsan (`python calculator.py`) değeri `"__main__"` olur.
Dosya başka bir programdan **içe aktarılırsa** (`from calculator import
square`) değeri modülün adıdır, `"calculator"`. Bu `if` sayesinde `main`
yalnızca dosya doğrudan çalıştırıldığında çağrılır; testimiz `square`'i içe
aktarınca program kullanıcıya `What's x?` diye sormaya kalkmaz. Bu satırı
unutunca ne olduğu **Sık Yapılan Hatalar** notunda.

## İlk test programı

Test dosyasının adı geleneksel olarak `test_` ile başlar ve test ettiği
dosyanın adıyla devam eder: `test_calculator.py`. İçinde `square`'i birkaç
sayıyla çağırıp sonucu beklenenle karşılaştıran bir fonksiyon:

```python
from calculator import square


def main():
    test_square()


def test_square():
    if square(2) != 4:
        print("2 squared was not 4")
    if square(3) != 9:
        print("3 squared was not 9")


if __name__ == "__main__":
    main()
```

```text
$ python test_calculator.py
```

Hiçbir şey yazmadı: iki karşılaştırma da tuttu. Testin işe yaradığını görmek
için `calculator.py`'ye bilerek bir hata koyalım, `*` yerine `+`:

```python
def main():
    x = int(input("What's x? "))
    print("x squared is", square(x))


def square(n):
    return n + n


if __name__ == "__main__":
    main()
```

```text
$ python test_calculator.py
3 squared was not 9
```

`2 + 2` de 4 ettiği için birinci karşılaştırma hatayı **göremedi**; ikincisi
gördü. İlk ders: tek bir örnek yetmez.

## assert

Python'un `assert` (iddia et) komutu bir koşulun doğru olduğunu iddia eder.
Koşul yanlışsa program `AssertionError` hatasıyla durur. `if` ve `print`
yerine:

```python
from calculator import square


def main():
    test_square()


def test_square():
    assert square(2) == 4
    assert square(3) == 9


if __name__ == "__main__":
    main()
```

Hatalı `calculator.py` ile:

```text
$ python test_calculator.py
Traceback (most recent call last):
  File "test_calculator.py", line 14, in <module>
    main()
    ~~~~^^
  File "test_calculator.py", line 5, in main
    test_square()
    ~~~~~~~~~~~^^
  File "test_calculator.py", line 10, in test_square
    assert square(3) == 9
           ^^^^^^^^^^^^^^
AssertionError
```

Hata mesajı hangi satırın tutmadığını gösteriyor: `assert square(3) == 9`.
Ama program ilk tutmayan `assert`'te durdu; daha fazla durum eklesek
sonrakileri hiç denemezdi. Her birini `try` ve `except` ile sarmak bir çözüm:

```python
from calculator import square


def main():
    test_square()


def test_square():
    try:
        assert square(2) == 4
    except AssertionError:
        print("2 squared was not 4")
    try:
        assert square(3) == 9
    except AssertionError:
        print("3 squared was not 9")
    try:
        assert square(-2) == 4
    except AssertionError:
        print("-2 squared was not 4")
    try:
        assert square(-3) == 9
    except AssertionError:
        print("-3 squared was not 9")
    try:
        assert square(0) == 0
    except AssertionError:
        print("0 squared was not 0")


if __name__ == "__main__":
    main()
```

```text
$ python test_calculator.py
3 squared was not 9
-2 squared was not 4
-3 squared was not 9
```

Artık bütün durumlar deneniyor, ama beş satırlık iş yirmi satır oldu ve her
yeni durum dört satır daha istiyor. Bu tekrarı bizim yerimize yapan bir
kütüphane var.

## pytest

`pytest`, fonksiyonları sınamak için yazılmış üçüncü taraf bir kütüphane.
Kendi bilgisayarında `pip install pytest` ile kurulur; Odyssey'de kurulu ve
alıştırmalarda testlerini Odyssey kendisi çalıştırıyor. `pytest` ile test
dosyası kısalır: `main` de, `try` de gerekmez, adı `test_` ile başlayan her
fonksiyonu `pytest` kendisi bulup çalıştırır:

```python
from calculator import square


def test_square():
    assert square(2) == 4
    assert square(3) == 9
    assert square(-2) == 4
    assert square(-3) == 9
    assert square(0) == 0
```

Programı `python` ile değil `pytest` ile çalıştırırsın. Hatalı
`calculator.py` ile (çıktının başındaki sürüm satırlarını ve sondaki süreyi
kısalttık, bilgisayara göre değişiyorlar):

```text
$ pytest test_calculator.py
=================== test session starts ===================
collected 1 item

test_calculator.py F                                 [100%]

======================== FAILURES =========================
_______________________ test_square _______________________

    def test_square():
        assert square(2) == 4
>       assert square(3) == 9
E       assert 6 == 9
E        +  where 6 = square(3)

test_calculator.py:6: AssertionError
================= short test summary info =================
FAILED test_calculator.py::test_square - assert 6 == 9
========================= 1 failed ========================
```

Okuması kolay: `F` bir testin düştüğünü (failed) gösterir, `>` düşen satırı,
`E` de nedenini: `assert 6 == 9`, `6` de `square(3)`'ten gelmiş. Yani
`square(3)` 9 yerine 6 döndürüyor. `+`'yı `*` yapınca:

```text
$ pytest test_calculator.py
=================== test session starts ===================
collected 1 item

test_calculator.py .                                 [100%]

========================= 1 passed ========================
```

Nokta (`.`) geçen bir test demek.

`pytest` bir test fonksiyonunda **ilk** tutmayan `assert`'te o fonksiyonu
bırakır. Hatanın tamamını görmek için testleri ayrı fonksiyonlara bölmek
iyi bir alışkanlık: pozitif sayılar, negatif sayılar, sıfır.

```python
from calculator import square


def test_positive():
    assert square(2) == 4
    assert square(3) == 9


def test_negative():
    assert square(-2) == 4
    assert square(-3) == 9


def test_zero():
    assert square(0) == 0
```

`calculator.py` yeniden hatalıyken:

```text
$ pytest test_calculator.py
=================== test session starts ===================
collected 3 items

test_calculator.py FF.                               [100%]

======================== FAILURES =========================
______________________ test_positive ______________________

    def test_positive():
        assert square(2) == 4
>       assert square(3) == 9
E       assert 6 == 9
E        +  where 6 = square(3)

test_calculator.py:6: AssertionError
______________________ test_negative ______________________

    def test_negative():
>       assert square(-2) == 4
E       assert -4 == 4
E        +  where -4 = square(-2)

test_calculator.py:10: AssertionError
================= short test summary info =================
FAILED test_calculator.py::test_positive - assert 6 == 9
FAILED test_calculator.py::test_negative - assert -4 == 4
==================== 2 failed, 1 passed ===================
```

Üç test ayrı ayrı çalıştı: `FF.` ikisinin düştüğünü, birinin geçtiğini
söylüyor. Negatif testteki ayrıntı ilginç: `-2 + -2` -4 eder, kare ise 4.
Sıfır testi geçti, çünkü `0 + 0` de `0 * 0` de 0. Bir hatayı yakalamak
için doğru durumu seçmek gerekiyor.

Bir fonksiyonun **hata vermesini** de test edebilirsin. `square("cat")`
`TypeError` vermeli; `pytest.raises` bunu iddia eder (bunun için dosyanın
başında `import pytest`):

```python
import pytest

from calculator import square


def test_positive():
    assert square(2) == 4
    assert square(3) == 9


def test_negative():
    assert square(-2) == 4
    assert square(-3) == 9


def test_zero():
    assert square(0) == 0


def test_str():
    with pytest.raises(TypeError):
        square("cat")
```

```text
$ pytest test_calculator.py
=================== test session starts ===================
collected 4 items

test_calculator.py ....                              [100%]

========================= 4 passed ========================
```

Hangi durumları test edeceğine sen karar verirsin. Yol gösteren soru şu:
**bu fonksiyon nasıl yanlış yazılmış olabilirdi, ve hangi örnek bunu
yakalardı?**

## Metinleri test etmek

İlk haftadaki `hello.py`'yi hatırla:

```python
def main():
    name = input("What's your name? ")
    hello(name)


def hello(to="world"):
    print("hello,", to)


if __name__ == "__main__":
    main()
```

```text
$ python hello.py
What's your name? David
hello, David
```

Bunun için bir test:

```python
from hello import hello


def test_hello():
    assert hello("David") == "hello, David"
    assert hello() == "hello, world"
```

```text
$ pytest test_hello.py
=================== test session starts ===================
collected 1 item

test_hello.py F                                      [100%]

======================== FAILURES =========================
_______________________ test_hello ________________________

    def test_hello():
>       assert hello("David") == "hello, David"
E       AssertionError: assert None == 'hello, David'
E        +  where None = hello('David')

test_hello.py:5: AssertionError
------------------ Captured stdout call -------------------
hello, David
================= short test summary info =================
FAILED test_hello.py::test_hello - AssertionError: assert...
========================= 1 failed ========================
```

Program doğru selam verdiği hâlde test düştü: `hello` selamı **yazıyor** ama
**döndürmüyor**, bu yüzden `hello("David")`'in değeri `None`. Ekrana yazmak
bir **yan etki** (side effect): fonksiyon bir şey yapıyor ama sonucunu
çağırana vermiyor (yazdığı satır çıktıda `Captured stdout` altında duruyor).
Test edilebilir fonksiyon sonucunu `return` ile döndürür, yazma işini
`main`'e bırakır:

```python
def main():
    name = input("What's your name? ")
    print(hello(name))


def hello(to="world"):
    return f"hello, {to}"


if __name__ == "__main__":
    main()
```

```text
$ python hello.py
What's your name? David
hello, David
```

```text
$ pytest test_hello.py
=================== test session starts ===================
collected 1 item

test_hello.py .                                      [100%]

========================= 1 passed ========================
```

Bu testi de ikiye bölmek daha iyi: varsayılan değer ve argüman ayrı.

```python
from hello import hello


def test_default():
    assert hello() == "hello, world"


def test_argument():
    assert hello("David") == "hello, David"
```

## Testleri klasörde toplamak

Programın büyüdükçe test dosyaları çoğalır. `pytest` bir klasördeki bütün
testleri tek komutla çalıştırabilir. Testleri `test` adında bir klasöre koy
(`test/test_hello.py`) ve klasöre boş bir `__init__.py` dosyası ekle;
`pytest` klasörü bir paket olarak tanısın diye bu dosya gerekiyor. Sonra
klasörün adını ver:

```text
$ pytest test
=================== test session starts ===================
collected 2 items

test\test_hello.py ..                                [100%]

========================= 2 passed ========================
```

## Odyssey testlerini nasıl sınıyor

Bu haftanın alıştırmalarında **test dosyasını sen yazıyorsun**, test edilen
modül (`calculator.py` gibi) hazır. Odyssey önce testlerini doğru modülle
çalıştırır: hepsi geçmeli. Sonra modülün **bilerek bozulmuş** birkaç
sürümüyle yeniden çalıştırır: her bozuk sürümde testlerinden **en az biri
düşmeli**. Yukarıdaki `+` hatası tam böyle bir bozuk sürüm; yalnızca
`square(2)`'yi deneyen bir test onu kaçırır. CS50'nin check50'si de ödevleri
aynı yolla sınıyor.

## Özet

Test, programcılığın olağan bir parçası. Birim testleri kodunun belirli
parçalarının beklendiği gibi çalıştığını gösterir; elle yazdığın test
programlarıyla ya da `pytest` gibi bir kütüphaneyle:

- Birim testleri ve `test_` ile başlayan dosya ve fonksiyon adları
- `if __name__ == "__main__":`
- `assert` ve `AssertionError`
- `pytest`: `F` ve `.`, testleri bölmek, `pytest.raises`
- Yan etki: `print` yerine `return`
- Testleri klasörde toplamak (`__init__.py`)

## Bu haftanın problem seti

**Alıştırma** sekmesindeki yedi alıştırma bu dersin konularını tek tek
çalıştırıyor. **Problem Seti** sekmesindeki dördü CS50'nin bu haftaki ödevi
(Problem Set 5): önceki haftalardan dört programı fonksiyonlara bölüp
testlerini yazmak.

| Problem | Ne istiyor | İlk hâli |
|---|---|---|
| twttr'ımı Test Etmek | `shorten` ve testleri | Hafta 2 |
| Bankaya Dönüş | `value` ve testleri | Hafta 1 |
| Kişisel Plakayı Yeniden İstemek | `is_valid` ve testleri | Hafta 2 |
| Yeniden Yakıt Almak | `convert`, `gauge` ve testleri | Hafta 3 |

Her problemde iki dosya var: programın kendisi ve `test_` dosyası. İkisi de
seninki; Odyssey programını ve testlerini ayrı ayrı denetliyor.

---

*Bu bölüm, Harvard Üniversitesi'nin [CS50's Introduction to Programming with Python](https://cs50.harvard.edu/python/) dersinin 5. haftasından (ders notu ve problem seti) çevrilip uyarlanmıştır; örnekler ve alıştırmalar değiştirildi, problem seti CS50'nin check50'siyle değil Odyssey'nin denetimiyle sınanıyor. Özgün içerik ve bu uyarlama [CC BY-NC-SA 4.0](https://creativecommons.org/licenses/by-nc-sa/4.0/) lisanslıdır. Harvard bu uyarlamayı onaylamış değildir.*
