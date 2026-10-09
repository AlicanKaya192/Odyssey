Ürün kodları iki büyük harf, tire ve dört rakamdan oluşur: `AB-1234`.
`is_product_code(code)` fonksiyonunu yaz: kod tam olarak bu biçimdeyse
`True`, değilse `False` döndürsün. Başlangıç kodu `search` kullanıyor;
`XAB-1234` ona göre de geçerli.

**Beklenen çıktı:**

```
AB-1234 True
ab-1234 False
AB-123 False
XAB-1234 False
```
