`files` dosya adlarını içeriklerine eşleyen bir sözlük. `find_secrets(files)` fonksiyonunu yaz; koda yazılmış gizli değerleri bulup şu biçimde satırların listesini döndürsün:

- `"ad:satır: api-key"`: satırda `API_KEY` deseni varsa.
- `"ad:satır: password"`: satırda `PASSWORD` deseni varsa.

Dosyalar ada göre **sıralı** gezilir, satırlar 1'den sayılır. Aynı satırda ikisi de varsa önce `api-key`. Desenler hazır; `DESEN.search(line)` eşleşme bulursa doğru sayılır.

**Beklenen çıktı:**

```
old_config.py:1: api-key
settings.py:2: password
```
