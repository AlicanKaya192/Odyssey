Ayar dosyaları genelde `anahtar=deger` biçiminde satırlardan oluşuyor. Bazı
satırlar bozuk olabiliyor. Bu alıştırmada bozuk satırı **fonksiyon bildirecek**,
çağıran taraf da onu yakalayıp devam edecek.

**Yapman gerekenler:**

1. `parse_line` adında bir fonksiyon yaz:
   - Satırda `=` **yoksa** `ValueError` çıkar. Mesajı tam olarak
     `bad line: ` + satırın kendisi olsun.
   - Varsa satırı ilk `=` işaretinden ikiye böl ve ikisini birden döndür.

2. Şu satırları sırayla işle:

```python
lines = ["name=Ada", "broken", "city=London"]
```

3. `settings` adında boş bir sözlükle başla.
   - Satır çözülürse anahtarı ve değeri sözlüğe koy.
   - `ValueError` çıkarsa **hatanın mesajını** yazdır ve devam et.

4. Döngü bitince `settings` sözlüğünü yazdır.

**Beklenen çıktı:**

```
bad line: broken
{'name': 'Ada', 'city': 'London'}
```

> Bir metni ikiye bölmek için `line.split("=", 1)` kullanıyorsun; ikinci
> argüman "en fazla bir kez böl" demek. Değerin içinde `=` varsa bu önemli.
> Hata çıkmadığında çalışacak kodu `else` bloğuna koyabilirsin.
