Arama sayfası, aranan kelimeyi sonuçta `<mark>...</mark>` ile
vurguluyor. `highlight(text, word)` önce metni **ve** kelimeyi
`html.escape` ile kodlasın, sonra kodlanmış metindeki kodlanmış kelimeyi
`<mark>KELIME</mark>` ile değiştirsin. Kelime boşsa yalnızca kodlanmış
metni döndürsün. Başlangıç kodu hiç kodlamıyor (yansıtılan XSS).

**Beklenen çıktı:**

```
x&lt;<mark>y</mark>
<mark>te</mark>a &amp; <mark>te</mark>e
a<mark>&lt;</mark>b
```
