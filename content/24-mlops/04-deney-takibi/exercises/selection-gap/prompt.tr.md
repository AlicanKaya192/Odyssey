Dersteki kazananın laneti ölçümünü bir fonksiyona çevir. `scores` bir liste: her eleman bir modelin `[doğrulama, test]` skorları. `selection_gap(scores)` bir sözlük döndürsün:

- Doğrulama skoru en yüksek modeli bul (eşitlikte önce gelen).
- `"val_lead"`: o modelin doğrulama skoru eksi bütün doğrulama skorlarının ortalaması.
- `"test_lead"`: **aynı** modelin test skoru eksi bütün test skorlarının ortalaması.
- İkisini de üç basamağa yuvarla.

**Beklenen çıktı:**

```
validation lead: 0.022
test lead: 0.005
```
