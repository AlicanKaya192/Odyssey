Write a function that puts a label at the front of log lines.

Define a function called `make_label`. It takes two parameters:

| Parameter | Meaning |
|---|---|
| `text` | the text to label |
| `prefix` | the label to put in front — **default value `INFO`** |

The function should **return** a string of this shape: the label, a colon, a
space, then the text.

Then call it twice:

- Into `first`, the text `Server started` with the **default label**.
- Into `second`, the text `Disk almost full` with the label `WARN`.

Print both, one under the other. Expected output:

```
INFO: Server started
WARN: Disk almost full
```

> Do not use `print` inside the function; hand the result back with `return`.
