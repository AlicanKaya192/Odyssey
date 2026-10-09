`numeric_grad(w)` fonksiyonunu yaz: hazır `f`'nin `w` noktasındaki gradyanını
**merkezi farkla** hesapla: her `i` için
`(f(w + ε eᵢ) − f(w − ε eᵢ)) / 2ε`, `ε = 1e-6`. Sonucu `round(..., 4)`
değerlerden oluşan liste olarak döndürsün.

**Beklenen çıktı:**

```
[-6.0, 4.0]
[-1.0, 3.0]
```
