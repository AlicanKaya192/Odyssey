Kontrol listesinin her maddesi için bakılacak komut. İmajın adı `app`,
konteynerin adı `web` varsayılıyor (Compose'da `docker compose ps` adı
gösterir).

## İmaj

| Soru | Komut | Beklenen |
|---|---|---|
| Kullanıcı root değil mi? | `docker run --rm app id` | `uid=1000(app)` |
| Çalışma klasörü doğru mu? | `docker inspect app --format "{{.Config.WorkingDir}}"` | `/app` |
| Varsayılan ayarlar var mı? | `docker inspect app --format "{{.Config.Env}}"` | `DB_PATH=... PORT=...` |
| Sağlık denetimi tanımlı mı? | `docker inspect app --format "{{json .Config.Healthcheck}}"` | `{"Test":["CMD","python",...` |
| `.env` imaja girmiş mi? | `docker run --rm app ls -a /app` | `.env` **yok** |
| Boyut makul mü? | `docker images app` | ~176 MB (`slim` taban) |
| Hangi katman ne kadar? | `docker history app` | Kendi katmanların KB düzeyinde |

## Çalışan konteyner

| Soru | Komut | Beklenen |
|---|---|---|
| Sağlıklı mı? | `docker ps` | `(healthy)` |
| Denetim neden düşüyor? | `docker inspect web --format "{{json .State.Health}}"` | Son denetimlerin çıktısı |
| Dışarıdan ulaşılıyor mu? | `curl localhost:8095/health` | `{"status": "ok"}` |
| Günlük ekranda mı? | `docker logs web` | `listening on port 8000...` |
| Düzgün kapanıyor mu? | `docker stop web` sonra `docker ps -a` | 1 saniye civarı, `Exited (0)` |
| Veri volume'da mı? | `docker inspect web --format "{{json .Mounts}}"` | `"Type":"volume"`, `/data` |

## Veri

```text
docker compose down
docker compose up -d
curl localhost:8095/stats       # notlar yerinde, starts bir arttı
```

`Exited (137)` görüyorsan program SIGTERM'i duymadı ve 10 saniye sonra
öldürüldü: `CMD` exec biçiminde mi, sinyal yakalanıyor mu?
