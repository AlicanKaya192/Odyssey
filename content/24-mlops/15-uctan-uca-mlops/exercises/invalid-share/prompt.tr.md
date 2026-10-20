Doğrulama adımı için `invalid_share(rows, limits)` fonksiyonunu yaz:

- `limits`: `{sütun: [alt, üst]}`.
- Bir satır, `limits`'teki sütunlardan biri eksikse (`None` ya da hiç yok) ya da aralığın dışındaysa geçersizdir.
- Geçersiz satırların payını üç basamağa yuvarlanmış döndür.

**Beklenen çıktı:**

```
0.75
0.0
```
