# Input Validation and Output Encoding

The SQL Injection and XSS sections showed two faces of the same mistake:
data was interpreted as code where it went. In both sections the main
defence was **on the way out** (parameters, output encoding), and input
validation came up as "a layer next to it". This section takes that layer
on its own: how input is validated, what traps there are (misused regular
expressions, different texts that look the same, file paths, the command
line) and how validation and encoding work together.

<figure class="fig"><div class="versus">
  <div><h4>Input validation</h4>When data <b>comes in</b>: is it of the expected type, length, range and form? If not, it is refused. It checks the data's <b>meaning</b>.</div>
  <div><h4>Output encoding</h4>When data <b>is written somewhere</b>: it is marked according to that place's rules (HTML, SQL, URL, command). It stops the data <b>becoming code</b>.</div>
</div><figcaption>Neither replaces the other: a valid name too (<code>O'Brien</code>) can break SQL.</figcaption></figure>

## Validating with an allow list

The most solid form of validation is an **allow list**: describe what is
valid and refuse the rest. A block list that counts "dangerous characters"
always forgets something (deny by default from the Security Principles
section).

```python
import re

COUNTRIES = {"TR", "DE", "US"}


def validate(form):
    errors = []
    if not re.fullmatch(r"[a-z0-9_]{3,20}", form.get("username", "")):
        errors.append("username")
    age = form.get("age", "")
    if not re.fullmatch(r"[0-9]{1,3}", age) or not 13 <= int(age) <= 120:
        errors.append("age")
    if form.get("country") not in COUNTRIES:
        errors.append("country")
    return errors


print(validate({"username": "ada_1", "age": "34", "country": "TR"}))
print(validate({"username": "Ada!", "age": "-5", "country": "XX"}))
print(validate({"username": "ada", "age": "999"}))
```

```text
[]
['username', 'age', 'country']
['age', 'country']
```

Three questions were asked for each field: **type** (is it a number),
**form** (only allowed characters, of a given length) and **range or set**
(between 13 and 120, one of the known countries). A missing field counted
as an error too. Validation is done **on the server**; validation in the
browser is only quick feedback for the user, because a request can be
written without a browser (the HTTP and HTTPS section).

## The regular expression trap: match and fullmatch

In a format check, the regular expression must fit the **whole** text.
`re.match` looks only at the start; and the `$` sign tolerates a trailing
newline:

```python
import re

for name in ["ada", "ada\n", "ada; x"]:
    loose = bool(re.match(r"^[a-z0-9_]{3,20}$", name))
    strict = bool(re.fullmatch(r"[a-z0-9_]{3,20}", name))
    print(f"{name!r:<10} match={loose!s:<5} fullmatch={strict}")
```

```text
'ada'      match=True  fullmatch=True
'ada\n'    match=True  fullmatch=False
'ada; x'   match=False fullmatch=False
```

The pattern written with `^...$`, which looks "right", accepted the name
with a newline at the end. `re.fullmatch` requires the whole text and
refused it. In validation `fullmatch` is used. Another trap in regular
expressions is that nested repeating patterns (such as `(a+)+`) can run for
a very long time on some inputs; this can turn into a denial-of-service
hole. Patterns are kept simple and input length limited.

## Canonical form first

Two texts that look the same can be different to a computer: letter case,
a trailing space, or forms written with other characters such as Unicode's
"full-width" letters. If the name `admin` is forbidden but the comparison
is made on the raw text, another spelling that looks the same slips in.
That is why text is first turned into a **canonical** (single, standard)
form, then validated and compared:

```python
import unicodedata

for name in ["admin", "Admin", "ａｄｍｉｎ", "admin "]:
    canon = unicodedata.normalize("NFKC", name).strip().casefold()
    print(f"{name!r:<9} -> {canon!r:<8} {canon == 'admin'}")
```

```text
'admin'   -> 'admin'  True
'Admin'   -> 'admin'  True
'ａｄｍｉｎ'   -> 'admin'  True
'admin '  -> 'admin'  True
```

All four spellings came down to the same canonical form. `NFKC` turns
Unicode's "compatibility" characters into their ordinary equivalents, and
`casefold` removes letter case (it does not know language-specific cases
such as the Turkish `İ`/`ı`; those are considered separately). The order
matters: **canonical form first, then validation**; done the other way, the
validated text and the used text differ.

## File paths

When a file name given by the user is added to a folder, `..` (the parent
folder) or an absolute path can take the result **outside** the folder.
This is called **path traversal**. Defence: join the path, **normalise**
it, and check that the result is still inside the allowed folder:

```python
import posixpath

BASE = "/srv/app/uploads"


def safe_path(name):
    full = posixpath.normpath(posixpath.join(BASE, name))
    return full if full.startswith(BASE + "/") else None


for name in ["cat.png", "2026/cat.png", "../settings.ini", "/srv/app/settings.ini"]:
    print(f"{name:<22} {safe_path(name)}")
```

```text
cat.png                /srv/app/uploads/cat.png
2026/cat.png           /srv/app/uploads/2026/cat.png
../settings.ini        None
/srv/app/settings.ini  None
```

The file in a subfolder was allowed; the names going up to the parent
folder or giving an absolute path were refused. The `BASE + "/"` in the
check matters: merely starting with `BASE` would also accept a
neighbouring folder such as `/srv/app/uploads-old`. Better still is not to
use the user's file name at all: the file is stored under a random name,
and the name the user gave is kept only as a label in the database.

## One value, many encodings

Even a value that passed validation cannot be written the same way
everywhere. The same text encoded for three different contexts:

```python
import html
import json
from urllib.parse import quote

value = 'Tom & "Jerry" <3'
print(html.escape(value))
print(quote(value, safe=""))
print(json.dumps(value))
```

```text
Tom &amp; &quot;Jerry&quot; &lt;3
Tom%20%26%20%22Jerry%22%20%3C3
"Tom & \"Jerry\" <3"
```

`&amp;` and `&lt;` in HTML, `%26` and `%3C` in an address parameter,
escaped quotes in JSON. Each context has its own encoder, and encoding is
done when the data **is written** into that context (the rule from the XSS
section).

## The command line

Adding a value given by the user to a **shell command** as text is the
command-line equivalent of SQL injection. In a shell, characters such as
`;` start a new command. No command runs below; it only shows how the
shell would split the text into parts:

```python
import shlex

name = "report.txt; echo hi"
print(shlex.split("wc -l " + name))
print(["wc", "-l", name])
print("wc -l " + shlex.quote(name))
```

```text
['wc', '-l', 'report.txt;', 'echo', 'hi']
['wc', '-l', 'report.txt; echo hi']
wc -l 'report.txt; echo hi'
```

In the command joined as text, `;` became a separate part and a second
command (`echo hi`) followed. In the argument **list** form, the name
stayed a single argument; if the program is run without a shell, this
value never becomes a command. The rule is the same as in SQL: a command is
not built from text, arguments are given separately; if a shell is really
needed, every value is escaped with `shlex.quote`. Best of all, where
possible, use a library function that does the same job instead of running
an external command.

## Summary

- **Input validation** checks meaning, **output encoding** stops data
  becoming code; neither replaces the other.
- Validation is done with an **allow list** and **on the server**: type,
  form, length, range or set; a missing field is an error too.
- Use **`re.fullmatch`** in regular expressions; `re.match` and `$` miss a
  trailing newline. Keep patterns simple and input length limited.
- Text is first turned into **canonical form** (NFKC, `strip`,
  `casefold`), then validated.
- A **file path** is normalised and checked to be inside the allowed
  folder; better still, do not make the user's name the file name.
- Each context has its own **encoder**: HTML, URL, JSON.
- A **command** is not built from text; an argument list, `shlex.quote` if
  needed.
