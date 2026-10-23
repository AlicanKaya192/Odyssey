Testler artık `test` klasöründe. İçinde boş bir `__init__.py` ve `hello.py`'nin testleri (`test_hello.py`) hazır duruyor. Aynı klasöre, `test/test_calculator.py`'ye `calculator.py`'deki `square` için testler yaz.

Odyssey CS50'nin `pytest test` komutu gibi klasördeki iki dosyayı da çalıştırır; hepsi geçmeli ve `square`'in bozuk sürümlerini (`n + n`, eksi sonuç) senin testlerin yakalamalı.
