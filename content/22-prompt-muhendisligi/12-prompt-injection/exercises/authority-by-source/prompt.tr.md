`allowed(tool, source, tools)` bir araç isteğine izin verilip
verilmeyeceğini söylesin: araç `tools`'ta yoksa `False`; aracın
`"irreversible"` değeri `True` ise yalnızca `source == "user"` iken
`True`; geri alınabilir araçlar her kaynaktan `True`.

**Beklenen çıktı:**

```
get_order document True
cancel_order document False
cancel_order user True
refund user False
```
