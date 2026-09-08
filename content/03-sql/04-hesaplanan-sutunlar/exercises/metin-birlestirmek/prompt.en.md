Produce a label for every product in this shape:

```
etiket
-------------------
Antivirus (Yazilim)
Fare (Aksesuar)
Kablo (Aksesuar)
...
```

That is: the product name, a space, then the category in brackets.

Return a single column and call it `etiket`. Sort by name.

**Use `CONCAT`.** You could join with `+`, but when one piece is empty `+`
wipes out the whole result while `CONCAT` skips it. There is no empty
piece here, but it is better to build the habit on the right tool.
