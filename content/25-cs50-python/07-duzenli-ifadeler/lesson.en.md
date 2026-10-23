# Regular Expressions

Week 7 of CS50 Python. You can watch the lecture in the **Video** tab; this
page is its written form. A **regular expression** (regex for short) is a
**pattern**. In programming it is very common to compare data, very often
the user's input, against a pattern: does what was typed really look like
an email address? This week we will use patterns for three jobs:
**validating** data, **cleaning** it up and **extracting** information from
it.

## Validating without patterns

Let's validate an email address. The loosest rule: if it contains an `@`,
call it valid. `validate.py`:

```python
email = input("What's your email? ").strip()

if "@" in email:
    print("Valid")
else:
    print("Invalid")
```

```text
$ python validate.py
What's your email? malan@harvard.edu
Valid
```

`"@" in email` looks for an `@` anywhere in the string. The problem: someone
who types only `@` passes too.

```text
$ python validate.py
What's your email? @
Valid
```

Let's be a little stricter: split the address in two at the `@` (`split`)
and require a username on the left and a domain ending in `.edu` on the
right:

```python
email = input("What's your email? ").strip()

username, domain = email.split("@")

if username and domain.endswith(".edu"):
    print("Valid")
else:
    print("Invalid")
```

```text
$ python validate.py
What's your email? malan@harvard.edu
Valid
```

`if username` is true when the string is not empty. But this can be fooled
too:

```text
$ python validate.py
What's your email? malan@.edu
Valid
```

`malan@.edu` has no domain name. Adding one more condition for every new gap
quickly gets out of hand. Python has the **`re`** library for this job.

## re.search

`re.search(pattern, string)` searches for the pattern in the string; if it
finds it, it returns a match object (which counts as true), otherwise
`None`. The simplest pattern is literal text:

```python
import re

email = input("What's your email? ").strip()

if re.search("@", email):
    print("Valid")
else:
    print("Invalid")
```

That is no different from `"@" in email`. The power comes from the special
symbols inside a pattern:

| Symbol | Meaning |
|---|---|
| `.` | any character except a newline |
| `*` | zero or more of the thing on its left |
| `+` | one or more of the thing on its left |
| `?` | zero or one of the thing on its left (optional) |
| `{m}` | exactly `m` of the thing on its left |
| `{m,n}` | between `m` and `n` of the thing on its left |

The pattern "something on the left, `@`, something on the right" is
`.+@.+`:

```python
import re

email = input("What's your email? ").strip()

if re.search(".+@.+", email):
    print("Valid")
else:
    print("Invalid")
```

```text
$ python validate.py
What's your email? malan@
Invalid
```

Had we written `.*@.*` first, `malan@` would pass: `*` means "zero or more",
so nothing after the `@` is fine too. With `.+` at least one character is
required. (`..*` does the same job: one dot, then zero or more.)

`re.search` reads the pattern from left to right and works like a **finite
state machine**: from the start state, it tries to move to the next state
with each character; if it is in an accepting state at the end of the
input, the pattern has matched.

## Escaping and raw strings

Let's add `.edu` at the end: `.+@.+.edu`. But this period also means "any
character":

```text
$ python validate.py
What's your email? malan@harvard?edu
Valid
```

For a literal period we put a **backslash** in front of it: `\.`. A
backslash is special in a Python string too (`\n` is a newline); so that
Python leaves it alone, we make the pattern a **raw string**: an `r` at the
start.

```python
import re

email = input("What's your email? ").strip()

if re.search(r".+@.+\.edu", email):
    print("Valid")
else:
    print("Invalid")
```

```text
$ python validate.py
What's your email? malan@harvard?edu
Invalid
```

Writing `r"..."` for patterns even when there is no backslash is a good
habit: you will not forget it when you add a `\` later.

## Start to end: ^ and $

This pattern also accepts an address inside a sentence:

```text
$ python validate.py
What's your email? My email address is malan@harvard.edu.
Valid
```

`^` means matching at the **start** of the string, `$` at its **end**.
Together they say "the whole string must be this pattern":

```python
import re

email = input("What's your email? ").strip()

if re.search(r"^.+@.+\.edu$", email):
    print("Valid")
else:
    print("Invalid")
```

```text
$ python validate.py
What's your email? My email address is malan@harvard.edu.
Invalid
```

## Character sets

`.` is still too generous: `@` is a character too, so
`malan@@@harvard.edu` passes. **Square brackets** define a set of
characters: `[abc]` is one of those three, `[a-z]` a range, and `[^@]` any
character **except** `@` (a `^` inside square brackets means "not"):

```python
import re

email = input("What's your email? ").strip()

if re.search(r"^[^@]+@[^@]+\.edu$", email):
    print("Valid")
else:
    print("Invalid")
```

```text
$ python validate.py
What's your email? malan@@@harvard.edu
Invalid
```

To limit the username to letters, digits and the underscore:
`[a-zA-Z0-9_]`. This set is so common that it has a shorthand: `\w`, "word
character". Some of the ready-made sets:

| Symbol | Meaning |
|---|---|
| `\d` | a digit (`0`–`9`) |
| `\D` | not a digit |
| `\s` | a whitespace character (space, tab...) |
| `\S` | not whitespace |
| `\w` | a word character: letter, digit, `_` |
| `\W` | not a word character |

```python
import re

email = input("What's your email? ").strip()

if re.search(r"^\w+@\w+\.edu$", email):
    print("Valid")
else:
    print("Invalid")
```

```text
$ python validate.py
What's your email? MALAN@HARVARD.EDU
Invalid
```

## Flags

`MALAN@HARVARD.EDU` fails, because the pattern asks for a lowercase `edu`.
We could lowercase the input with `lower()`; but the third argument of
`re.search` is **flags**: `re.IGNORECASE` ignores case. (`re.MULTILINE` is
for text with several lines, `re.DOTALL` for letting the period match a
newline too.)

```python
import re

email = input("What's your email? ").strip()

if re.search(r"^\w+@\w+\.edu$", email, re.IGNORECASE):
    print("Valid")
else:
    print("Invalid")
```

```text
$ python validate.py
What's your email? MALAN@HARVARD.EDU
Valid
```

## Groups and optional parts

`malan@cs50.harvard.edu` fails: there are two periods in the domain. There
may or may not be a subdomain. **Parentheses** group parts together, and a
`?` after them makes the whole group optional:

```python
import re

email = input("What's your email? ").strip()

if re.search(r"^\w+@(\w+\.)?\w+\.edu$", email, re.IGNORECASE):
    print("Valid")
else:
    print("Invalid")
```

```text
$ python validate.py
What's your email? malan@cs50.harvard.edu
Valid
```

Had we put the `?` only after `\.`, without parentheses, only the period
would be optional. `|` means "or": `(com|edu)` is either one; `(\w|\.)+` is a
letter, digit, underscore or period.

| Syntax | Meaning |
|---|---|
| <code>A&#124;B</code> | A or B |
| `(...)` | a group (and a capture) |
| `(?:...)` | a non-capturing group |

Even with all of this, the official rule for email addresses is much
broader; the pattern browsers use fills the screen. A real program uses a
popular library for this (that is exactly Response Validation in the
problem set). `re.match` matches a pattern from the start of the string and
`re.fullmatch` against the whole string; with them there is no need to
write `^` and `$`.

## Cleaning up: capturing

Users sometimes type their name as `Malan, David`. Let's store them all as
`David Malan`. We start with `split(", ")`, `format.py`:

```python
name = input("What's your name? ").strip()

if "," in name:
    last, first = name.split(", ")
    name = f"{first} {last}"

print(f"hello, {name}")
```

```text
$ python format.py
What's your name? Malan, David
hello, David Malan
```

If the space after the comma is forgotten, the program crashes:

```text
$ python format.py
What's your name? Malan,David
Traceback (most recent call last):
  File "format.py", line 4, in <module>
    last, first = name.split(", ")
    ^^^^^^^^^^^
ValueError: not enough values to unpack (expected 2, got 1)
```

In a regular expression, parentheses have one more job: they **capture**
what is inside them. The match object `re.search` returns gives you what
was captured: `matches.groups()` all of it, `matches.group(1)` the first
(groups are counted from 1; `group(0)` is the whole match). Let's leave the
number of spaces free with ` *`:

```python
import re

name = input("What's your name? ").strip()

matches = re.search(r"^(.+), *(.+)$", name)
if matches:
    name = matches.group(2) + " " + matches.group(1)

print(f"hello, {name}")
```

```text
$ python format.py
What's your name? Malan,David
hello, David Malan
```

### The walrus operator

"Assign, then ask with `if`" is so common that Python lets you write it on
one line: `:=` both assigns and uses the value in the condition. Seen from
the side it looks like a walrus, so it is called the **walrus operator**:

```python
import re

name = input("What's your name? ").strip()

if matches := re.search(r"^(.+), *(.+)$", name):
    name = matches.group(2) + " " + matches.group(1)

print(f"hello, {name}")
```

The output is the same.

## Extracting: re.sub

Let's ask the user for the address of their Twitter profile (now called X)
and extract the username. `twitter.py`:

```python
url = input("URL: ").strip()

username = url.replace("https://twitter.com/", "")
print(f"Username: {username}")
```

```text
$ python twitter.py
URL: https://twitter.com/davidjmalan
Username: davidjmalan
```

But if `http://`, `www.` or an address with no protocol comes in, or the
address is inside a sentence, it breaks. `str.removeprefix` solves the
sentence problem, not the others. `re.sub(pattern, replacement, string)`
does find and replace with a regular expression:

```python
import re

url = input("URL: ").strip()

username = re.sub(r"^(https?://)?(www\.)?twitter\.com/", "", url)
print(f"Username: {username}")
```

```text
$ python twitter.py
URL: http://www.twitter.com/davidjmalan
Username: davidjmalan
```

Each part of the pattern solves one problem: `^` from the start, `s?` for
`http` or `https`, `(www\.)?` an optional `www.`, `(https?://)?` an optional
protocol, and the `\.` in `twitter\.com` a literal period.

### Only if it matches

`re.sub` returns the string unchanged even if the pattern does not match;
`https://google.com/` would be printed as a username. Let's make it
conditional with `re.search`. The parentheses of `(www\.)?` capture too, so
the username would be group 2; a **non-capturing group** `(?:...)` groups
without capturing, and the username stays in group 1. By Twitter's rule a
username is only letters, digits and the underscore:

```python
import re

url = input("URL: ").strip()

if matches := re.search(
    r"^(?:https?://)?(?:www\.)?twitter\.com/([a-z0-9_]+)", url, re.IGNORECASE
):
    print("Username:", matches.group(1))
```

```text
$ python twitter.py
URL: twitter.com/davidjmalan/
Username: davidjmalan
```

```text
$ python twitter.py
URL: https://google.com/
```

Do not try to write a long pattern all at once: start with a small
pattern, see it work, add a piece, try again.

## Summary

Besides these, `re` has `re.split` (splitting by a pattern) and `re.findall`
(every match of a pattern); you will use them in the exercises. Regular
expressions exist with the same syntax in many languages, such as
JavaScript, Java and Ruby.

- `re.search`, `re.match`, `re.fullmatch`; `re.sub`, `re.split`, `re.findall`
- `. * + ? {m} {m,n}`, `^ $`, `[...] [^...]`, `\d \s \w`, `A|B`, `(...)`,
  `(?:...)`
- Raw string `r"..."`, escaping `\.`
- The flag `re.IGNORECASE`
- Groups: `matches.group(1)`; the walrus operator `:=`

---

*This section is translated and adapted from week 7 of Harvard University's [CS50's Introduction to Programming with Python](https://cs50.harvard.edu/python/) (lecture notes and problem set); examples and exercises were changed, and the problem set is checked by Odyssey, not by CS50's check50. The original and this adaptation are licensed under [CC BY-NC-SA 4.0](https://creativecommons.org/licenses/by-nc-sa/4.0/). Harvard does not endorse this adaptation.*
