Softmax çıktısı `a` ve çıktıya gelen türev `da` verildiğinde
`softmax_backward(a, da)` puanlara giden türevi döndürsün: her eleman için
`a_i · (da_i − a · da)` (`a · da` nokta çarpımı), 4 basamak. Bu türevlerin
toplamı her zaman sıfırdır.

**Beklenen çıktı:**

```
[0.35, -0.09, -0.26]
True
```
