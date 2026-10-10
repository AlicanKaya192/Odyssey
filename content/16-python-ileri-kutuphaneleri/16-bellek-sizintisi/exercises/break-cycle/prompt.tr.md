Ebeveyn çocuğunu (`children`), çocuk ebeveynini (`parent`) gösteriyor: bir
döngü. Çöp toplayıcı kapalıyken (`gc.disable()`) kök silinince hiçbiri
silinmiyor. `parent`'ı `weakref.ref(parent)` olarak sakla ve `parent_node()`
`self.parent()` döndürsün (ebeveyn yoksa `None`). Beklenen çıktı:

```
root
['child', 'root']
```

**Beklenen çıktı:**

```
root
['child', 'root']
```
