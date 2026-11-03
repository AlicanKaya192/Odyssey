`safe_path(base, name)` `base` klasörüne `name`'i eklesin
(`posixpath.join`), sonucu `posixpath.normpath` ile normalleştirsin;
sonuç `base + "/"` ile başlıyorsa yolu, başlamıyorsa `None` döndürsün.
Başlangıç kodu normalleştirmeden denetliyor.

**Beklenen çıktı:**

```
cat.png /srv/app/uploads/cat.png
../settings.ini None
a/../../x None
/etc/x None
```
