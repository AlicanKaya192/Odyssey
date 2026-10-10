`round_price(text, rule)` fonksiyonunu yaz: `text`'i `Decimal`'a çevirip iki
ondalığa yuvarlasın. `rule` `"up"` ise `ROUND_HALF_UP`, `"even"` ise
`ROUND_HALF_EVEN` kullansın. Sonucu metin olarak döndürsün
(`"2.665"`, `"up"` → `"2.67"`).

**Beklenen çıktı:**

```
2.67 2.66
10.00
```
