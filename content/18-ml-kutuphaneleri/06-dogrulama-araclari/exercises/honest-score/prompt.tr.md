Başlangıç kodunda 30 hastanın 5'er ölçümü var (`groups` hasta numarası) ve
etiket rastgele. `honest_score(k)` `KNeighborsClassifier(n_neighbors=k)` için
iki skor döndürsün (3 basamak):

- düz: `KFold(5, shuffle=True, random_state=0)` ortalaması
- grup: `GroupKFold(5)` ve `groups=groups` ile ortalama

Başlangıç kodu ikisini de düz `KFold` ile hesaplıyor.

**Beklenen çıktı:**

```
[1.0, 0.52]
```
