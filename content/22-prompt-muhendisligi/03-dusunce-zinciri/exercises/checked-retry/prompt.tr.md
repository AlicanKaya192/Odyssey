`ask_checked(script, max_tries)` `ChatClient(script)` ile `MESSAGES`'ı
en fazla `max_tries` kez sorsun (`max_tokens=120`, `temperature=0.7`).
Her cevabın son satırını hazır `final_answer` ile ayrıştır ve hazır
`order_total(ITEMS, 0.10)` ile karşılaştır. Eşitse
`[tutar, kaçıncı denemede]` döndür; hiçbiri tutmazsa
`[None, max_tries]`.

**Beklenen çıktı:**

```
[193.41, 3]
[None, 2]
```
