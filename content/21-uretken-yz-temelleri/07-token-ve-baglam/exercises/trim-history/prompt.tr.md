`trim(messages, budget)` ilk mesajı (sistem mesajı) her zaman tutsun ve
`count_message_tokens` bütçeyi aşmayana kadar sistem mesajından sonraki
**en eski** mesajı atsın. Döndür: `[kalan mesaj sayısı, kalan token
sayısı]`. Hiç atmadan sığıyorsa listeye dokunma.

**Beklenen çıktı:**

```
[4, 53]
[6, 73]
```
