`render_comment(author, text)` şu HTML'i döndürsün:
`<p><b>AUTHOR</b>: TEXT</p>`. Yazar adı ve metin kullanıcıdan geliyor;
ikisi de `html.escape` ile kodlanmalı. Başlangıç kodu ikisini de olduğu
gibi yazıyor.

**Beklenen çıktı:**

```
<p><b>ada</b>: 1 &lt; 2 &amp; ok</p>
<p><b>&lt;b&gt;bob&lt;/b&gt;</b>: hi</p>
```
