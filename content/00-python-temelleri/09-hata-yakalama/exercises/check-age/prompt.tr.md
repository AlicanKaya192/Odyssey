Şimdiye kadar hataları yakaladın. Bu alıştırmada **sen çıkaracaksın**.

`check_age` adında bir fonksiyon yazacaksın. Yaş eksiyse bu anlamsız bir
değer; sessizce sıfır döndürmek yerine hata çıkarması gerekiyor.

**Yapman gerekenler:**

1. `check_age(age)` fonksiyonunu yaz:
   - Yaş **eksiyse** `ValueError` çıkar, mesajı tam olarak şu olsun:
     `age cannot be negative`
   - Eksi değilse yaşı olduğu gibi döndür.

2. Aşağıdaki döngüde her değeri fonksiyona ver:

```python
for value in [25, -3, 40]:
```

   - Sonuç dönerse yazdır.
   - `ValueError` çıkarsa **hatanın mesajını** yazdır.

**Beklenen çıktı:**

```
25
age cannot be negative
40
```

Dikkat: sıfır eksi değil, yani `check_age(0)` hata vermemeli, `0`
döndürmeli.

> Hatanın mesajına ulaşmak için `except ValueError as error:` yazıp
> `print(error)` diyorsun.
