`CondNet` toplamı pozitifse `x * 2`, değilse `x * -1` döndürüyor. Şu
hâliyle sıradan bir `if` kullandığı için dışa aktarma hata veriyor.
`forward`'ı `torch.cond` ile yeniden yaz; `cond_outputs` hazır.

**Beklenen çıktı:**

```
[2.0, 4.0, 6.0]
[1.0, 2.0, -0.5]
```
