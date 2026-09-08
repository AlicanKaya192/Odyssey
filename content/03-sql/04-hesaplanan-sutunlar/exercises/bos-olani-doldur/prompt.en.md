Three products have an empty `tedarikci_kod`. Show `YOK` for those and the
actual code for the rest.

Columns: `ad` and `tedarikci`. Sort by name. **Every product belongs in
the result** — this is not filtering.

```
ad           tedarikci
-----------  ---------
Antivirus    T2
Fare         T1
Kablo        T1
Klavye       T1
Kulaklik     YOK
...
```

What you want is not a condition but a **value replacer**: a function that
says what to show in place of an empty cell.

The name can mislead — `IS NULL` asks a question; the function you want
writes an answer.
