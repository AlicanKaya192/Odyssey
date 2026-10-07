Göndermek istediğin kayıtta JSON'un tanımadığı türler var: bir **küme**, bir
**demet** ve **sayı anahtarlı** bir sözlük. `json.dumps(record)` küme yüzünden
hata veriyor.

**Yapman gerekenler:**

1. `record`'dan `clean` adlı yeni bir sözlük kur:
   - `id` aynı kalsın,
   - `tags` kümesi **sıralı** bir liste olsun (`sorted`),
   - `coords` demeti liste olsun,
   - `scores` sözlüğünün anahtarları metne çevrilsin (`str`).
2. `text = json.dumps(clean, sort_keys=True)` ile metne çevir ve yazdır.
3. `back = json.loads(text)` ile geri oku ve `back == clean` sonucunu
   yazdır. `True` çıkmalı: temizlenmiş kayıt gidip geri geldiğinde aynı
   kalıyor.

**Beklenen çıktı:**

```
{"coords": [38.42, 27.14], "id": 7, "scores": {"2023": 4.5, "2024": 4.8}, "tags": ["classic", "english", "novel"]}
same after round trip: True
```

Temizlemeden `record`'u gönderseydin, demet liste olarak, sayı anahtarlar
metin olarak geri gelirdi ve `back == record` `False` çıkardı.
