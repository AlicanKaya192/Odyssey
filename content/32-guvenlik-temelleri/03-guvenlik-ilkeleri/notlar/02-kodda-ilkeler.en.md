In code, a principle is often the difference of a single line. In every
pair below the first one breaks the principle and the second applies it.

## An unknown user

```python
allowed = rules.get(user, ["read", "write"])
allowed = rules.get(user, [])
```

The first line gives a user who is not on the list privileges by default.
The second gives an empty list: everything not mentioned is forbidden.

## When there is an error

```python
try:
    ok = check_permission(user, item)
except Exception:
    ok = True
```

```python
try:
    ok = check_permission(user, item)
except Exception:
    ok = False
```

Look at what is returned when the error is caught. If you cannot be sure,
refuse, and record the error in the log.

## Format checks

```python
if not name.endswith(".exe"):
    save(name)
```

```python
if name.rsplit(".", 1)[-1].lower() in {"pdf", "png", "jpg"}:
    save(name)
```

The first is a blocklist, the second an allowlist. The second has
`lower()`: so `PHOTO.PNG` is accepted too and `.PNG` and `.png` are not
treated differently.

## The default of a setting

```python
debug = settings.get("debug", True)
debug = settings.get("debug", False)
```

If the line is missing from the settings file, the system has to stay on
the safe side. Debug mode often dumps internal details (paths, versions,
queries) on the screen.

## Simplicity

If a permission rule grows with many nested `if`s, turn it into a table:
who may do what is written in a dictionary, and the code only looks at the
table. Reading a table is easier than following branches in code.
