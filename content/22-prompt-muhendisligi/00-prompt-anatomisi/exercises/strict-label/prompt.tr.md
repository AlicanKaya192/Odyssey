`parse_label(text, labels)` modelin cevabını katı ayrıştırsın: baştaki ve
sondaki boşlukları at, küçük harfe çevir, sondaki `.` ve `!`
işaretlerini at. Sonuç `labels` listesindeyse onu, değilse
`"needs_review"` döndür. Metnin içinde kategori adı arama.

**Beklenen çıktı:**

```
'Refunds.' refunds
' payment\n' payment
'Returns?' needs_review
'It is shipping.' needs_review
```
