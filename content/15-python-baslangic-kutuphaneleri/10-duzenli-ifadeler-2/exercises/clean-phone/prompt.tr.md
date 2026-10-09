`clean_phone(text)` fonksiyonunu yaz: rakam olmayan her şeyi silsin
(`re.sub(r"\D", "", text)`); kalan metin `0` ile başlayan **11 rakam**sa onu
döndürsün, değilse `None`. Böylece `"0532 123 45 67"` ve `"(0532) 123-4567"`
aynı numaraya iner.

**Beklenen çıktı:**

```
05321234567
05321234567
None
05321234567
```
