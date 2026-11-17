`attention(q, k, v)` ölçekli nokta çarpım dikkatini elle hesaplasın:
`softmax(q @ k.T / √d) @ v` (`d` sorgu vektörünün uzunluğu, softmax son
boyutta). Sonucu her sayı 3 basamaklı iç içe liste olarak döndürsün.

**Beklenen çıktı:**

```
[[6.698, 3.302]]
[[5.0, 5.0]]
```
