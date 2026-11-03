`html.escape` kullanmadan `escape_html(text)` yaz: `&` → `&amp;`,
`<` → `&lt;`, `>` → `&gt;`, `"` → `&quot;`, `'` → `&#x27;`. Başlangıç
kodu doğru karakterleri çeviriyor ama `&`'yi **en son** çevirdiği için az
önce ürettiği `&lt;` gibi karşılıkları bozuyor.

**Beklenen çıktı:**

```
a &lt; b &amp; c
say &quot;hi&quot; or &#x27;bye&#x27;
&amp;lt;
```
