Kod üç işi sırayla yürütüyor ve yaklaşık 600 ms sürüyor. `tokio::join!` ile birlikte yürüt, 500 ms'nin altına insin.

**Beklenen çıktı:**

```text
2 4 6
fast: true
```
