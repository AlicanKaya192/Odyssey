Konteyner şu hatayla bitiyor:

```text
python: can't open file '/app/app.py': [Errno 2] No such file or directory
```

`docker run --rm --entrypoint ls app -la /app` boş bir klasör gösteriyor.

**Yapman gereken:** `app.py`'nin programın aradığı yere (çalışma klasörüne)
kopyalanmasını sağla.

**Beklenen çıktı:**

```
debugged and running
```
