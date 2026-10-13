Küçük bir lojistik modelin kaybı (`loss(w)`) hazır. `numeric_gradient(w,
eps)` her ağırlık için `(loss(w + ε) − loss(w − ε)) / 2ε` türevini (yalnızca
o ağırlığı oynatarak) 4 basamakla döndürsün. `w`'nin kendisini
değiştirme.

**Beklenen çıktı:**

```
[0.5692, -0.6805]
[0.3333, -0.5833]
```
