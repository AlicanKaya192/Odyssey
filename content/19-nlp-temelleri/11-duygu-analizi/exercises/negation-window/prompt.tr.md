`negated(text, window)` dersteki olumsuzlama kuralını uygulasın. Tokenları
`re.findall(r"[a-z']+|[.,!?]", text.lower())` ile al:

- Noktalama işareti pencereyi kapatır.
- `NEGATORS`'tan bir kelime pencereyi `window` kelimelik açar, kendisi puan
  almaz.
- Diğer kelimeler `GOOD` +1, `BAD` −1; pencere açıksa işaret ters çevrilir
  ve pencere bir kelime azalır.

**Beklenen çıktı:**

```
-1
2
1
```
