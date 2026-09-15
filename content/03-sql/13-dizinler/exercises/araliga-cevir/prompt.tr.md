1 Haziran 2025'teki satın almaları (`event_type` `'purchase'`) getiren bu
sorgu doğru sonuç veriyor:

```sql
SELECT id, created_at, amount FROM events
WHERE event_type = N'purchase'
  AND YEAR(created_at) = 2025 AND MONTH(created_at) = 6
  AND DAY(created_at) = 1
ORDER BY created_at;
```

Ama `created_at`'e bir dizin kurulsa bile onu **kullanamıyor**: sütun bir
işlevin içinde. Ölçüldü: dizin varken bu yazım tabloyu taradı (150
okuma), aynı sonucu veren aralık yazımı dizinden geldi.

Aynı sonucu sütuna işlev uygulamadan yaz. Sütunlar: `id`, `created_at`,
`amount`; `created_at`'e göre sırala. Sonuç 15 satır:

```
id    created_at           amount
----  -------------------  ------
8699  2025-06-01T00:35:00  199.99
8703  2025-06-01T02:15:00  203.99
8707  2025-06-01T03:55:00  207.99
...
```

`YEAR(`, `MONTH(` ve `DAY(` denetim tarafından yasak.
