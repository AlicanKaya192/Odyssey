Dosyaların ilk baytları onaltılık metin olarak verilir. İki fonksiyon:

- `file_kind(header_hex)`: `25504446` → `"pdf"`, `89504e47` → `"png"`,
  `504b0304` → `"zip"` ile başlıyorsa o türü, yoksa `"unknown"` (büyük-küçük
  harf fark etmez).
- `mismatches(files)`: ad → onaltılık başlık; türü bilinen ama uzantısıyla
  uyuşmayan dosyaların adlarını abece sırasıyla döndürsün.

**Beklenen çıktı:**

```
pdf
zip
unknown
['photo.png']
```
