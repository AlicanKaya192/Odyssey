`sessions` kimlik → kullanıcı sözlüğü. `rotate(sessions, old_id,
new_id)` **yeni** bir sözlük döndürsün: eski kimlik silinmiş, kullanıcısı
yeni kimliğe taşınmış olsun. `old_id` sözlükte yoksa sözlüğün değişmemiş
bir kopyasını döndürsün. Verilen sözlüğü değiştirme. Başlangıç kodu
eski kimliği bırakıyor.

**Beklenen çıktı:**

```
[('new456', 'ada'), ('x9', 'bob')]
True
```
