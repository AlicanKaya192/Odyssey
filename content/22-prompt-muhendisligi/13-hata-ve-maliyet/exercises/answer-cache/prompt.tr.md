`cache_run(requests)` isteklerin üzerinden geçsin. Anahtar metnin küçük
harfli ve boşlukları sadeleştirilmiş hâli (`" ".join(text.lower().split())`).
Anahtar önceden görüldüyse isabet sayılsın ve o isteğin
`count_message_tokens(messages_for(text))` token'ı kazanılmış sayılsın;
görülmediyse bir model çağrısı. `[çağrı, isabet, kazanılan token]`
döndürsün.

**Beklenen çıktı:**

```
[2, 2, 60]
[0, 0, 0]
```
