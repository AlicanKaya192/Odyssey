The abstract `Formatter` class is ready: subclasses register themselves
in `registry` with `name="..."` and must write `format(text)`. Write two
plugins: `name="upper"` turns the text to uppercase, `name="reverse"`
reverses it. Then let `apply(name, text)` find the class in the registry,
build an object and return the `format` result.

**Expected output:**

```
ODYSSEY
yessydo
['reverse', 'upper']
```
