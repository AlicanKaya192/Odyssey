Bir Python uygulaması için bu patikada öğrendiğin her şeyi birleştiren
örnek Dockerfile. Kendi projelerinde başlangıç noktası olarak kullan.

```dockerfile
# 1) Sabit sürümlü, küçük, resmî taban
FROM python:3.13-slim

# 2) Python için iyi varsayılanlar
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

# 3) Root olmayan kullanıcı
RUN useradd --create-home --uid 1000 app

WORKDIR /app

# 4) Önce bağımlılıklar (önbellek), önbelleksiz pip
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 5) Sonra kod, sahibi kullanıcı
COPY --chown=app:app . .

# 6) Yazılacak veri klasörü kullanıcıya ait
RUN mkdir -p /data && chown app:app /data
VOLUME /data

# 7) Kullanıcıya geç
USER app

# 8) Belgelenmiş port, sağlık denetimi, exec biçimi
EXPOSE 8000
HEALTHCHECK --interval=10s --timeout=3s --retries=3 \
  CMD python -c "import urllib.request as u; u.urlopen('http://localhost:8000/health')"
CMD ["python", "app.py"]
```

Yanında olması gerekenler:

- `.dockerignore`: `.git`, `.venv`, `**/__pycache__`, `.env`, `data/`.
- `.env.example`: ayarların adları, sahte değerlerle.

Çalıştırırken:

```text
docker run -d --name app -p 8000:8000 --env-file .env -v appdata:/data `
  --memory 512m --cap-drop ALL app
```
