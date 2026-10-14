`resilient(spec, deadline)` en fazla 5 deneme yapsın (`ChatClient`,
`MESSAGES`, `max_tokens=40`). Her geçici hatada hatanın metnini
(`str(error)`) `log`'a eklesin. Sıradaki bekleme `2.0 ** attempt`;
son denemedeyse ya da beklemelerin toplamı bu beklemeyle `deadline`'ı
aşacaksa beklemeden `[FALLBACK, beklemeler, log]` döndürsün. Yoksa
beklemeyi listeye ekleyip yeniden denesin. Cevap gelince `[cevap,
beklemeler, log]`.

**Beklenen çıktı:**

```
ok 1.0 503
fallback 7.0 429,429,429,429
fallback 15.0 429,429,429,429,429
```
