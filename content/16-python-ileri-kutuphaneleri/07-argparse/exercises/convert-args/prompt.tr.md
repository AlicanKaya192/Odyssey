`convert_args(argv)` fonksiyonunu yaz: bir ya da daha çok dosya adı
(`nargs="+"`) ve `csv` ya da `json` olabilen `--format` (varsayılan `csv`,
`choices`) tanımlasın; `[dosyalar, biçim]` listesini döndürsün.

**Beklenen çıktı:**

```
[['a.txt', 'b.txt'], 'json']
[['x.txt'], 'csv']
```
