Derste gördüğün gibi e-posta adreslerini kendi kalıbınla doğrulamak zor. Bu kez işi yaygın bir kütüphaneye bırak: `validators` (Odyssey'de kurulu). `response.py` kullanıcıdan bir e-posta adresi alır (baştaki ve sondaki boşlukları atarak) ve geçerliyse `Valid`, değilse `Invalid` yazar. `validators.email(adres)` geçerli adreste `True`, geçersizde yanlış sayılan bir hata nesnesi döndürür; `if` ile sorabilirsin. Kendi düzenli ifadeni yazma, `re` gerekmiyor.

Örnek çalıştırma (soru metnini istediğin gibi yazabilirsin, yalnızca çıktın denetlenir):

```text
$ python cozum.py
Email: malan@harvard.edu
Valid
```

## Nasıl denenir

- Girdi `malan@harvard.edu` → çıktı `Valid`
- Girdi `  malan@cs50.harvard.edu ` → çıktı `Valid`
- Girdi `malan@@@harvard.edu` → çıktı `Invalid`
- Girdi `malan@harvard` → çıktı `Invalid`
- Girdi `malan.harvard.edu` → çıktı `Invalid`
