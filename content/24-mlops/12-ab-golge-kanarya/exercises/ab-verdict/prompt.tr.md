A/A gürültüsüyle bir A/B farkını yorumlayan `ab_verdict(diff, aa_gaps)` fonksiyonunu yaz:

- `aa_gaps`: A/A testinde ölçülen farklar (artı sayılar).
- Bant: sıralanmış farklarda `int(0.95 * uzunluk)` sıradaki değer, üç basamağa yuvarlanmış.
- `diff`'in mutlak değeri banttan büyükse `["real", bant]`, değilse `["noise", bant]` döndür.

**Beklenen çıktı:**

```
['real', 0.095]
['noise', 0.095]
['real', 0.095]
```
