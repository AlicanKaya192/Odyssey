`make_password(length)` should produce a random password made of letters
and digits; the password must contain **at least one lower-case letter,
one upper-case letter and one digit**.

- Choose the characters with `secrets.choice`; the `random` module is
  predictable, and a seed produces the same passwords on every run.
- If the password does not contain all three kinds, throw it away and
  make a new one.

The code below makes 50 passwords and prints their properties, not the
passwords themselves.

**Expected output:**

```
lengths ok: True
classes ok: True
unique: 50
```
