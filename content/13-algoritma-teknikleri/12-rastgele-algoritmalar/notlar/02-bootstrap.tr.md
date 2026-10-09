On öğrencinin not ortalaması 80. Başka on öğrenci seçseydik ortalama ne kadar
değişirdi? Yeni veri toplamadan bunu tahmin etmenin yolu **bootstrap**: eldeki
veriden **yerine koyarak** aynı boyda yeni örnekler çek, her birinin
ortalamasını al ve bu ortalamaların ne kadar yayıldığına bak.

```python
import random
import statistics

random.seed(0)
scores = [72, 85, 90, 64, 78, 88, 95, 70, 81, 77]
means = []
for _ in range(10_000):
    resample = random.choices(scores, k=len(scores))   # yerine koyarak
    means.append(statistics.mean(resample))
means.sort()
print(statistics.mean(scores))
print(means[250], means[9750])                          # ortadaki %95
```

```text
80
74.2 85.6
```

On bin yeniden örneğin ortalamalarının ortadaki %95'i yaklaşık bu aralıkta:
on kişilik bir sınıf için ortalamanın ne kadar oynak olduğunu gösteren bir
**güven aralığı**. Formül gerekmiyor; yalnızca yerine koyarak örnekleme ve
biraz hesap gücü.

Rastgele orman (random forest) aynı fikri kullanır: her ağaç verinin bir
bootstrap örneğiyle eğitilir, ağaçların farklı hatalar yapması ortalamayı
sağlamlaştırır. Örneğe hiç girmeyen satırlar (yaklaşık üçte bir) o ağacın
**out-of-bag** doğrulama verisi olur.
