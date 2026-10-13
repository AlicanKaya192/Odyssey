`sgns_loss(v, u_pos, u_negs)` bir çiftin kaybını 3 basamakla döndürsün:

`L = −log σ(v · u_pos) − Σ log σ(−v · u_k)`

`u_negs` olumsuz bağlam vektörlerinin listesi. `sigmoid` hazır.

**Beklenen çıktı:**

```
1.565
1.386
```
