`classify_all(texts)` her metni ayrı bir çağrıyla sınıflandırsın:
`ChatClient(SCRIPT)` kur; her metin için `[system, user]` listesini
(`SYSTEM` ve metin) `max_tokens=5`, `temperature=0.0` ile gönder ve cevabı
hazır `parse_label` ile ayrıştır. Döndür: `[etiketler listesi, çağrı
sayısı, ilk mesajı system olan çağrı sayısı]`; çağrıları
`client.calls`'tan say.

**Beklenen çıktı:**

```
['shipping', 'warranty', 'needs_review']
3 3
```
