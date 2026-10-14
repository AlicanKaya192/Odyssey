`answer(script, question)` `ChatClient(script)` ile `[system, user]`
gönderip (`SYSTEM`, `question`, `max_tokens=80`) cevabı hazır `review` ile
denetlesin. Sorunlarda `"promise"` varsa hemen `[HANDOVER, çağrı
sayısı]` döndür. Sorun yoksa `[cevap metni, çağrı sayısı]`. Yalnızca
uzunluk sorunu varsa cevabı `assistant` ve `SHORTEN`'ı `user` mesajı
olarak ekleyip bir kez daha sor; ikinci cevap da geçmezse
`[HANDOVER, çağrı sayısı]`.

**Beklenen çıktı:**

```
1 It left yesterday.
2 It left today.
1 A colleague will get back to you soon.
```
