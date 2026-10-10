Gerçek bir projede testler kodun yanında ayrı bir **`tests`** klasöründe
durur ve tek komutla hepsi çalışır. Aşağıdaki kod küçük bir proje kurup
testleri **keşfederek** (discover) çalıştırıyor:

```python
import io
import unittest
from pathlib import Path

Path("shop").mkdir()
Path("shop/__init__.py").write_text("")
Path("shop/prices.py").write_text(
    "def with_tax(price, rate=0.2):\n"
    "    return round(price * (1 + rate), 2)\n")
Path("tests").mkdir()
Path("tests/__init__.py").write_text("")
Path("tests/test_prices.py").write_text(
    "import unittest\n"
    "from shop.prices import with_tax\n\n\n"
    "class TestWithTax(unittest.TestCase):\n"
    "    def test_default(self):\n"
    "        self.assertEqual(with_tax(10), 12.0)\n\n"
    "    def test_zero_rate(self):\n"
    "        self.assertEqual(with_tax(10, 0), 10)\n")
suite = unittest.defaultTestLoader.discover("tests", top_level_dir=".")
result = unittest.TextTestRunner(stream=io.StringIO()).run(suite)
print(result.testsRun, result.wasSuccessful())
```

```text
2 True
```

## Klasör düzeni

```text
proje/
  shop/
    __init__.py
    prices.py
  tests/
    __init__.py
    test_prices.py
```

- Test dosyalarının adı **`test_`** ile başlar; keşif bu adlara bakar.
- Komut satırında proje klasöründen: `python -m unittest` (ya da
  `python -m unittest discover -s tests`). `pytest` aynı klasörü
  kendiliğinden bulur.
- Testler kodu **içe aktararak** sınar (`from shop.prices import with_tax`);
  kodu kopyalamaz.

## İyi bir test

- **Hazırla – çalıştır – denetle** (arrange – act – assert): girdiyi kur,
  fonksiyonu bir kez çağır, sonucu denetle. Bir test bir davranışı sınar.
- **Adı ne sınadığını söyler:** `test_zero_rate`, `test_empty_list`; düşünce
  rapordan ne bozulduğu anlaşılır.
- **Kenar durumları:** boş girdi, tek eleman, sıfır, eksi, çok büyük değer,
  hatalı tür, beklenen hata (`assertRaises`).
- **Bağımsız ve tekrarlanabilir:** sıra önemli değil; ağ, saat, rastgelelik
  sahte nesneyle ya da sabit tohumla sabitlenir.
- **Hızlı:** testler sık çalıştırılsın diye saniyeler içinde biter.
- Bir hata bulunduğunda önce o hatayı yakalayan testi yaz, sonra düzelt: aynı
  hata bir daha geri gelmez.
