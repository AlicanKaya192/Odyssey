Dosya bir sözlük: `owner`, `group`, `mode`. `has_access(file, user,
groups, action)` (`action`: `"r"`, `"w"` ya da `"x"`) erişime izin olup
olmadığını döndürsün. **Tek sınıf** seç: kullanıcı sahipse sahip bitleri,
değilse ve dosyanın grubu `groups` içindeyse grup bitleri, yoksa
diğerleri. Başlangıç kodu üç sınıfın herhangi birinde izin görünce
`True` diyor; bu yanlış.

**Beklenen çıktı:**

```
False
True
True
False
False
```
