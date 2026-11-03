## HTML encoding table

| Character | Encoded form |
|---|---|
| `&` | `&amp;` (first) |
| `<` | `&lt;` |
| `>` | `&gt;` |
| `"` | `&quot;` |
| `'` | `&#x27;` |

Python: `html.escape(text)` encodes all five (`quote=True` is the
default).

## By context

| Where does it go? | What is done |
|---|---|
| HTML body | `html.escape` |
| Attribute value | `html.escape`, the value always in quotes |
| Link (`href`, `src`) | Scheme allow list (`http`, `https`) + `html.escape` |
| Inside a `<script>` block | User data is not written |
| Address parameter | `urllib.parse.quote` (URL encoding) |

## Layers of defence

1. **Output encoding** (context-aware): the main defence.
2. **Templates that encode automatically:** prevent forgetting; "raw/safe"
   markers with care.
3. **CSP:** `script-src 'self'`; no `'unsafe-inline'`.
4. **`HttpOnly` cookie:** a leaked script cannot read the cookie.
5. **Input validation:** the expected type and form.

## Kinds of XSS

| Kind | Where does the text come from? |
|---|---|
| Stored | The database (comment, profile) |
| Reflected | The same request (search box, parameter) |
| DOM-based | The page's own JavaScript |

## Rules

- Encoding is done **when writing** the data, not when storing it: the same
  data goes into HTML, JSON or an e-mail with different encodings.
- If formatted text is needed, do not write your own filter; use a
  maintained sanitising library with an allow list.
- Do not assume a value is "already clean"; let the template encode it.
