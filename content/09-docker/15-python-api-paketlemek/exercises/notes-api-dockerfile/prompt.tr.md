Dersteki not API'si (`app.py`) hazır. Ona bir Dockerfile yaz.

**Yapman gerekenler:**

1. Taban `python:3.13-slim`, çalışma klasörü `/app`.
2. **Önce** `requirements.txt`'i kopyala ve paketleri
   `pip install --no-cache-dir -r requirements.txt` ile kur.
3. **Sonra** `app.py` ve `healthcheck.py`'yi kopyala.
4. `EXPOSE 8000`.
5. Exec biçiminde `CMD`: `python app.py`.

Odyssey imajı kurup çalıştıracak ve `/health` adresine istek atacak:

```
{"status": "ok"}
```
