SQL Enjeksiyonu ve XSS bölümlerini birleştir. `comments_html(rows, author)`
`rows`'u (`[yazar, metin]`) bellekteki bir `comments` tablosuna yazsın,
`author`'un yorumlarını eklenme sırasıyla **parametreli sorguyla**
okusun ve her birini `"<li>" + kodlanmış metin + "</li>"` olarak bir
liste döndürsün.

**Beklenen çıktı:**

```
ada
  <li>&lt;i&gt;hi&lt;/i&gt;</li>
  <li>second</li>
o'brien
  <li>x &lt; y</li>
zeynep
```
