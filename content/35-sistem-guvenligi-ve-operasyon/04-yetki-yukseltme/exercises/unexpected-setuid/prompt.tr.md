`unexpected_setuid(files, allowed)` setuid biti açık (`mode & 0o4000`)
olup `allowed` listesinde olmayan dosyaların yollarını abece sırasıyla
döndürsün.

**Beklenen çıktı:**

```
/opt/app/helper
/opt/tools/report-tool
```
