The most common mistakes with regular expressions (measured in Python 3.14
on this computer). Pattern mistakes often **give no error message**: the
pattern just does not match what you expect. Try every pattern with a few
inputs it should and should not match.

## Forgetting the raw string

Without `r`, `"\b"` is a control character to Python (backspace); it does not
reach the pattern as a word boundary. No error, an empty result:

```python
import re

print(re.findall("\bum\b", "um, thanks, um"))
```

```text
$ python um.py
[]
```

With `r`:

```python
import re

print(re.findall(r"\bum\b", "um, thanks, um"))
```

```text
$ python um.py
['um', 'um']
```

Always write patterns as `r"..."`.

## Not escaping the period

In the pattern `.edu`, the period is "any character": it matches
`harvard?edu` too. A literal period is `\.`.

## Forgetting ^ and $

`re.search` searches **anywhere** in the string: without `^` and `$`,
`"My email address is malan@harvard.edu."` counts as a valid address too.
If you are checking the whole string, `^...$` or `re.fullmatch`.

## Calling group when nothing matched

If the pattern does not match, `re.search` returns `None`, and `None` has no
`group`:

```python
import re

name = "David Malan"
matches = re.search(r"^(.+), *(.+)$", name)
print(matches.group(2))
```

```text
$ python format.py
Traceback (most recent call last):
  File "format.py", line 5, in <module>
    print(matches.group(2))
          ^^^^^^^^^^^^^
AttributeError: 'NoneType' object has no attribute 'group'
```

Ask first: `if matches := re.search(...):`.

## The wrong group number

This pattern has one group; there is no `group(2)`:

```python
import re

url = "https://twitter.com/davidjmalan"
matches = re.search(r"^https://twitter\.com/(\w+)$", url)
print(matches.group(2))
```

```text
$ python twitter.py
Traceback (most recent call last):
  File "twitter.py", line 5, in <module>
    print(matches.group(2))
          ~~~~~~~~~~~~~^^^
IndexError: no such group
```

Groups are counted from 1, from left to right in the order their
parentheses open. If you make the parentheses you use only for grouping
`(?:...)`, the numbers do not shift.

## An unclosed parenthesis

If the pattern itself is wrong, `re` raises an error before searching; the
message gives the position of the mistake in the pattern (counted from 0):

```python
import re

print(re.search(r"^(\w+@\w+\.edu$", "malan@harvard.edu"))
```

```text
$ python validate.py
Traceback (most recent call last):
  File "validate.py", line 3, in <module>
  ...
re.PatternError: missing ), unterminated subpattern at position 1
```

## Greedy .+

`+` and `*` take the **longest** piece they can. `<(.+)>` captures
everything from the first `<` to the last `>`:

```python
import re

html = "<b>bold</b> and <i>it</i>"
print(re.findall(r"<(.+)>", html))
```

```text
$ python tags.py
['b>bold</b> and <i>it</i']
```

Limit what can go inside with a set: `[^>]+` is "characters other than `>`".

```python
import re

html = "<b>bold</b> and <i>it</i>"
print(re.findall(r"<([^>]+)>", html))
```

```text
$ python tags.py
['b', '/b', 'i', '/i']
```

## Mixing up match and search

`re.match("b", "ab")` returns `None`: `match` only looks from the start of
the string. To search anywhere, `re.search`; for the whole string,
`re.fullmatch`.
