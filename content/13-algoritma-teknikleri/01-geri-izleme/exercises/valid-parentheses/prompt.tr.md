`parentheses(n)` fonksiyonunu yaz: `n` çift parantezle yazılabilen bütün
**geçerli** dizileri döndürsün. Her adımda önce `(`, sonra `)` dene; bu
sırayla üretince sonuç kendiliğinden sıralı çıkar.

Budama kuralları:

- `(` yalnızca açık sayısı `n`'den azsa
- `)` yalnızca kapanan sayısı açıktan azsa

- `parentheses(2)` → `['(())', '()()']`

**Beklenen çıktı:**

```
((()))
(()())
(())()
()(())
()()()
16796
```
