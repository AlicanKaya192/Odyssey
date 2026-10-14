`build_messages(question, texts)` iki mesaj döndürsün: önce
`{"role": "system", "content": SYSTEM}`, sonra kullanıcı mesajı. Kullanıcı
mesajının içeriği: `"Sources:"` satırı, her parça için `"[n] metin"` satırı
(`n` 1'den başlar), bir boş satır ve `"Question: soru"`. Satırlar `\n` ile
birleşir.

**Beklenen çıktı:**

```
Sources:
[1] Gift cards are valid for 3 years.
[2] Points expire.

Question: Do gift cards expire?
```
