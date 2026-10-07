Dün çektiğin veri seti `known.json`'da (kimlik → kayıt), son güncelleme tarihi
`last_sync.txt`'de. Bugün yalnızca değişenleri çek ve birleştir.

**Yapman gerekenler:**

1. `last_sync.txt`'yi oku; `known.json`'u oku ve anahtarları **sayıya**
   çevirerek `known` sözlüğüne koy.
2. `GET /changes?since=<tarih>` ile değişenleri al.
3. Her değişen kaydı `known`'a yaz: kimlik varsa `updated`, yoksa `added`
   say.
4. Değişen kimlikleri, güncellenen ve eklenen sayısını, `known`'daki kayıt
   sayısını ve yeni son güncelleme tarihini (değişenlerin en büyük
   `updated` değeri) yazdır.

**Beklenen çıktı:**

```
changed: [6, 10, 13, 20, 23]
updated: 4 added: 1
records: 21
new last sync: 2024-03-14
```
