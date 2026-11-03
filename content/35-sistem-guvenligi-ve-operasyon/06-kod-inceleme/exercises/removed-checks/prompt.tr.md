`removed_checks(diff, keywords)` bir farktaki **silinen** satırlardan
(`-` ile başlayan ama `---` ile başlamayan) içinde `keywords`'ten biri
geçenleri döndürsün: baştaki `-` atılmış ve `strip()` edilmiş olarak,
farktaki sırayla. Başlangıç kodu eklenen satırlara bakıyor.

**Beklenen çıktı:**

```
check_owner(user, data)
verify_token(user)
```
