`make_tag` hazır. `handle(key_hex, message, tag)` **önce** etiketi
doğrulasın (`hmac.compare_digest`). Tutmazsa `"rejected"` döndürsün ve
mesajı hiç kullanmasın; tutarsa `"accepted: " + message` döndürsün.

**Beklenen çıktı:**

```
accepted: ok
rejected
rejected
```
