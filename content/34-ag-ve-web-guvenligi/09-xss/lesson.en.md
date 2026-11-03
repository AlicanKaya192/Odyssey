# XSS: Cross-Site Scripting

In the SQL Injection section the user's data was interpreted as code **in
the database**. In XSS (cross-site scripting) the same mistake happens **in
the browser**: user text that the site puts on a page is interpreted as
HTML or JavaScript and runs in another user's browser with that site's
authority. This section shows how the hole arises in a small toy example,
then builds its defences in turn: context-aware output encoding, templates
that encode automatically, safe links and a content security policy (CSP).
In the examples HTML is produced only as Python text; no browser is opened.

## The problem: text turns into HTML

A blog writes comments onto the page as they are:

```python
comment = "Nice post! <b>bold</b> <script>showPopup()</script>"
page = f"<p>{comment}</p>"
print(page)
```

```text
<p>Nice post! <b>bold</b> <script>showPopup()</script></p>
```

When the browser opens this page it draws the `<b>` tag as bold text and
**runs** what is inside the `<script>` tag. The `showPopup()` here is an
imaginary function; but a real script written in the same place runs in
the browser of everyone who opens the page as if it were part of that
site: it can read the page's content, send requests in the user's name and
reach cookies that are not `HttpOnly` (the Sessions and Cookies section).
The user who wrote the comment has run code for **other** users who read
the page.

## Three kinds

<figure class="fig anat">
  <div class="anat-row"><span><b>Stored</b></span><span>The bad text is saved in the database (a comment, a profile name) and served to everyone who opens the page. The kind with the widest effect.</span></div>
  <div class="anat-row"><span><b>Reflected</b></span><span>The text comes from the request (a search box, an address parameter) and is written back onto the page in the same response. The victim has to click a prepared link.</span></div>
  <div class="anat-row"><span><b>DOM-based</b></span><span>The server is not involved at all; the page's own JavaScript writes text it took from the address or another source onto the page as HTML.</span></div>
  <figcaption>All three have the same root cause: untrusted text enters HTML or a script without encoding.</figcaption>
</figure>

## The first defence: output encoding

The solution is to turn the characters that mean something to HTML into
**harmless equivalents** when writing the text onto the page: `&lt;` for
`<`, `&gt;` for `>`, `&amp;` for `&`, `&quot;` and `&#x27;` for quotes.
The browser still shows them on screen as `<` and `>` but does not read
them as tags. In Python `html.escape` does this:

```python
import html

comment = "Nice post! <b>bold</b> <script>showPopup()</script>"
print(f"<p>{html.escape(comment)}</p>")
print(html.escape('He said "hi" & left'))
```

```text
<p>Nice post! &lt;b&gt;bold&lt;/b&gt; &lt;script&gt;showPopup()&lt;/script&gt;</p>
He said &quot;hi&quot; &amp; left
```

The comment now appears on the page as it was written; none of its tags
work. Note that `&` was converted too: otherwise the text of someone who
typed `&lt;` would come out on screen as `<`.

This is the HTML equivalent of the injection rule from the OWASP Top 10
section: a **parameter** in SQL, **output encoding** in HTML. In both, data
is marked according to the rules of the language it goes into and cannot
become code.

## Context matters

The right encoding depends on **where** on the page the text goes. The same
value needs different handling in different places:

<figure class="fig anat">
  <div class="anat-row"><span>HTML body</span><span>Inside <code>&lt;p&gt;...&lt;/p&gt;</code>: HTML encoding (<code>html.escape</code>).</span></div>
  <div class="anat-row"><span>Attribute value</span><span>Inside <code>title="..."</code>: quotes are encoded too, and the value is always written in quotes.</span></div>
  <div class="anat-row"><span>Link address</span><span>Inside <code>href="..."</code>: besides HTML encoding the <b>scheme</b> is checked; only <code>http</code> and <code>https</code>.</span></div>
  <div class="anat-row"><span>Inside a script</span><span>User data is not written inside a <code>&lt;script&gt;</code> block; if needed, the data is read from elsewhere (e.g. an attribute).</span></div>
  <figcaption>A single "escape" function does not protect every context; context-aware encoding is needed.</figcaption>
</figure>

The link address is the most often overlooked context. HTML encoding
neutralises quotes but does not touch the address's **scheme**; an address
starting with `javascript:` runs a script when clicked. That is why the
address is split with a parser and its scheme checked against an allow
list (`urlsplit` from the HTTP and HTTPS section):

```python
import html
from urllib.parse import urlsplit


def safe_link(url, label):
    if urlsplit(url).scheme not in ("http", "https"):
        return html.escape(label)
    return f'<a href="{html.escape(url)}">{html.escape(label)}</a>'


print(safe_link("https://example.com/a?x=1&y=2", "docs"))
print(safe_link("javascript:showPopup()", "click"))
print(safe_link('https://example.com/" title="x', "quote"))
```

```text
<a href="https://example.com/a?x=1&amp;y=2">docs</a>
click
<a href="https://example.com/&quot; title=&quot;x">quote</a>
```

The first address became a valid link (`&` was encoded). The second's
scheme is not in the allow list, so no link was made at all, only the text
remained. In the third, the quote was encoded, so it could not break out of
the `href` value and open a new attribute.

## The second defence: templates that encode automatically

Calling `html.escape` by hand leaves a hole the **one time** it is
forgotten. That is why real applications produce HTML with template
engines that encode values **by default**. Let us show the idea with a
small function:

```python
import html
from string import Template


def render(template, **values):
    safe = {k: html.escape(str(v)) for k, v in values.items()}
    return Template(template).substitute(safe)


print(render("<p>Hello, $name!</p>", name="<i>Ada</i>"))
```

```text
<p>Hello, &lt;i&gt;Ada&lt;/i&gt;!</p>
```

Every value entering the template was encoded; the developer did not have
to remember. In template engines, the markers that **switch encoding off**
(marking a value as "safe" or "raw") are used with care; most XSS holes
come from these doors being opened in the wrong place. If the user needs
to write formatted text (bold, links), instead of writing your own regular
expression you use a maintained sanitising library that limits the allowed
tags with a list.

## The third defence: a content security policy (CSP)

What if a place was missed in encoding? **CSP** (Content Security Policy)
is a response header that tells the browser **which scripts may run** on
the page. For example, only scripts from the site's own files are allowed,
and scripts embedded in the page do not run:

```python
def parse_csp(header):
    policy = {}
    for part in header.split(";"):
        words = part.split()
        if words:
            policy[words[0].lower()] = words[1:]
    return policy


csp = parse_csp("default-src 'self'; script-src 'self'; object-src 'none'")
print(csp["script-src"])
print("'unsafe-inline'" in csp["script-src"])
```

```text
["'self'"]
False
```

`script-src 'self'` allows only script files loaded from the same site; a
`<script>...</script>` block that has somehow leaked into the page does
not run. If `'unsafe-inline'` is added this protection goes away; its name
says so. CSP is not **instead of** encoding but a **second layer** against
a missed mistake (the CORS and Security Headers section).

## Limiting the damage

- The session cookie is **`HttpOnly`**: a leaked script cannot read the
  cookie (it can still send requests in the user's name; that is why the
  real solution is encoding).
- **Input validation:** the age field is a number, the user name only
  certain characters (the Input Validation section). A layer next to
  encoding.
- For important operations (changing the password) the password is asked
  again; a leaked script cannot do this on its own.

## Summary

- **XSS:** untrusted text written onto the page without encoding runs as
  code in the browser; it affects other users who open the page.
- Kinds: **stored**, **reflected**, **DOM-based**; the root cause is the
  same.
- The first defence is **output encoding**: `html.escape` turns the
  characters `< > & " '` into harmless equivalents.
- Encoding is chosen **by context**; in a link address the scheme is
  checked too (only `http`, `https`).
- **Templates that encode automatically** prevent forgetting; markers that
  switch encoding off are used with care.
- **CSP** stops embedded scripts; `'unsafe-inline'` removes the protection.
- `HttpOnly` cookies and input validation limit the damage; they do not
  replace encoding.
