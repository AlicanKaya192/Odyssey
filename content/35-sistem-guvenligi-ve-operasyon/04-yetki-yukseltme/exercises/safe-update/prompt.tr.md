`safe_update(user, changes, allowed)` kullanıcının **kopyasını**
döndürsün; `changes` içindeki alanlardan yalnızca `allowed` listesinde
olanları yazsın. Asıl `user` sözlüğü değişmesin. Başlangıç kodu her alanı
asıl sözlüğe yazıyor: istekteki `role` kullanıcıyı yönetici yapıyor.

**Beklenen çıktı:**

```
ada@x.io user
a@x.io user
```
