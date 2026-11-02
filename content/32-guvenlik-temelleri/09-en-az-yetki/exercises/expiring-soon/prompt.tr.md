Her yetki `[kullanici, kaynak, bitis_tarihi]` listesi; tarih ISO biçiminde
(`"2026-11-05"`).

`expiring_soon(grants, today, days)` süresi **henüz dolmamış** (bitiş
tarihi ≥ bugün) ve en geç `days` gün sonra dolacak (bitiş tarihi ≤ bugün +
`days`) yetkileri `"kullanici:kaynak"` metinleri olarak abece sırasında
döndürsün. `today` da ISO metni.

`date.fromisoformat` metni tarihe, `timedelta(days=n)` gün farkına çevirir
(ikisi de `datetime` modülünde).

**Beklenen çıktı:**

```
['ada:prod-db', 'linus:logs']
```
