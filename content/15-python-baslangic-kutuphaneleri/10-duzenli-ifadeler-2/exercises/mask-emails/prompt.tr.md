`mask_emails(text)` fonksiyonunu yaz: metindeki her e-posta adresinin
`@` öncesini `***` yapsın, alan adını korusun:
`ada.l@example.com` → `***@example.com`. `re.sub` ve yeni metinde `\1`
kullan; adres kalıbı `[\w.]+@([\w.]+)`.

**Beklenen çıktı:**

```
Mail ***@example.com or ***@test.org now
```
