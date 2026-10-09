`logging.basicConfig`'i günlükleri **stdout**'a, `INFO` düzeyinden
itibaren, `"%(levelname)s: %(message)s"` biçiminde yazacak şekilde düzelt.
`debug` mesajı görünmemeli, `info` ve `warning` görünmeli.

**Beklenen çıktı:**

```
INFO: job started
WARNING: low memory
```
