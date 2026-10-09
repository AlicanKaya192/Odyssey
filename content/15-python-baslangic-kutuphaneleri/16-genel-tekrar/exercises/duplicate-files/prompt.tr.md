Yanında alt klasörlü bir `files` klasörü var; bazı dosyaların içeriği
aynı. `duplicate_files(folder)` fonksiyonunu yaz: bütün dosyaları (`rglob`)
içeriklerine göre gruplasın (`defaultdict(list)`, anahtar `read_text`),
**birden fazla** dosyası olan grupları al. Her grup, `folder`'a göre göreli
ve `/` ayıraçlı yolların **sıralı** listesi olsun; grupların listesi de
sıralı dönsün.

**Beklenen çıktı:**

```
['a.txt', 'copy/a2.txt', 'notes.txt']
['b.txt', 'c.txt']
```
