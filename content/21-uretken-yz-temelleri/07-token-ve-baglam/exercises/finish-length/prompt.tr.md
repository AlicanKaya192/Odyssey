`ask_complete(start)` aynı soruyu `ChatClient([ANSWER] * 5)` ile
`max_tokens=start` sınırıyla sorsun. Cevabın bitiş nedeni `"length"` ise
sınırı iki katına çıkarıp yeniden sorsun; `"stop"` gelince dursun.
Döndür: `[son cevabın metni, son kullanılan max_tokens, toplam çağrı
sayısı]` (çağrı sayısı `len(client.calls)`).

**Beklenen çıktı:**

```
5 20 3 True
40 40 1 True
```
