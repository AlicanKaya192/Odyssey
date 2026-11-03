`record` bir sıfırlama kaydı (`hash`, `expires`, `used`) ya da `None`.
`status(record, token, now)` şunları **bu sırayla** denetleyip döndürsün:
kayıt yoksa `"invalid"`; kullanılmışsa `"used"`; `now >= expires` ise
`"expired"`; jetonun SHA-256 özeti `hmac.compare_digest` ile tutmazsa
`"invalid"`; yoksa `"ok"`.

**Beklenen çıktı:**

```
ok
invalid
expired
used
invalid
```
