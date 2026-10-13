Dersteki kural "Not bad"i olumsuz sanıyordu. `predict_neg(text)` aynı
`GOOD` ve `BAD` listeleriyle çalışsın, ama bir listedeki kelimenin **hemen
önünde** `not` varsa o kelimenin etkisini tersine çevirsin: olumlu kelime -1,
olumsuz kelime +1 saysın. Skor pozitifse `"positive"`, negatifse
`"negative"`, sıfırsa `"neutral"` döndürsün.

Çıktının son satırı 2000 yorumdaki doğru tahmin sayısı; dersteki kural 898
yorumu biliyordu. Üçüncü örneğe de bak: "not" ile kelime arasına başka bir
kelime girince kural yine yanılıyor.

**Beklenen çıktı:**

```
positive
negative
positive
1005
```
