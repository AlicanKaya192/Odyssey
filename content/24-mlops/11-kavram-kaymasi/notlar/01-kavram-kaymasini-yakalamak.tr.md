Kavram kayması girdilere bakarak görülmez; etiketler gelince görülür.

## Dersteki ölçümler

| Ay | Beklenen iptal | Gerçekleşen | Fark |
|---|---|---|---|
| 0 | 0,277 | 0,297 | -0,020 |
| 3 | 0,425 | 0,410 | 0,015 |
| 4 | 0,504 | 0,413 | 0,091 |
| 6 | 0,576 | 0,471 | 0,105 |

Fark 4. ayda birden büyüyor: kalibrasyon bozuldu.

## İki ağırlığın değişimi

| Özellik | İlk model | Son pencere |
|---|---|---|
| `monthly_fee` | 0,87 | 1,89 |
| `support_calls` | 1,02 | 0,24 |

Ağırlıklar ancak özellikler ölçeklendiyse (`StandardScaler`)
birbiriyle karşılaştırılabilir.

## Sinyaller

- **Kalibrasyon:** verilen ortalama olasılık ile gerçekleşen oran
  ayrışıyor.
- **Doğruluk:** girdiler pek kaymadığı hâlde doğruluk düşüyor.
- **Ağırlıklar:** yeni veriyle eğitilen modelin ağırlıkları eskisinden
  belirgin farklı.

## Yapma

- Kavram kaymasını yalnızca girdi dağılımına bakarak arama; PSI ilişkiyi
  ölçmez.
- Ölçeklenmemiş özelliklerin ağırlıklarını birbiriyle karşılaştırma.
- `predict(...).mean()` ile kalibrasyon ölçme; olasılık
  (`predict_proba`) gerekir.
