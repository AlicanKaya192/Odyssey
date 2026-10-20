Bir deney kaydında olması gerekenler:

| Alan | Örnek | Neden |
|---|---|---|
| Numara | `"run": 3` | Deneyi adıyla anmak için |
| Ayarlar | `{"model": "logistic", "C": 0.1}` | Deneyin bütün tarifi |
| Ölçümler | `{"val_accuracy": 0.832}` | Karşılaştırmak için |
| Verinin parmak izi | `"data": "a91a352912da"` | Hangi veriyle |
| Kodun sürümü | Git commit kimliği | Hangi kodla |
| Not | `"dropped the fee column"` | Neden denendi |

## JSON Lines

```text
{"run": 1, "params": {"model": "baseline"}, "metrics": {"val_accuracy": 0.748}}
{"run": 2, "params": {"model": "logistic", "C": 0.01}, "metrics": {...}}
```

- Her satır bir deney; her satır tek başına geçerli bir JSON.
- Yazmak: dosyayı ekleme kipinde aç (`open("a")`), sonuna bir satır yaz.
- Okumak: `[json.loads(line) for line in text.splitlines()]`.
- Eski satırlar hiç değiştirilmez; bir deney yanlışsa yeni bir satırla
  düzeltilir.

## Üç küme

| Küme | Ne için | Ne zaman |
|---|---|---|
| Eğitim | Modeli eğitmek | Her deneyde |
| Doğrulama | Deneyleri karşılaştırıp seçmek | Her deneyde |
| Test | Seçilen modeli raporlamak | Bir kez, en sonda |

## Temel çizgi

Hiçbir şey öğrenmeyen en basit tahmin: herkese en sık sınıfı söylemek.
Bu modülün verisinde doğrulama kümesinde 0,748. Her model önce bunu
geçmeli.

## Terimler

- **Deney takibi** (experiment tracking): her denemenin ayarlarını ve
  sonuçlarını kendiliğinden kaydetmek.
- **Deney** (run): bir ayar takımıyla bir eğitim ve ölçüm.
- **Temel çizgi** (baseline): modellerin geçmesi gereken en basit sonuç.
- **JSON Lines**: her satırı ayrı bir JSON olan dosya biçimi.
