Sıcaklık bir dağılımı nasıl değiştiriyor? ", my"dan sonra gelen kelimenin
dağılımında (10 seçenek) en büyük olasılığa ve **entropiye** (dağılımın
belirsizliği, bit olarak) bakalım:

```python
probs = list(next_probs(",", "my").values())
for t in [0.1, 0.5, 1.0, 2.0, 10.0]:
    weights = [p ** (1 / t) for p in probs]
    q = [w / sum(weights) for w in weights]
    entropy = -sum(x * math.log2(x) for x in q if x > 0)
    print(t, round(max(q), 3), round(entropy, 2))
print(round(math.log2(len(probs)), 2))
```

```text
0.1 0.985 0.12
0.5 0.595 1.37
1.0 0.446 1.81
2.0 0.305 2.63
10.0 0.136 3.29
3.32
```

- `T = 1` modelin kendi dağılımı. `T` küçüldükçe en olası seçenek bütün
  ağırlığı topluyor; `T → 0` açgözlü seçimin aynısı.
- `T` büyüdükçe dağılım düzleşiyor ve entropi üst sınırına (10 seçenek için
  `log2 10`) yaklaşıyor: `T → ∞` bütün seçeneklere eşit şans, yani modelin
  bilgisini atmak.
- Sıcaklık modelin bildiklerini değiştirmez; yalnızca o bilgiye ne kadar
  güvenerek seçim yapıldığını ayarlar. Kesin cevap istenen işte (kod, hesap,
  bilgi sorusu) düşük, beyin fırtınası gibi işlerde daha yüksek sıcaklık
  kullanılır.
