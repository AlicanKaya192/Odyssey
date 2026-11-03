`password_problems(password, user, common)` sorunların listesini
**bu sırayla** döndürsün: 8 karakterden kısaysa `"too short"`; küçük
harfe çevrilmiş hâli `common` içindeyse `"common"`; kullanıcı adını
(büyük/küçük harf duyarsız) içeriyorsa `"contains user name"`.

**Beklenen çıktı:**

```
qwerty ['too short', 'common']
Ada2026! ['contains user name']
blue-river-under-stone []
PASSWORD ['common']
```
