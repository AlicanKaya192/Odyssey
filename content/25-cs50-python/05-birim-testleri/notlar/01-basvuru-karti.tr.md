Hafta 5'te geçen her şey tek sayfada.

## Adlar

| Ne | Kural | Örnek |
|---|---|---|
| Test dosyası | `test_` + test edilen dosya | `test_calculator.py` |
| Test fonksiyonu | `test_` ile başlar | `def test_zero():` |
| Test klasörü | içinde boş `__init__.py` | `test/__init__.py` |

`pytest` adı `test_` ile başlamayan fonksiyonu test saymaz.

## Komutlar

| Komut | Ne yapar |
|---|---|
| `pip install pytest` | pytest'i kurar (kendi bilgisayarında) |
| `pytest test_calculator.py` | o dosyadaki testleri çalıştırır |
| `pytest test` | `test` klasöründeki bütün testleri çalıştırır |
| `python test_calculator.py` | dosyayı sıradan program gibi çalıştırır |

## Çıktıyı okumak

| İşaret | Anlamı |
|---|---|
| `.` | bir test geçti |
| `F` | bir test düştü (failed) |
| `>` | testin düştüğü satır |
| `E` | neden: `assert 6 == 9` |
| `where 6 = square(3)` | değer nereden geldi |
| `2 failed, 1 passed` | özet |

## Test yazmak

| Yazım | Ne iddia eder |
|---|---|
| `assert square(3) == 9` | sonuç 9 |
| `assert hello() == "hello, world"` | varsayılan argümanla sonuç |
| `with pytest.raises(TypeError):` | içindeki satır `TypeError` vermeli |

```python
import pytest

from calculator import square


def test_zero():
    assert square(0) == 0


def test_str():
    with pytest.raises(TypeError):
        square("cat")
```

## Test edilebilir program

```python
def main():
    x = int(input("What's x? "))
    print("x squared is", square(x))


def square(n):
    return n * n


if __name__ == "__main__":
    main()
```

- Fonksiyon sonucunu **döndürür** (`return`); yazma işi `main`'de.
- `if __name__ == "__main__":` içe aktarılınca `main`'in çalışmasını önler.

## Hangi durumlar

Her fonksiyon için şunları düşün: sıradan bir değer, sınırdaki değer
(0, boş metin, en küçük ve en büyük), negatif sayı, büyük ve küçük harf,
geçersiz girdi (hata vermeli mi?). Soru hep aynı: **bu fonksiyon nasıl
yanlış yazılmış olabilirdi, hangi örnek bunu yakalar?**
