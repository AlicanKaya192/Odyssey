## The order of validation

1. **Canonical form:** `unicodedata.normalize("NFKC", s).strip()`,
   `casefold()` if needed.
2. **Type:** is it a number, a date? Check the form first, then convert.
3. **Form:** allowed characters and length with `re.fullmatch(pattern, s)`.
4. **Range or set:** `13 <= age <= 120`, `country in COUNTRIES`.
5. **Refuse:** if one fails, the data is not used; the user is told which
   field is wrong (but no internal details).

## Python patterns

| Job | Pattern |
|---|---|
| Full match | `re.fullmatch(r"[a-z0-9_]{3,20}", s)` |
| ASCII digits only | `re.fullmatch(r"[0-9]{1,3}", s)` (`isdigit` also accepts superscripts) |
| Set | `s in ALLOWED` |
| Canonical | `unicodedata.normalize("NFKC", s).strip().casefold()` |
| Safe path | `posixpath.normpath(posixpath.join(BASE, name))` + `startswith(BASE + "/")` |
| Command | An argument list; `shlex.quote(value)` if needed |

## Encoding by context

| Context | Encoder |
|---|---|
| HTML | `html.escape` |
| Address parameter | `urllib.parse.quote(s, safe="")` |
| JSON | `json.dumps` |
| SQL | A parameterised query (not encoding) |
| Shell command | An argument list, `shlex.quote` |

## Rules

- Validation **on the server**; the browser's is only a convenience.
- An **allow list**, not a block list.
- Canonical form first, then validation.
- Validation does not replace encoding; both together.
