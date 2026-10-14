`guarded(script, message)` üç katmanı birleştirsin. Mesaj hazır `DETECT`
kalıbına uyuyorsa model hiç çağrılmadan `["blocked input", ""]`. Yoksa
`ChatClient(script)` ile `[system, user]` gönder (`SYSTEM`,
`max_tokens=80`). Cevapta `CANARY` varsa `["blocked output", "leak"]`;
`LINK`'in bulduğu bir alan adı `ALLOWED`'da değilse
`["blocked output", alan adı]`; yoksa `["sent", cevap]`.

**Beklenen çıktı:**

```
['sent', 'It ships today.']
['blocked input', '']
['blocked output', 'evil.example']
['blocked output', 'leak']
```
