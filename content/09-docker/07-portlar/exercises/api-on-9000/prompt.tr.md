`api.py` bir API; hangi portu dinlediğini dosyanın son satırında bul.

**Yapman gereken:** bu API'yi çalıştıran Dockerfile'ı yaz: `python:3.13-slim`,
çalışma klasörü `/app`, `api.py`'yi kopyala, dinlediği portu **`EXPOSE` ile
belgele**, `python api.py` çalışsın.

Odyssey iki istek atacak: `/health` → `200` ve `{"status": "ok"}`,
`/missing` → `404`.
