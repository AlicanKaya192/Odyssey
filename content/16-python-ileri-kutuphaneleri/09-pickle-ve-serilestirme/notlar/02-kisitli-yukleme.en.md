The rule does not change: do not load pickle data you do not trust. But
sometimes the data you have comes in no other format than pickle and you
know which types can be inside it. In that case you can **restrict** the
loader.

When pickle data needs a function or a class, it looks it up with
`find_class(module, name)`. If this method is overridden, only the allowed
names get through:

```python
import io
import pickle
from datetime import date

ALLOWED = {("datetime", "date")}


class SafeUnpickler(pickle.Unpickler):
    def find_class(self, module, name):
        if (module, name) in ALLOWED:
            return super().find_class(module, name)
        raise pickle.UnpicklingError(f"blocked: {module}.{name}")


def safe_loads(blob):
    return SafeUnpickler(io.BytesIO(blob)).load()


class Trap:
    def __reduce__(self):
        return (print, ("this ran while loading!",))


print(safe_loads(pickle.dumps({"day": date(2026, 3, 2), "n": [1, 2]})))
try:
    safe_loads(pickle.dumps(Trap()))
except pickle.UnpicklingError as error:
    print(error)
```

```text
{'day': datetime.date(2026, 3, 2), 'n': [1, 2]}
blocked: builtins.print
```

- Basic types like dictionaries, lists, strings and numbers never go through
  `find_class`; for the date, `datetime.date` is allowed.
- The trap object asked for `builtins.print` and was stopped; the message was
  never printed.
- `pickle.Unpickler(file)` expects a file; `io.BytesIO` makes the bytes in
  memory look like a file.

## Its limits

- The allow list is kept **narrow**. Allowing the whole `builtins` module
  (including `eval`, `exec`, `open`) removes the protection.
- This is a mitigation, not a full guarantee. For data from outside, the real
  answer is still a format that carries only data, like JSON.
- To make sure a file you produced was not changed on the way, signing the
  bytes with a key (`hmac`) is also used; that comes later, in the `hashlib`
  section.
