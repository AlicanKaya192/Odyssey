`write_people(path, people)` fonksiyonunu yaz: `people` sözlük listesini
`csv.DictWriter` ile dosyaya yazsın; sütunlar ilk sözlüğün anahtarları
(`list(people[0])`), önce başlık satırı. Sonra dosyayı okuyup satırlarını
liste olarak döndürsün (`read().splitlines()`).

**Beklenen çıktı:**

```
name,city
Ada,"London, UK"
Alan,Wilmslow
```
