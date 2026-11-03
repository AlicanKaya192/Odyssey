`encode_for(context, value)` değeri bağlama göre kodlasın: `"html"` →
`html.escape`; `"url"` → `quote(value, safe="")`; `"json"` →
`json.dumps`. Bilinmeyen bağlamda `None` döndürsün: SQL için kodlama
değil parametre kullanılır.

**Beklenen çıktı:**

```
html a&amp;b &quot;c&quot; &lt;d&gt;
url a%26b%20%22c%22%20%3Cd%3E
json "a&b \"c\" <d>"
sql None
```
