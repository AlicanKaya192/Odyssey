Sınıf, liste ve tip belirtimlerini bir arada kullanacaksın.

**Yapman gerekenler:**

1. `Task` sınıfı:
   - Kurucusu `title` (metin) ve `done` (mantıksal, varsayılan `False`) alsın.
   - `finish` metodu: `done` değerini `True` yapsın ve bir şey döndürmesin.
   - `__str__` metodu: bitmişse `[x] baslik`, bitmemişse `[ ] baslik`
     **döndürsün**.

2. `Board` sınıfı:
   - Kurucusu **boş bir** `tasks` listesi kursun. Listenin belirtimini yaz:
     `list[Task]`
   - `add` metodu: bir `Task` alsın, listeye eklesin, **listedeki toplam
     sayıyı** döndürsün.
   - `pending` metodu: bitmemiş görevlerin **başlıklarını** liste olarak
     döndürsün. Dönüş belirtimi `list[str]` olsun.

3. Bir `Board` kur, üç görev ekle: `"write"`, `"test"`, `"ship"`.
   İkincisini bitir.
4. Sırayla şunları yazdır: görev sayısı, ikinci görevin metin hâli,
   bekleyen başlıklar.

**Beklenen çıktı:**

```
3
[x] test
['write', 'ship']
```

> `tasks` listesini **`__init__` içinde** kur, sınıf seviyesinde değil.
