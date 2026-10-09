Yanında `app.log` var; satırlar `2026-03-15 10:02:11 ERROR [db] mesaj`
biçiminde, arada bir bozuk satır da var. `log_levels(path)` fonksiyonunu yaz:
dosyayı `pathlib` ile okusun, her satırı `re.fullmatch` ile ayrıştırsın
(kalıp: `\S+ \S+ (\w+) \[\w+\] .+`), uyan satırların düzeylerini `Counter`
ile saysın ve sözlük olarak döndürsün. Uymayan satırı atlasın.

**Beklenen çıktı:**

```
ERROR 2
INFO 2
WARNING 1
```
