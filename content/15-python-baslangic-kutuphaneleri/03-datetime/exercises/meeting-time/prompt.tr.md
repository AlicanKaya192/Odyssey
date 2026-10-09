`meeting_time(local, from_zone, to_zone)` fonksiyonunu yaz: `local`
`"2026-03-15 14:30"` biçiminde, `from_zone` saat diliminde bir an. Onu
`to_zone` saat diliminde gösterip yalnızca saati `"07:30"` biçiminde
döndürsün. Adımlar: `strptime`, `replace(tzinfo=ZoneInfo(from_zone))`,
`astimezone(ZoneInfo(to_zone))`, `strftime("%H:%M")`.

**Beklenen çıktı:**

```
07:30
17:00
```
