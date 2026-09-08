Three products have an empty `supplier_code`. Show `NONE` for those and the
actual code for the rest.

Columns: `name` and `supplier`. Sort by name. **Every product belongs in
the result** — this is not filtering.

```
name       supplier
---------  --------
Antivirus  S2      
Cable      S1      
Desktop    S3      
Headset    NONE    
Keyboard   S1      
...
```

What you want is not a condition but a **value replacer**: a function that
says what to show in place of an empty cell.

The name can mislead — `IS NULL` asks a question; the function you want
writes an answer.
