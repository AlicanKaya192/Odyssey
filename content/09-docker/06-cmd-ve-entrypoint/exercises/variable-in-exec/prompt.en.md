This image should print `hi Ada`, but it prints `hi $NAME`: in the exec form
there is no shell to expand the variable.

**What to do:** keeping `CMD` in the exec form, call the shell explicitly:
`echo hi $NAME` should run through `sh -c`.

**Expected output:**

```
hi Ada
```
