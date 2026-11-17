`hook_shape(index, size)` modelin `index` numaralı katmanına bir ileri kanca
taksın, `(1, 1, size, size)` sıfır girdiyle bir kez çalıştırıp yakalanan
çıktının şeklini alsın, kancayı söküp modeli bir kez daha çalıştırsın.
`[yakalanan şekil, yakalanan çıktı sayısı]` döndürsün (sökülen kanca ikinci
çalıştırmada bir şey eklememeli).

**Beklenen çıktı:**

```
[[1, 8, 8, 8], 1]
[[1, 16, 6, 6], 1]
```
