`encode_for(context, value)` should encode the value by context:
`"html"` → `html.escape`; `"url"` → `quote(value, safe="")`; `"json"` →
`json.dumps`. For an unknown context it should return `None`: for SQL a
parameter is used, not encoding.

**Expected output:**

```
html a&amp;b &quot;c&quot; &lt;d&gt;
url a%26b%20%22c%22%20%3Cd%3E
json "a&b \"c\" <d>"
sql None
```
