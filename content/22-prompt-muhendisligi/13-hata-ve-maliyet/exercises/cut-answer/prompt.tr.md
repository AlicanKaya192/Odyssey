`ask(reply, max_tokens, tries)` `ChatClient([reply] * tries)` ile
`MESSAGES`'ı göndersin. Cevap `"length"` ile kesilirse `max_tokens`'ı ikiye
katlayıp yeniden istesin, en fazla `tries` çağrı. Ödenen token'ları
toplasın ve `[metin, giren, çıkan]` döndürsün; hiç sığmazsa metin
`None`.

**Beklenen çıktı:**

```
4 True 39 26
20 True 13 15
2 False 26 5
```
