`layer_shapes(size)` hazır `model`'in her katmanına bir ileri kanca taksın,
`torch.zeros(1, 1, size, size)` ile modeli çalıştırsın ve her katmanın çıktı
şeklini liste olarak (sırayla) döndürsün. Kancalar iş bitince sökülmeli:
fonksiyon ikinci kez çağrılınca da aynı sonucu vermeli.

**Beklenen çıktı:**

```
[1, 4, 8, 8]
[1, 4, 8, 8]
[1, 4, 4, 4]
[1, 8, 2, 2]
[1, 8, 2, 2]
[1, 32]
[1, 128]
6
```
