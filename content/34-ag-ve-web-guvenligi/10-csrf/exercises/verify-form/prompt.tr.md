`sessions` oturum kimliği → CSRF jetonu sözlüğü. `verify(sessions, sid,
form)` oturumun jetonu varsa ve formdaki `"csrf"` değeri onunla
`hmac.compare_digest` ile eşleşiyorsa `"ok"`, aksi hâlde `"rejected"`
döndürsün. Formda jeton yoksa ya da oturum bilinmiyorsa da
`"rejected"`.

**Beklenen çıktı:**

```
ok
rejected
rejected
rejected
```
