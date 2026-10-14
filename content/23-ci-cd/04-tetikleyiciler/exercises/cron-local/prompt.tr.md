`turkey_time(cron)` fonksiyonunu yaz. Bir cron ifadesinin **Türkiye saatini** `"HH:MM"` biçiminde döndürsün:

- İlk alan dakika, ikinci alan saat (UTC).
- Türkiye saati = UTC + 3; 24'ü geçerse başa döner (`22` → `01`).
- Saat ve dakika iki haneli olsun: `"06:00"`, `"06:17"`.
- Saat alanı `*` ise: `"every hour at minute "` + dakika alanı.

**Beklenen çıktı:**

```
06:00
06:17
01:30
every hour at minute 5
```
