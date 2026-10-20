Hattaki kapı ayrı bir betiktir. Eğitim betiği ölçümleri `metrics.json`'a
yazar, kapı betiği onları okuyup karar verir. Bir taslak:

```python
import json
import sys

RULES = {"min_accuracy": 0.78, "min_lift": 0.05, "min_slice": 0.75}

metrics = json.loads(open("metrics.json", encoding="utf-8").read())
failures = []
if metrics["accuracy"] < RULES["min_accuracy"]:
    failures.append("accuracy below the floor")
if metrics["accuracy"] < metrics["baseline"] + RULES["min_lift"]:
    failures.append("too close to the baseline")
for name, value in metrics["slices"].items():
    if value < RULES["min_slice"]:
        failures.append(f"{name} slice too low")

for failure in failures:
    print("FAIL:", failure)
sys.exit(1 if failures else 0)
```

- Eğitim ile kapı **ayrı** betik: kapı kuralları değişince modeli
  yeniden eğitmek gerekmez; ölçümler dosyada duruyor.
- `sys.exit(1)` adımın kırmızıya dönmesini sağlar; GitHub Actions bir
  adımın başarısını çıkış koduna bakarak anlar.
- Her sorun ayrı satırda yazılır: hattın kaydında neden düştüğü okunur.

## Kontrol listesi

- Kapı her çekme isteğinde çalışıyor mu?
- CI'daki eğitimin verisi ve tohumu sabit mi? (Değilse kapı bazen
  geçer, bazen düşer: kararsız test.)
- Her dilim için ayrı çıta var mı?
- Ölçümler `if: always()` ile saklanıyor mu?
- Eşikler bir yerde yazılı ve gerekçeli mi?

## Yapma

- Kapı düşünce eşiği düşürüp geçirme; önce neden düştüğüne bak.
- Kapıyı yalnızca ortalamaya bağlama; dilimler ortalamada kaybolur.
- CI'da saatler süren eğitim çalıştırma; hat yavaşlar, kimse beklemez.
