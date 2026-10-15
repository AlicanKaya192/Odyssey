**Hangi etiket ne zaman?**

| Ne zaman | Etiket | Değişir mi? |
|---|---|---|
| Her derlemede | Commit kimliği (`4f2a9c8`) | Hayır |
| `main`'e gönderimde | `latest` | Evet, her gönderimde |
| `v1.4.2` etiketinde | `1.4.2` ve `1.4` | `1.4.2` hayır, `1.4` evet |

- Dağıtımda **değişmeyen** etiket kullan (SHA ya da tam sürüm). `latest`
  ile dağıtılmış bir sunucuyu "öncekine" döndüremezsin.
- Dal derlemesine `latest` verme.

**Katman önbelleği**

- Bir adım değişince o adım ve **sonraki her adım** yeniden çalışır.
- Hattın makinesi her seferinde sıfırdan: önbellek `cache-from` /
  `cache-to` ile.
- Dockerfile'da sık değişen dosya en sona:

```text
FROM python:3.13-slim
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["python", "app.py"]
```

**Servis: işin yanında veritabanı**

```yaml
    services:
      postgres:
        image: postgres:17
        env:
          POSTGRES_PASSWORD: test
        ports:
          - "5432:5432"
        options: >-
          --health-cmd "pg_isready -U postgres"
          --health-interval 5s
          --health-retries 10
```

| Parça | Neden |
|---|---|
| `ports` | Testler `localhost:5432`'ye bağlanır |
| Sağlık denetimi | Veritabanı hazır olmadan testler başlamasın |
| Tırnaklı port | `22:22` gibi değerler bazı okuyucularda altmışlık sayı olur |
| Düz şifre | Sorun değil: veritabanı yalnızca bu iş boyunca var |

**Sık hatalar**

| Belirti | Neden |
|---|---|
| `docker run` imajı bulamıyor | `load: true` yazılmamış |
| Gönderim izin hatası veriyor | `packages: write` izni yok |
| Gönderim ad hatası veriyor | İmaj adında büyük harf |
| Testler bazen bağlanamıyor | Serviste sağlık denetimi yok |
| Her derleme dakikalarca sürüyor | Önbellek yok ya da `COPY . .` kurulumdan önce |
