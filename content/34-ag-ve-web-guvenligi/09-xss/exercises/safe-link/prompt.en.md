`safe_link(url, label)` should return `<a href="URL">LABEL</a>` if the
address's scheme is `http` or `https` (both encoded with `html.escape`);
otherwise it should make no link and return only the encoded label. For
the scheme, `urlsplit(url).scheme`.

**Expected output:**

```
<a href="https://a.example/">docs</a>
&lt;b&gt;click&lt;/b&gt;
<a href="http://a.example/?p=1&amp;q">x</a>
```
