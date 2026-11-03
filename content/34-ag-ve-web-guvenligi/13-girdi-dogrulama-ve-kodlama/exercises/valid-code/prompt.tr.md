Ürün kodu iki büyük harf, tire ve dört rakamdır (`AB-1234`).
`valid_code(code)` kodun tamamı bu biçimdeyse `True` döndürsün. Başlangıç
kodu `re.match` ve `^...$` kullanıyor; sonunda satır sonu olan kodu kabul
ediyor.

**Beklenen çıktı:**

```
'AB-1234' True
'ab-1234' False
'AB-1234\n' False
'AB-12345' False
```
