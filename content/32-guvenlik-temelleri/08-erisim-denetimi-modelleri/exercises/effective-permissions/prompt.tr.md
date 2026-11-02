Rol hiyerarşisi: `parents` sözlüğü bir rolün **miras aldığı** rolleri
söylüyor. `{"admin": ["editor"], "editor": ["viewer"]}` ise `admin`,
`editor`'ün; `editor` de `viewer`'ın bütün izinlerini alır.

`effective_permissions(role, role_perms, parents)` rolün kendi izinleriyle
miras aldığı **bütün** rollerin izinlerini, tekrarsız ve abece sırasında
döndürsün. Miras birkaç kat sürebilir. Bir döngü olursa (`a` → `b` → `a`)
sonsuza gitmemek için ziyaret edilen rolleri bir kümede tut.

**Beklenen çıktı:**

```
viewer read
editor read, write
admin delete, manage, read, write
```
