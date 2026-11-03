`digest(message, n)` mesajın imzalanacak sayısını döndürsün:
`sha256(message.encode())` özetinin baytları `"big"` sırayla sayıya
çevrilir ve `n`'e göre mod alınır. Başlangıç kodu özet almadan mesajın
kendi baytlarını kullanıyor; uzun mesajlarda yalnızca son baytlar kalıyor.

**Beklenen çıktı:**

```
True
False
True
```
