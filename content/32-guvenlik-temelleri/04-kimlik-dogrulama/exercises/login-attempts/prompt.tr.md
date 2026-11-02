Bir hesaba yapılan giriş denemeleri sırayla `events` listesinde:
`"right"` (doğru parola) ya da `"wrong"` (yanlış parola).

`login_attempts(events, limit)` her deneme için bir sonuç listesi
döndürsün:

- doğru parola → `"ok"` ve art arda yanlış sayacı sıfırlanır,
- yanlış parola → `"fail"`; art arda yanlış sayısı `limit`'e ulaşınca
  hesap **kilitlenir**,
- kilitlendikten sonraki her deneme, parola doğru olsa bile → `"locked"`.

**Beklenen çıktı:**

```
fail ok fail fail fail locked locked
fail locked
```
