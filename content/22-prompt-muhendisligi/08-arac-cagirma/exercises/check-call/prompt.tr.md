`check_call(call, specs)` bir araç çağrısını denetlesin; `specs`
araç adı → `{argüman: kalıp}`. Sırayla: araç `specs`'te yoksa
`"unknown tool <ad>"`; argüman adları kümesi beklenenle aynı değilse
`"arguments must be "` + beklenen adların `", "` ile birleşimi; bir
argüman kalıbına `re.fullmatch` ile uymuyorsa `"<argüman> has the wrong
form"`; hepsi geçerse `"ok"`. Çağrıda `arguments` yoksa boş sözlük say.

**Beklenen çıktı:**

```
ok
arguments must be order_id
order_id has the wrong form
unknown tool refund
```
