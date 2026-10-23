Kullanıcı bir alışveriş listesini virgülle ya da noktalı virgülle ayırarak yazıyor, ayıracın çevresinde boşluk olabilir de olmayabilir de (`apples, pears;plums ; figs`). Listeyi `re.split` ile böl ve her öğeyi ayrı satıra, çevresindeki boşluklar olmadan yaz.

Örnek çalıştırma (soru metnini istediğin gibi yazabilirsin, yalnızca çıktın denetlenir):

```text
$ python cozum.py
Items: apples, pears;plums ; figs
apples
pears
plums
figs
```
