- `strip_tags(text)`: HTML etiketlerini (`<...>`) boşlukla değiştirsin,
  fazla boşlukları teke indirsin ve **küçük harfe** çevirsin. Fonksiyonu
  `preprocessor` olarak verince vektörleştirici küçük harf yapmaz; o iş senin.
- `vocab_has(word, preprocessor)`: kirli yorumlarda
  `TfidfVectorizer(preprocessor=preprocessor)` kursun ve `word` dağarcıkta
  mı döndürsün.

**Beklenen çıktı:**

```
good value works
True
False
```
