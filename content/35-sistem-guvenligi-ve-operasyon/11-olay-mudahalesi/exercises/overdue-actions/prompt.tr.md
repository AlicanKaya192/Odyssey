Her eylem maddesi `[kimlik, sahip, son_tarih, bitti]`. `overdue_actions(actions,
today)` bitmemiş ve son tarihi `today`'den **önce** olan maddeleri
`"<kimlik> <sahip> <son_tarih>"` satırları olarak döndürsün; önce son
tarihe, sonra kimliğe göre sıralı. Tarihleri `date.fromisoformat` ile
karşılaştır.

**Beklenen çıktı:**

```
A-5 ada 2026-10-01
A-1 bob 2026-10-20
A-4 bob 2026-10-20
```
