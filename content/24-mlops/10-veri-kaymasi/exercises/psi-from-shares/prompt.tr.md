Referansın ve güncel verinin kutu payları aynı sırayla veriliyor. `psi_from_shares(reference, current)` fonksiyonunu yaz:

- Her paya en az `0.0001` taban uygula (boş kutuda `log(0)` olmasın).
- `Σ (güncel - referans) × ln(güncel / referans)` toplamını üç basamağa yuvarlayıp döndür.

**Beklenen çıktı:**

```
0.0
0.228
4.257
```
