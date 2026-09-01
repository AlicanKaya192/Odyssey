Bir kabın içinde başka bir kap olabiliyor. Bu alıştırmada onu belirteceksin.

**Yapman gerekenler:**

1. `grades` adında bir sözlük tanımla ve belirtimini yaz. Anahtarları metin,
   **değerleri sayı listesi**. Başlangıç değeri:

```python
{"Ada": [90, 85], "Alan": [70, 95]}
```

2. `best` adında bir fonksiyon yaz:
   - Parametresi `records`, `grades` ile aynı biçimde bir sözlük.
   - Geriye metin anahtarlı, **tek sayı** değerli bir sözlük döndürüyor.
   - Her ismin listesindeki **en yüksek** notu buluyor.

3. `best(grades)` sonucunu yazdır.

**Beklenen çıktı:**

```
{'Ada': 90, 'Alan': 95}
```

Dikkat: parametrenin belirtimi ile dönüşün belirtimi **aynı değil**. Giren
sözlüğün değerleri liste, çıkan sözlüğün değerleri tek sayı.

> Bir listedeki en büyük değeri `max(values)` veriyor.
