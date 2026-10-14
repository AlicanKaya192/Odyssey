Depoda bir `test_app.py` ve bir `requirements.txt` var (yan sekmelerde, salt okunur).

`.github/workflows/ci.yml` dosyası kodu indiriyor ve Python'u kuruyor, ama testleri hiç çalıştırmıyor. Yorumun yerine iki adım ekle:

- `pip install -r requirements.txt` komutunu çalıştıran bir adım
- `python -m pytest` komutunu çalıştıran bir adım

Komut çalıştıran adım `- run: komut` diye yazılır. Girintiye dikkat et: yeni adımlar öbür `- uses:` satırlarıyla aynı hizada başlar.
