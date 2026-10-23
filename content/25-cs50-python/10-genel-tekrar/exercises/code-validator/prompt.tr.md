Bir depodaki ürün kodları şu kurala uyuyor: iki **büyük** harf, bir tire, dört rakam; rakamların ilki 0 olamaz (`AB-1234` geçerli, `AB-0123`, `ab-1234`, `AB1234`, `AB-12345` geçersiz). Kodun başında ve sonunda başka bir şey olamaz. `validate.py`'de `is_valid(code)` bunu bir düzenli ifadeyle denetleyip `True` ya da `False` döndürsün; `main` kodu sorup `Valid` ya da `Invalid` yazsın.

Sonra `test_validate.py`'ye `is_valid`'i sınayan, adı `test_` ile başlayan fonksiyonlar yaz.

Örnek çalıştırma (soru metnini istediğin gibi yazabilirsin, yalnızca çıktın denetlenir):

```text
$ python validate.py
Code: AB-1234
Valid
```

Testlerin için: Odyssey `test_validate.py`'yi önce **senin** `validate.py`'ınla çalıştırır (hepsi geçmeli), sonra `validate.py`'ın bilerek bozulmuş sürümleriyle (her birinde testlerinden en az biri düşmeli).
