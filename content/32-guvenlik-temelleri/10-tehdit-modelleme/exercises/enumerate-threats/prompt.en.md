The `PER_ELEMENT` table is ready in the starter code. `elements` is made
of `[name, kind]` lists.

`enumerate_threats(elements)` should return the threats to ask about for
every part as `"name:LETTER"` texts: the parts in list order, the letters
in table order.

If a kind the table does not know comes in, treat it **like a process**
(all six letters): if you cannot be sure, ask more questions.

**Expected output:**

```
11
student:S
student:R
login:T
login:I
login:D
plugin:S
plugin:T
plugin:R
plugin:I
plugin:D
plugin:E
```
