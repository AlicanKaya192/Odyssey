`render(template, values)` should first find missing and unused
variables; if there is even one, return the text `missing [...], unused
[...]` (both lists in alphabetical order, in the lesson's form).
Otherwise fill the template **in one pass**: with `SLOT.sub`, the `str`
of each placeholder's value in its place. Marks inside a value that was
put in are not filled.

**Expected output:**

```
Ada wrote: Is {{name}} ok?
missing ['message'], unused []
```
