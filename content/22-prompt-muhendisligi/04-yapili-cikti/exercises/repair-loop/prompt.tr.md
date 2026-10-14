`ask_json(script, max_tries)` `ChatClient(script)` ile `QUESTION`'ı
sorsun (`max_tokens=60`). Her cevabı hazır `parse_json` ve `validate` ile
denetle. Hata yoksa `[veri, deneme sayısı, son çağrıdaki mesaj sayısı]`
döndür. Hata varsa cevabı `assistant` mesajı, hatalardan kurulan mesajı
(`"Your answer was not valid: "` + `"; "` ile birleşim +
`". Reply with the JSON object only."`) `user` mesajı olarak ekleyip
yeniden sor. `max_tries` deneme dolarsa
`[None, max_tries, son çağrıdaki mesaj sayısı]`.

**Beklenen çıktı:**

```
{'category': 'shipping', 'urgent': True}
3 5
None
2 3
```
