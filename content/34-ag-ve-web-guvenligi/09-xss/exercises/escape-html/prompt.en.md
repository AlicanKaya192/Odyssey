Write `escape_html(text)` without using `html.escape`: `&` → `&amp;`,
`<` → `&lt;`, `>` → `&gt;`, `"` → `&quot;`, `'` → `&#x27;`. The starter
code converts the right characters, but because it converts `&` **last**
it breaks the equivalents like `&lt;` it has just produced.

**Expected output:**

```
a &lt; b &amp; c
say &quot;hi&quot; or &#x27;bye&#x27;
&amp;lt;
```
