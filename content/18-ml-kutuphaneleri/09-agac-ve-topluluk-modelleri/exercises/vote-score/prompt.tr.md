`vote_score(weights)` lojistik regresyon ve rastgele ormanı
`VotingClassifier(..., voting="soft", weights=weights)` ile birleştirip 5
katlı ortalama doğruluğu (3 basamak) döndürsün. Başlangıç kodu `"hard"`
(çoğunluk oyu) kullanıyor; yumuşak oylamada olasılıklar ağırlıklarla
ortalanır.

**Beklenen çıktı:**

```
0.904
0.907
```
