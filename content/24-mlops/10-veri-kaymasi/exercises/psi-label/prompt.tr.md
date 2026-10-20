Başparmak kuralına göre bir PSI değerini etikete çeviren `psi_label(value)` fonksiyonunu yaz:

- `0.1`'in altında: `"stable"`
- `0.1` ile `0.25` arasında (ikisi de dahil): `"moderate"`
- `0.25`'in üstünde: `"large"`

**Beklenen çıktı:**

```
0.012 stable
0.1 moderate
0.229 moderate
0.25 moderate
0.456 large
```
