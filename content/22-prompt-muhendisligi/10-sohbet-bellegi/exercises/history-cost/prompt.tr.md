`compare(questions, keep)` sohbeti taklit etsin: her soruyu `user`
mesajı olarak geçmişe ekle; o turda bütün geçmişle (`[SYSTEM] + history`)
ve yalnızca son `keep` mesajla (`[SYSTEM] + history[-keep:]`) giden token
sayısını `count_message_tokens` ile ayrı ayrı topla; sonra `REPLY`'yi
`assistant` mesajı olarak ekle. Döndür: `[bütün geçmiş toplamı, son
mesajlar toplamı]`.

**Beklenen çıktı:**

```
[337, 168]
[337, 337]
```
