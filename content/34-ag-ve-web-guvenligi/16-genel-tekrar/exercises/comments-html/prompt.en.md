Combine the SQL Injection and XSS sections. `comments_html(rows, author)`
should write `rows` (`[author, text]`) to an in-memory `comments` table,
read `author`'s comments in insertion order **with a parameterised
query**, and return each as `"<li>" + encoded text + "</li>"` in a
list.

**Expected output:**

```
ada
  <li>&lt;i&gt;hi&lt;/i&gt;</li>
  <li>second</li>
o'brien
  <li>x &lt; y</li>
zeynep
```
