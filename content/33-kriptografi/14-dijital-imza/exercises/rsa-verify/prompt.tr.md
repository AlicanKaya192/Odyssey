`digest` hazır. `verify(message, signature, e, n)` imza doğruysa `True`
döndürsün: `pow(signature, e, n)` mesajın özetine eşit olmalı. Başlangıç
kodu imzayı doğrudan özetle karşılaştırıyor; açık üssü hiç
kullanmıyor.

**Beklenen çıktı:**

```
True
False
```
