`conv_output_length(length, kernel, padding, stride)` bir `nn.Conv1d`'nin
çıkış uzunluğunu formülle hesaplasın: `(length + 2·padding − kernel) // stride
+ 1`.

**Beklenen çıktı:**

```
60
64
30
```
