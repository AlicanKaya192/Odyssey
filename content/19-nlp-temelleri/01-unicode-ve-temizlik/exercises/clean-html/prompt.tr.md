`clean_html(text)` üç şey yapsın: `html.unescape` ile HTML varlıklarını
çözsün, `re.sub(r"<[^>]+>", " ", text)` ile etiketleri boşluğa çevirsin ve
sonunda boşlukları teke indirsin (`" ".join(text.split())`).

**Beklenen çıktı:**

```
Great & cheap
Fast delivery, well packed
5 < 7
```
