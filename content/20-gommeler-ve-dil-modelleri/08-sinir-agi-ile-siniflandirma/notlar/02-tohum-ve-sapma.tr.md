Derste tek bir tohumla eğittik. Sonuç tohuma ne kadar bağlı? Aynı ağı beş
farklı tohumla kurup eğitelim (birinci nottaki `train` fonksiyonuyla):

```python
scores = []
for seed in range(5):
    rng = np.random.default_rng(seed)
    P = {"E": rng.normal(0, 0.1, (V, 16)),
         "W1": rng.normal(0, np.sqrt(2 / 16), (16, 32)), "b1": np.zeros(32),
         "W2": rng.normal(0, np.sqrt(1 / 32), (32, 3)), "b2": np.zeros(3)}
    scores.append(train(P, epochs=20, seed=seed))
print(scores)
print(round(float(np.mean(scores)), 3), round(float(np.std(scores)), 3))
```

```text
[0.864, 0.88, 0.882, 0.876, 0.868]
0.874 0.007
```

- Beş tohum beş farklı doğruluk veriyor. Fark başlangıç ağırlıklarından ve
  örneklerin karıştırılma sırasından geliyor.
- İki modeli tek bir çalıştırmayla karşılaştırmak yanıltıcı olabilir: bu
  aralıktaki bir fark tohumun eseri olabilir. Birkaç tohumla çalıştırıp
  ortalama ve standart sapmayı raporla.
- Doğrusal modellerde (lojistik regresyon) bu sorun çok daha küçüktür:
  kayıp dışbükeydir, her başlangıç aynı çözüme gider. Sinir ağlarının
  kaybında birçok yerel çözüm vardır.
