Hızlanmanın iki ucuz yolu: aynı soruyu tekrar hesaplamamak ve gereğinden
büyük model kullanmamak.

## Önbellek (50 000 istek, 6794 farklı müşteri)

| Önbellek boyu | Önbellekten karşılanan |
|---|---|
| 10 | 0,128 |
| 100 | 0,388 |
| 1000 | 0,667 |
| 5000 | 0,852 |

- **LRU:** dolunca en uzun süredir sorulmayan çıkar.
- **Anahtar:** müşteri + model sürümü.
- **TTL:** her kaydın bir ömrü var; süre dolunca yeniden hesaplanır.

## Model boyu (rastgele orman, derinlik 6)

| Ağaç | Doğruluk |
|---|---|
| 5 | 0,810 |
| 20 | 0,812 |
| 100 | 0,813 |
| 400 | 0,814 |

Bu bilgisayarda tek tahmin 5 ağaçla yaklaşık 1 ms, 400 ağaçla yaklaşık
45 ms.

## Yapma

- Önbellek anahtarına model sürümünü koymayı unutma; yeni model eski
  skorları göstermeye devam eder.
- Doğruluktaki binde birlik artış için gecikmeyi onlarca katına çıkarma;
  önce bir gecikme sınırı koy.
