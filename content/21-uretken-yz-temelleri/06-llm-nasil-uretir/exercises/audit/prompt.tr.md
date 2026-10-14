Salt okunur `tiny_chat.py` dersteki oyuncak modeli içeriyor (`ask`,
`CAPITALS`). `audit(countries)` her ülkeyi `ask(country)` ile sorsun.
Cevap `"the capital of X is Y ."` biçiminde: `X` cevabın ülkesi, `Y`
başkenti. Üç sayı döndür: `[doğru, yanlış başkent, başka ülke]`. Başkent
`CAPITALS[country]` ise doğru; değilse ve cevabın ülkesi sorulan ülke
değilse "başka ülke"; geri kalanı "yanlış başkent".

**Beklenen çıktı:**

```
[2, 0, 2]
```
