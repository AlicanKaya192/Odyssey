`expected_std(fan_in, nonlinearity)` Kaiming/Xavier ailesinin önerdiği standart
sapmayı hesaplasın: `kazanç / sqrt(fan_in)`. Kazancı
`nn.init.calculate_gain(nonlinearity)` veriyor. 4 basamakla döndür.

**Beklenen çıktı:**

```
0.0884
0.1667
```
