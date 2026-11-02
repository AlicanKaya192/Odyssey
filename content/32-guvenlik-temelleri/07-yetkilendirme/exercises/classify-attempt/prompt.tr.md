Rollerin sırası: `"user"` < `"moderator"` < `"admin"`.

`classify_attempt(user, user_role, owner, required_role)` bir erişim
denemesini sınıflandırsın:

1. `user_role`, `required_role`'dan **düşükse** → `"vertical"`.
2. Değilse; `owner` `None` değil, `user`'dan farklı ve `user_role`
   `"user"` ise → `"horizontal"`.
3. Öteki durumlar → `"allowed"`.

Rolleri sıralamak için `{"user": 1, "moderator": 2, "admin": 3}` gibi bir
sözlük kullan; metinleri doğrudan `<` ile karşılaştırma (abece sırası
verir).

**Beklenen çıktı:**

```
allowed
horizontal
vertical
allowed
```
