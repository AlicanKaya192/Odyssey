`stamp_to_text(stamp)` fonksiyonunu yaz: zaman damgasını **UTC**'de
tarihe çevirip `"2026-03-15 14:30"` biçiminde metin olarak döndürsün
(`datetime.fromtimestamp(stamp, timezone.utc)`, `strftime`).

**Beklenen çıktı:**

```
2026-03-15 14:30
1970-01-01 00:00
```
