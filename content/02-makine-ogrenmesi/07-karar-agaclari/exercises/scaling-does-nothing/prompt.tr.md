Bölüm 06'da ölçeklemeyi atlamak KNN'i **taban çizginin altına** düşürmüştü:
0.64'e karşı 0.92. Aynı veride ağaca ne oluyor?

**Yapman gerekenler:**

1. Aynı akışı kur ve ayır.
2. **İki ağaç** eğit, ikisi de `max_depth=3` ve `random_state=42`:
   - biri **ham** veriyle
   - öteki **ölçeklenmiş** veriyle
3. İki doğruluğu yan yana yazdır (üç ondalık).
4. Sonuçlar aynıysa `same`, farklıysa `different` yazdır.
5. Bölüm 06'da KNN'in ölçeklemeden kazandığı farkı yazdır: **0.92 - 0.64**,
   iki ondalık.

**Beklenen çıktı:**

```
0.8 0.8
same
0.28
```

**İki sayı birebir aynı.** Tek bir ondalık bile oynamıyor.

**Neden:** ağaç `income <= 137500` diye soruyor. Ölçeklendikten sonra bu
soru `income_scaled <= 0.42` oluyor. **Eşik değişiyor, sıralama
değişmiyor** — ve ağaç yalnızca sıralamayla ilgileniyor. Hangi kayıtların
eşiğin üstünde kaldığı hiç değişmediği için ağacın kendisi de değişmiyor.

**Üçüncü satır karşıtlığı gösteriyor:** aynı veride, aynı ölçekleme işlemi
KNN'de **0.28**'lik bir fark yaratıyordu.

<br>

| Model | Ölçeklemesiz | Ölçekli | Fark |
|---|---|---|---|
| KNN | 0.64 | 0.92 | **0.28** |
| Ağaç | 0.80 | 0.80 | **0.00** |

**Alınacak ders: "her zaman ölçekle" diye bir kural yok.** Ölçekleme,
modelin neye baktığına bağlı bir adım:

- **Uzaklık kullananlar** (KNN, SVM, kümeleme) → zorunlu
- **Eşik kullananlar** (ağaçlar, orman, gradyan artırma) → gereksiz

Ağaçta ölçekleme yapmanın zararı yok ama faydası da yok; boşa harcanan bir
adım.

**Aynı sebeple ağaçlar aykırı değerlere de dayanıklı:** bir kayıt yüz kat
büyük olsa bile hâlâ "eşiğin üstünde" grubunda, o kadar.
