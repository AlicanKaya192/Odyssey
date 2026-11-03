`safe_link(url, label)` adresin şeması `http` ya da `https` ise
`<a href="URL">LABEL</a>` döndürsün (ikisi de `html.escape` ile
kodlanmış); değilse bağlantı üretmesin, yalnızca kodlanmış etiketi
döndürsün. Şema için `urlsplit(url).scheme`.

**Beklenen çıktı:**

```
<a href="https://a.example/">docs</a>
&lt;b&gt;click&lt;/b&gt;
<a href="http://a.example/?p=1&amp;q">x</a>
```
