`original` ve `restored` dosya adı → içerik (metin). `restore_check(original,
restored)` ada göre abece sırasıyla satırlar döndürsün: aslı olan her dosya
için `"<ad>: ok"`, `"<ad>: different"` ya da `"<ad>: missing"`; yalnızca
geri yüklenende olan dosya için `"<ad>: extra"`. İçerikleri SHA-256
özetleriyle karşılaştır.

**Beklenen çıktı:**

```
keys.txt: missing
orders.csv: ok
tmp.log: extra
users.csv: different
```
