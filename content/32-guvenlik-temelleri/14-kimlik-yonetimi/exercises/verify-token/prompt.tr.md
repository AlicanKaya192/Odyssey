Oyuncak jeton iki parçalı: `govde.imza`. Gövde JSON'un base64url
kodlaması, imza gövdenin `key` ile HMAC-SHA256 özeti (hex). `make_token`
hazır.

`verify_token(token, key)` şunu döndürsün:

- nokta sayısı 1 değilse `"malformed"`,
- imza tutmuyorsa `"bad-signature"` (`hmac.compare_digest` ile),
- gövde çözülemiyorsa `"malformed"`,
- yoksa iddiaların sözlüğü.

İmzayı **gövdeyi çözmeden önce** denetle.

**Beklenen çıktı:**

```
{'sub': 'ada', 'role': 'user'}
bad-signature
bad-signature
malformed
```
