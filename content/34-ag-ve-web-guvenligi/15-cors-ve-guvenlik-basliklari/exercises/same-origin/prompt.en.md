`same_origin(a, b)` should return `True` if the two addresses have the
same scheme, domain name and port. If no port is written, it is taken
from `DEFAULT_PORTS`. Use `urlsplit(...).hostname` for the domain name: it
comes in lower case. The starter code compares the addresses as text.

**Expected output:**

```
True
False
False
True
```
