`render_comment(author, text)` should return this HTML:
`<p><b>AUTHOR</b>: TEXT</p>`. The author name and the text come from the
user; both must be encoded with `html.escape`. The starter code writes both
as they are.

**Expected output:**

```
<p><b>ada</b>: 1 &lt; 2 &amp; ok</p>
<p><b>&lt;b&gt;bob&lt;/b&gt;</b>: hi</p>
```
