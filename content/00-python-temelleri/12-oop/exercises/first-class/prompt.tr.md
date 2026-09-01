İlk sınıfını yazacaksın.

**Yapman gerekenler:**

1. `Book` adında bir sınıf yaz.
2. Kurucusu (`__init__`) iki şey alsın: `title` ve `pages`. İkisini de
   nesnenin özelliği yap.
3. `is_long` adında bir metot yaz: sayfa sayısı **300 veya üstü** ise `True`,
   değilse `False` döndürsün.
4. İki kitap kur ve sonuçları yazdır:
   - `long_book` — `"Ulysses"`, 730 sayfa
   - `short_book` — `"Notes"`, 120 sayfa

**Beklenen çıktı:**

```
Ulysses
True
Notes
False
```

Sırayla: uzun kitabın başlığı, `is_long` sonucu, kısa kitabın başlığı,
`is_long` sonucu.

> Her metodun ilk parametresi `self` olmak zorunda. Nesnenin verisine
> `self.pages` ile ulaşıyorsun.
