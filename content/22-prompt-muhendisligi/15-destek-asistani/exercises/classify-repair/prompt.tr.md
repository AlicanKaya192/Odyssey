`classify_with_repair(script, message)` `ChatClient(script)` ile
`[system (CLASSIFY), user]` göndersin (`max_tokens=20`). Cevap hazır
`parse_label` ile ayrıştırılamazsa mesajlara modelin cevabını ve
`"Only the category word, please."` kullanıcı mesajını ekleyip bir kez daha
sorsun. `[kategori ya da None, çağrı sayısı]` döndürsün.

**Beklenen çıktı:**

```
['payment', 1]
['payment', 2]
[None, 2]
```
