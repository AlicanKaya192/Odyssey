`rules` sözlüğü kullanıcı adından izinli işlemlerin listesine gidiyor.
`is_allowed(rules, user, action)` kullanıcının o işleme izni varsa `True`
döndürmeli.

Başlangıç kodu çalışıyor gibi görünüyor ama listede **hiç olmayan** bir
kullanıcıya her şeye izin veriyor. Varsayılan olarak reddedecek şekilde
düzelt.

**Beklenen çıktı:**

```
True
False
False
```
