`aspect_labels(text, aspects)` metni `re.findall(r"[^.!?]+", text.lower())`
ile cümlelere bölsün. İçinde bir özellik adı geçen her cümlenin
`negated(sentence, 3)` puanını o özelliğe eklesin. Sonunda **geçen**
özellikler için sözlük döndürsün: toplam > 0 `"positive"`, < 0
`"negative"`, 0 `"neutral"`. `negated` hazır.

**Beklenen çıktı:**

```
{'strap': 'positive', 'screen': 'negative'}
```
