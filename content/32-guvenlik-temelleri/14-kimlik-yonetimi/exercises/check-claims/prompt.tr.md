İmzası doğrulanmış bir jetonun iddiaları `claims` sözlüğünde.

`check_claims(claims, issuer, audience, now)` şu denetimleri **bu sırayla**
yapsın ve ilk tutmayanın adını döndürsün:

1. `iss` `issuer` değilse `"bad-issuer"`
2. `aud` `audience` değilse `"bad-audience"`
3. `now >= exp` ise `"expired"` (`exp` yoksa da)
4. `nbf` varsa ve `now < nbf` ise `"not-yet-valid"`

Hepsi geçerse `"ok"`. Olmayan iddia için `claims.get(...)` kullan.

**Beklenen çıktı:**

```
50 not-yet-valid
500 ok
1000 expired
bad-audience
```
