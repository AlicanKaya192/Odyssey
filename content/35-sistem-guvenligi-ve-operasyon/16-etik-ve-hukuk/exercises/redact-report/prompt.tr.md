`redact(text)` metindeki her e-posta adresini `PATTERN` ile bulup
`"a***@example.org"` biçimine çevirsin; alan adı (`@`'den sonrası)
korunsun ki rapor hangi sistemin etkilendiğini hâlâ söylesin. `re.sub`'a
metin yerine bir fonksiyon verilebilir: eşleşmeyi alıp yerine konacak
metni döndürür.

**Beklenen çıktı:**

```
Owner: a***@example.org
Seen: b***@example.org, x***@y.org
No address here.
```
