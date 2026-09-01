Sözlükte olmayan bir anahtar `KeyError`, listede olmayan bir sıra numarası
`IndexError` veriyor. İkisi de "aradığın şey orada yok" demek, yani ikisine
de aynı cevabı verebilirsin.

**Yapman gerekenler:**

1. `lookup` adında bir fonksiyon yaz. İki şey alsın: `data` ve `key`.
2. `data[key]` değerini döndürmeyi dene.
3. `KeyError` **veya** `IndexError` çıkarsa `"missing"` döndür.
4. Fonksiyonu şu dört çağrıyla dene ve sonuçları yazdır:

```python
lookup({"a": 1}, "a")
lookup({"a": 1}, "b")
lookup([10, 20], 1)
lookup([10, 20], 5)
```

**Beklenen çıktı:**

```
1
missing
20
missing
```

Dikkat: aynı fonksiyon hem sözlükle hem listeyle çalışıyor. `data[key]`
yazımı ikisinde de geçerli — sözlükte anahtar, listede sıra numarası.

> Birden fazla hatayı tek `except` ile yakalamak için parantez içinde
> virgülle yazıyorsun: `except (KeyError, IndexError):`
