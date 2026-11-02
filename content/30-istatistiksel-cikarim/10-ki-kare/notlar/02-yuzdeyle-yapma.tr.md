Ki-kare testine yüzde vermek sık yapılan ve sessizce yanlış sonuç veren bir
hatadır: kod çalışır, bir p değeri çıkar, ama o p yanlış örneklem
büyüklüğüne aittir.

## Aynı oranlar, farklı kanıt

İki grupta alışveriş oranı %12 ve %20 olsun. Bunu 100'er kişide görmekle
1000'er kişide görmek aynı kanıt değildir:

```python
from scipy import stats

small = [[12, 88], [20, 80]]
large = [[120, 880], [200, 800]]
print(round(stats.chi2_contingency(small).pvalue, 4))
print(f"{stats.chi2_contingency(large).pvalue:.1e}")
```

```text
0.177
1.4e-06
```

100'er kişide fark anlamlı değil; 1000'er kişide çok güçlü. Oranlar aynı,
yalnızca sayılar farklı.

## Yüzde tablosu neden yanıltır?

Tabloya `[[12, 88], [20, 80]]` diye yüzdeleri yazarsan test bunları **100'er
kişilik sayım** sanar. Gerçekte 1000'er kişi varsa p'yi olduğundan çok
büyük bulursun ve gerçek bir farkı kaçırırsın. Gerçekte 30'ar kişi varsa
tam tersi: p'yi olduğundan küçük bulursun ve yanlış alarm verirsin.

## Doğrusu

- Her zaman ham sayımlardan kur: `pd.crosstab(veri["grup"], veri["sonuç"])`.
- Oranları ayrıca hesapla ve raporla; teste sayımları ver.
- Elinde yalnızca yüzdeler ve grup boyları varsa sayıları geri hesapla:
  `oran × grup boyu`, en yakın tam sayıya.
