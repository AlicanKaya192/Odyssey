Dockerfile `COPY . .` ile her şeyi kopyalıyor; `.env`'deki anahtar da
imaja giriyor.

**Yapman gereken:** `.dockerignore` dosyasına `.env` ve `notes.txt`'yi yaz.
Odyssey imajı kurup içinde bu iki dosyanın **olmadığını** denetleyecek.

`app.py` çalışma klasöründeki dosyaları yazdırıyor. **Beklenen çıktı:**

```
files: ['.dockerignore', 'Dockerfile', 'app.py']
```

(`.dockerignore` ve `Dockerfile` da imaja girdi; istersen onları da
dışarıda bırakabilirsin, ama bu alıştırmada beklenen çıktı bu.)
