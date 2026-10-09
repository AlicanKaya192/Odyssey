`debug_value(log, value)` mesajı f-string ile kurduğu için `DEBUG` kapalıyken
de `value`'yu metne çeviriyor (`calls` artıyor). `log.debug("value: %s",
value)` biçimine çevir: kayıt yazılmayınca metin hiç kurulmasın.

**Beklenen çıktı:**

```
0
```
