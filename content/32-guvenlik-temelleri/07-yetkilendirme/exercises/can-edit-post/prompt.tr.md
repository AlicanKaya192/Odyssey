Bir forumda gönderi sözlüğü: `id`, `author`, `locked`.
`can_edit_post(user, role, post)` şu kurallara göre `True`/`False`:

- `role` `"admin"` ya da `"moderator"` ise her gönderiyi düzenleyebilir,
- gönderinin yazarı kendi gönderisini, **kilitli değilse** düzenleyebilir,
- başka hiç kimse düzenleyemez.

Başlangıç kodu yalnızca rolü soruyor; nesne düzeyindeki soruyu
(gönderinin sahibi kim?) unutmuş.

**Beklenen çıktı:**

```
ada True False
alan False False
grace True True
```
