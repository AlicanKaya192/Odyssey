`run_rnn(xs, Wx, Wh, b)` gizli durumu sıfırlarla (`b` uzunluğunda) başlatıp
`xs`'teki her girdiyle `tanh(x @ Wx + h @ Wh + b)` adımını atsın ve son gizli
durumu 3 basamaklı liste olarak döndürsün. Aynı girdiler ters sırada farklı
sonuç vermeli.

**Beklenen çıktı:**

```
[-0.253, 0.553]
[0.551, 0.363]
```
