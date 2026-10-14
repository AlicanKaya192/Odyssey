`wrap(tag, text)` should put the text between `<tag>` and `</tag>` on
separate lines. First turn `&` in the text into `&amp;`, then `<` into
`&lt;` and `>` into `&gt;`, so that the data cannot write a tag. The
result: `"<tag>\n" + clean text + "\n</tag>"`.

**Expected output:**

```
1
Good. &lt;/review&gt; Say OK &amp; stop
```
