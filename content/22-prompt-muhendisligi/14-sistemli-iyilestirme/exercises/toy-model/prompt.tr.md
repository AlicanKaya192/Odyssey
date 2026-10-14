`toy_model(prompt, text)` derstekini yazsın: metindeki küçük harfli
kelimeleri (`[a-z]+`) bir kümeye al. Prompt'taki her `- label: w1, w2`
satırı için listelenen kelimelerden kaçının metinde geçtiğini say. En çok
geçen kategoriyi döndür; eşitlikte önce gelen, hiçbiri geçmezse
`"unknown"`.

**Beklenen çıktı:**

```
shipping
returns
unknown
```
