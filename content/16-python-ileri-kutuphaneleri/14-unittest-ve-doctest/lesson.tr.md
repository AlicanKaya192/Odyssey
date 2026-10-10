# unittest ve doctest

Bir fonksiyonu yazdın, birkaç değerle denedin, çalışıyor. Bir ay sonra küçük
bir değişiklik yaptın; eski durumların hâlâ çalıştığını nasıl bileceksin?
Elle yeniden denemek unutulur. **Test**, "bu girdiyle şu sonuç çıkmalı"
beklentisini koda döker ve her seferinde saniyeler içinde yeniden çalışır.
Bu bölüm standart kütüphanedeki iki aracı anlatıyor: **`unittest`** (test
sınıfları, sahte nesneler) ve **`doctest`** (belge içindeki örnekler). API
Yazmak modülünde anlatılan `pytest` de bu testleri çalıştırabilir.

## İlk test sınıfı

```python
import io
import unittest


def word_count(text):
    return len(text.split())


class TestWordCount(unittest.TestCase):
    def test_simple(self):
        self.assertEqual(word_count("a b c"), 3)

    def test_empty(self):
        self.assertEqual(word_count(""), 0)

    def test_spaces(self):
        self.assertEqual(word_count("  a   b "), 2)


suite = unittest.defaultTestLoader.loadTestsFromTestCase(TestWordCount)
stream = io.StringIO()
result = unittest.TextTestRunner(stream=stream, verbosity=2).run(suite)
for line in stream.getvalue().splitlines():
    if line.endswith("ok"):
        print(line)
print(result.testsRun, result.wasSuccessful())
```

```text
test_empty (__main__.TestWordCount.test_empty) ... ok
test_simple (__main__.TestWordCount.test_simple) ... ok
test_spaces (__main__.TestWordCount.test_spaces) ... ok
3 True
```

- Testler **`unittest.TestCase`**'ten türeyen bir sınıfta toplanır. Adı
  **`test_`** ile başlayan her metot ayrı bir testtir.
- **`self.assertEqual(gelen, beklenen)`** ikisi eşit değilse testi düşürür.
- Gerçek bir test dosyasının sonuna `unittest.main()` yazılır ya da
  komut satırında `python -m unittest` çalıştırılır. Burada çıktıyı sayfaya
  koyabilmek için çalıştırıcıyı (runner) elle kurduk ve süre satırını
  atladık.
- Her test birbirinden bağımsız çalışır; birinin düşmesi diğerlerini
  durdurmaz.

## Düşen test ne söyler?

```python
import io
import unittest


def average(values):
    return sum(values) // len(values)


class TestAverage(unittest.TestCase):
    def test_whole(self):
        self.assertEqual(average([2, 4]), 3)

    def test_fraction(self):
        self.assertEqual(average([1, 2]), 1.5)


suite = unittest.defaultTestLoader.loadTestsFromTestCase(TestAverage)
result = unittest.TextTestRunner(stream=io.StringIO()).run(suite)
print(result.testsRun, len(result.failures))
name, report = result.failures[0]
print(name.id().split(".")[-1])
print(report.strip().splitlines()[-1])
```

```text
2 1
test_fraction
AssertionError: 1 != 1.5
```

- `average` yanlışlıkla `//` (tam bölme) kullanıyor. `[2, 4]` için sonuç
  yine doğru (3), hata yalnızca küsuratlı ortalamada çıkıyor. **Tek bir
  "mutlu yol" testi bu hatayı kaçırırdı**; testler kenar durumları da
  kapsamalı.
- Düşen testin raporu hangi testin düştüğünü ve neyin beklendiğini söylüyor:
  `1 != 1.5` (gelen ≠ beklenen).

## Daha fazla assert, setUp ve subTest

```python
import io
import unittest


class Account:
    def __init__(self, balance=0):
        self.balance = balance

    def withdraw(self, amount):
        if amount > self.balance:
            raise ValueError("not enough money")
        self.balance -= amount


class TestAccount(unittest.TestCase):
    def setUp(self):
        self.account = Account(100)

    def test_withdraw(self):
        self.account.withdraw(30)
        self.assertEqual(self.account.balance, 70)

    def test_too_much(self):
        with self.assertRaises(ValueError):
            self.account.withdraw(500)
        self.assertEqual(self.account.balance, 100)

    def test_many(self):
        for amount in [0, 1, 100]:
            with self.subTest(amount=amount):
                Account(100).withdraw(amount)

    def test_float(self):
        self.assertAlmostEqual(0.1 + 0.2, 0.3)


suite = unittest.defaultTestLoader.loadTestsFromTestCase(TestAccount)
result = unittest.TextTestRunner(stream=io.StringIO()).run(suite)
print(result.testsRun, result.wasSuccessful())
```

```text
4 True
```

- **`setUp`** her testten **önce** çalışır: her test temiz bir hesapla
  başlar. (`tearDown` her testten sonra; dosya silmek, bağlantı kapatmak
  için.)
- **`with self.assertRaises(ValueError):`** blokta bu hatanın çıkmasını
  bekler; çıkmazsa test düşer. Hatadan sonra bakiyenin değişmediğini de
  denetledik.
- **`subTest`** bir döngüdeki her değeri ayrı bir alt test yapar; biri düşerse
  hangi değerde düştüğü raporda yazar.
- **`assertAlmostEqual`** float'ları küçük farkı tolere ederek karşılaştırır
  (decimal bölümü).
- Sık kullanılanlar: `assertTrue`, `assertFalse`, `assertIn`, `assertIsNone`,
  `assertIsInstance`, `assertGreater`.

## Sahte nesne: unittest.mock

```python
import io
import unittest
from unittest.mock import patch


def fetch_price(symbol):
    raise ConnectionError("no network in tests")


def portfolio_value(holdings):
    return sum(qty * fetch_price(symbol) for symbol, qty in holdings.items())


class TestPortfolio(unittest.TestCase):
    @patch("__main__.fetch_price", return_value=10)
    def test_value(self, fake):
        self.assertEqual(portfolio_value({"AAA": 3, "BBB": 2}), 50)
        self.assertEqual(fake.call_count, 2)
        fake.assert_any_call("AAA")


suite = unittest.defaultTestLoader.loadTestsFromTestCase(TestPortfolio)
result = unittest.TextTestRunner(stream=io.StringIO()).run(suite)
print(result.testsRun, result.wasSuccessful())
```

```text
1 True
```

- Gerçek `fetch_price` ağa çıkıyor (burada çıkamayınca hata veriyor). Test
  ağa, saate, rastgeleliğe bağlı olmamalı: her çalıştırmada aynı sonucu
  vermeli.
- **`@patch("modül.ad", return_value=10)`** test süresince o adı sahte bir
  nesneyle (Mock) değiştirir; test bitince eskisi geri gelir. Burada modül
  `__main__`; gerçek projede `"shop.prices.fetch_price"` gibi, **kullanıldığı
  yerin** adı yazılır.
- Sahte nesne kaç kez ve neyle çağrıldığını hatırlar: `call_count`,
  `assert_any_call`, `assert_called_once_with`.

## doctest: belgedeki örnekler

```python
import contextlib
import doctest
import io


def slugify(title):
    """Bir başlığı adres parçasına çevirir.

    >>> slugify("Hello World")
    'hello-world'
    >>> slugify("  Many   spaces  ")
    'many-spaces'
    >>> slugify("")
    ''
    """
    return "-".join(title.lower().split())


def broken_double(x):
    """
    >>> broken_double(2)
    4
    """
    return x + 2 + 1


print(doctest.run_docstring_examples(slugify, globals()))
with contextlib.redirect_stdout(io.StringIO()) as report:
    results = doctest.testmod()
print(results)
lines = report.getvalue().splitlines()
start = lines.index("Expected:")
print(lines[start:start + 4])
```

```text
None
TestResults(failed=1, attempted=4)
['Expected:', '    4', 'Got:', '    5']
```

- Docstring içindeki **`>>>`** satırları birer örnek; altlarındaki satır
  beklenen çıktı. **`doctest`** bu örnekleri çalıştırıp karşılaştırır.
- `slugify`'ın üç örneği tuttuğu için `run_docstring_examples` hiçbir şey
  yazmadı (`None`).
- `testmod()` dosyadaki bütün docstring'leri dener: 4 örnek, 1 düşen.
  Düşen örneğin raporunu normalde ekrana yazar; burada
  `redirect_stdout` ile yakalayıp yalnızca beklenen / gelen kısmını
  gösterdik: `broken_double(2)` `4` yerine `5` verdi.
- Doctest belgeyi **doğru tutar**: örnek eskirse test düşer. Kenar durumları
  çok olan mantık için tek başına yetmez; `unittest`/`pytest` ile birlikte
  kullanılır.

## unittest mi, pytest mi?

| | `unittest` | `pytest` |
|---|---|---|
| Kurulum | standart kütüphane | paket (`pip install pytest`) |
| Yazım | sınıf + `self.assertEqual` | düz fonksiyon + `assert` |
| Çalıştırma | `python -m unittest` | `pytest` (unittest testlerini de çalıştırır) |
| Sahte nesne | `unittest.mock` | `unittest.mock` ya da `monkeypatch` |

İkisi aynı fikri taşır. Ekip hangisini kullanıyorsa o; yeni projelerde
`pytest` yaygın, ama `unittest` her Python kurulumunda hazır.

## Özet

- `unittest.TestCase` + `test_` ile başlayan metotlar; `assertEqual`,
  `assertRaises`, `assertAlmostEqual`.
- `setUp` her testten önce; `subTest` döngüdeki değerler için.
- Testler kenar durumları kapsar: boş, tek eleman, küsuratlı, hatalı girdi.
- `unittest.mock.patch` ağ, saat gibi dış şeyleri test süresince değiştirir.
- `doctest` docstring'deki `>>>` örneklerini çalıştırır.
