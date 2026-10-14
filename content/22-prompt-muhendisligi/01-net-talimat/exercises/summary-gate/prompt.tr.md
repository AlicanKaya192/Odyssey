`summarize(reviews)` her yorumu ayrı bir çağrıyla özetletsin:
`ChatClient(SCRIPT)` kur; her yorum için `[system, user]` gönder
(`SYSTEM` ve `wrap("review", yorum)`, `max_tokens=40`). Her cevabı hazır
`check(reply.text, RULES)` ile denetle. Döndür: `[kurallardan geçen
cevapların metinleri, her cevabın kaldığı kuralların listesi]`.

**Beklenen çıktı:**

```
1
ok
['max_words']
['must_include']
```
