`sign` hazır. `verify(secret, ts, now, body, signature)` önce zamana
baksın: `abs(now - ts) > 300` ise `"expired"`. Sonra imzayı kendisi
yeniden hesaplayıp `hmac.compare_digest` ile karşılaştırsın: tutmazsa
`"bad signature"`, tutarsa `"ok"`.

**Beklenen çıktı:**

```
ok
bad signature
expired
```
