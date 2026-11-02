Parola Saklama ve Kimlik Doğrulama bölümlerini birleştir. `users`
kullanıcı → `{"salt": hex, "hash": hex}`, `attempts` `[kullanici, parola]`
denemeleri. `hash_password` hazır.

`run_logins(users, attempts, max_fail)` her deneme için bir sonuç
listesi döndürsün:

- kullanıcı yoksa `"unknown user"`,
- hesap kilitliyse `"locked"`,
- özet tutuyorsa `"ok"` (`hmac.compare_digest` ile) ve o kullanıcının
  hata sayısı sıfırlanır,
- tutmuyorsa `"bad password"`; üst üste `max_fail` hatada hesap kilitlenir
  ve sonraki her denemesi `"locked"` olur.

**Beklenen çıktı:**

```
ada bad password
ada ok
bora bad password
bora bad password
bora bad password
bora locked
zeynep unknown user
```
