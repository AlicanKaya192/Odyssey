Öğrencilerin bilgileri sayı anahtarlı sözlüklerde ve bir kümede duruyor. Bunları
JSON'un bozmadan taşıyabileceği bir rapora çevir.

**Yapman gerekenler:**

1. Önce sorunu gör: `names`'i JSON'a çevirip geri oku
   (`json.loads(json.dumps(names))`) ve yazdır.
2. `report` adında bir sözlük kur:
   - `"tags"`: kümenin **sıralı listesi** (`sorted(tags)`),
   - `"students"`: her öğrenci için `{"id": ..., "name": ..., "average": ...}`
     sözlüklerinin listesi (id sırasıyla; ortalama **tam bölme**).
3. `report`'u `report.json` dosyasına `indent=2` ile yaz ve `back` adıyla
   geri oku.
4. Yazdır: `back["tags"]`, her öğrencinin id, ad ve ortalaması (bir satırda)
   ve ilk öğrencinin `id`'sinin türü.

**Beklenen çıktı:**

```text
{'1': 'Ada', '2': 'Alan', '3': 'Grace'}
['files', 'json', 'python']
1 Ada 87
2 Alan 82
3 Grace 90
<class 'int'>
```

Sayı **anahtar** olunca metne dönüyor; **değer** olunca sayı kalıyor.
