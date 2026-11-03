## Küme halinde atamanın bedeli: tasarım etkisi

Aynı kümedeki kullanıcılar birbirine benzer. Bu benzerlik **sınıf içi
korelasyonla** (ICC) ölçülür: 0 ise kümedeki herkes bağımsız, 1 ise
kümedeki herkes aynı. Küme halinde atanan bir testin varyansı, aynı sayıda
kullanıcının tek tek atandığı teste göre **tasarım etkisi** kadar büyür:

$$\text{DEFF} = 1 + (m - 1)\,\text{ICC}$$

Burada m küme başına kullanıcı sayısı. Etkin örneklem n / DEFF olur.

```python
def design_effect(cluster_size, icc):
    return 1 + (cluster_size - 1) * icc


for icc in [0.0, 0.01, 0.05]:
    deff = design_effect(300, icc)
    print(icc, round(deff, 2), round(30000 / deff))
```

```text
0.0 1.0 30000
0.01 3.99 7519
0.05 15.95 1881
```

Şehir başına 300 kullanıcıda ICC yalnızca 0,01 bile olsa 30 000 kullanıcı
yaklaşık 7500 bağımsız kullanıcı kadar bilgi taşır.

## Küme testinde analiz

- Birim kümedir: her kümenin ortalaması bir gözlem.
- Kümeler arası Welch testi ya da küme düzeyinde bootstrap.
- Kullanıcıları bağımsız sayıp test etmek, Oran Metrikleri ve Delta
  Yöntemi bölümündeki hatanın aynısıdır: standart hata küçük, alarm fazla.

## Küme sayısı

Gürültüyü azaltan şey kümenin büyüklüğü değil **küme sayısıdır**. 10 dev
şehir, 100 küçük şehirden daha az bilgi taşır.
