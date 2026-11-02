`stats` program adından iki sayıya giden bir sözlük: `files_written` ve
`extensions_changed`.

`ransomware_alert(stats, min_writes, min_ratio)` şüpheli programların
adlarını abece sırasında döndürsün: yazdığı dosya sayısı `min_writes`'a eşit
ya da büyük **ve** uzantı değiştirme oranı (`extensions_changed /
files_written`) `min_ratio`'dan büyük. Hiç dosya yazmayan program şüpheli
değildir (sıfıra bölme yapma).

**Beklenen çıktı:**

```
['unknown.exe']
['renamer.exe', 'unknown.exe']
```
