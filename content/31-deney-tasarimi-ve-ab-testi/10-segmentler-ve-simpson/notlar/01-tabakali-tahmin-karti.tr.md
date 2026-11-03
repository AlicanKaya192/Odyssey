## Küçük bir Simpson örneği

```python
import pandas as pd

cells = pd.DataFrame({"week": [1, 1, 2, 2],
                      "group": ["A", "B", "A", "B"],
                      "buyers": [180, 22, 50, 52],
                      "users": [1500, 170, 1000, 1000]})
cells["rate"] = cells["buyers"] / cells["users"]
print(cells.pivot(index="week", columns="group", values="rate").round(3))
total = cells.groupby("group")[["buyers", "users"]].sum()
print((total["buyers"] / total["users"]).round(3).to_string())
share = cells.groupby("week")["users"].sum() / cells["users"].sum()
rates = cells.pivot(index="week", columns="group", values="rate")
print(round(((rates["B"] - rates["A"]) * share).sum(), 4))
```

```text
group     A      B
week              
1      0.12  0.129
2      0.05  0.052
group
A    0.092
B    0.063
0.0054
```

İki haftada da B önde, toplamda geride; tabakalı fark yine pozitif.

## Tabakalı tahmin adım adım

1. Her tabakada (hafta, platform...) iki grubun oranını ayrı hesapla.
2. Her tabakada farkı al: B − A.
3. Farkları tabakanın **toplam** kullanıcı payıyla ağırlıklandırıp topla.

Ağırlık iki grup için aynı olduğu için karışım farkı ortadan kalkar.

## Ne zaman gerekir?

- Atama oranı test ortasında değiştiyse (yavaş açılış).
- SRM bir tabakada var, ötekinde yoksa (önce nedeni bulunur).
- Tabakalar çok farklı davranıyorsa ve bileşim gruplar arasında
  dengesizse.

Atama her yerde aynı orandaysa tabakalı tahmin ile toplam neredeyse aynı
sonucu verir.
