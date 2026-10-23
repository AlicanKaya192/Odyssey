Test yazarken en sık yapılan hatalar ve mesajları (Python 3.14 ve pytest ile
ölçüldü). Çıktının başındaki sürüm satırlarını ve sondaki süreyi kısalttık.

## Modülün sonunda koşulsuz main()

`calculator.py`'nin sonunda koşulsuz `main()` olursa:

```python
def main():
    x = int(input("What's x? "))
    print("x squared is", square(x))


def square(n):
    return n * n


main()
```

```text
$ pytest test_calculator.py
=================== test session starts ===================
collected 0 items / 1 error

========================= ERRORS ==========================
___________ ERROR collecting test_calculator.py ___________
test_calculator.py:1: in <module>
    from calculator import square
calculator.py:10: in <module>
    main()
calculator.py:2: in main
    x = int(input("What's x? "))
            ^^^^^^^^^^^^^^^^^^^
...\site-packages\_pytest\capture.py:229: in read
    raise OSError(
E   OSError: pytest: reading from stdin while output is captured!  Consider using `-s`.
--------------------- Captured stdout ---------------------
What's x? 
================= short test summary info =================
ERROR test_calculator.py - OSError: pytest: reading from ...
!!!!!!!!! Interrupted: 1 error during collection !!!!!!!!!!
========================= 1 error =========================
```

Test dosyası `square`'i içe aktarınca `calculator.py` baştan sona çalıştı,
`main` de çağrıldı ve `input` girdi bekledi. `pytest` testler çalışırken girdi
vermediği için durdu. Çözüm: son satırı `if __name__ == "__main__":` içine
al.

## Adı test_ ile başlamayan fonksiyon

```python
from calculator import square


def positive():
    assert square(2) == 4
    assert square(3) == 9


def negative():
    assert square(-2) == 4
    assert square(-3) == 9


def zero():
    assert square(0) == 0
```

```text
$ pytest test_calculator.py
=================== test session starts ===================
collected 0 items

======================= no tests ran ======================
```

Hata yok ama hiçbir test de çalışmadı (`no tests ran`). `pytest` yalnızca
adı `test_` ile başlayan fonksiyonları test sayar.

## Yazan ama döndürmeyen fonksiyon

Fonksiyon sonucu `print` ile yazıyorsa değeri `None`'dır ve
`assert hello("David") == "hello, David"` şöyle düşer:
`assert None == 'hello, David'`. Program doğru çalışıyor gibi görünse de test
edilemez. Fonksiyon `return` etsin, `main` yazsın.

## Hata vermeyen yanlışlar

Geçen bir test, kodun doğru olduğunu kanıtlamaz; yalnızca denediğin
durumlarda doğru olduğunu gösterir. `*` yerine `+` yazılmış `calculator.py`
ile:

```python
from calculator import square


def test_square():
    assert square(2) == 4
```

```text
$ pytest test_calculator.py
=================== test session starts ===================
collected 1 item

test_calculator.py .                                 [100%]

========================= 1 passed ========================
```

Test geçti, çünkü `2 + 2` de 4. Yanlış kodu ancak onu ele veren bir durum
yakalar: 3, eksi sayılar. Odyssey testlerini bu yüzden bozuk sürümlerle de
çalıştırıyor.
