**Özet fonksiyonları.** `manifest` her dosya adını beklenen SHA-256
özetine (onaltılık) eşliyor; `files` adı içeriğe eşliyor.
`changed_files(files, manifest)` manifestteki dosyalardan **eksik olanların
ya da içeriği değişmiş olanların** adlarını sıralı liste olarak döndürsün.
İçeriğin özeti `hashlib.sha256(içerik.encode()).hexdigest()`. Başlangıç
kodu yalnızca eksikleri buluyor.

**Beklenen çıktı:**

```
['config.json', 'readme.md']
```
