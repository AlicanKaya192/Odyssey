Önceki bölüm tek bir ağacın kararsız olduğuyla bitti. Çözüm: **çok sayıda
ağaç kur, hepsine sor.**

Bu alıştırmada üç modeli yan yana koyacaksın — ve tek bir sayıya bakmanın
neden yetmediğini bir kez daha göreceksin.

**Yapman gerekenler:**

1. Veriyi hazırla ve ayır (`random_state=42`, `stratify=y`).
   **Ölçekleme yok** — hepsi ağaç tabanlı.
2. Taban çizgiyi yazdır (en sık sınıf, üç ondalık).
3. Üç modeli sırayla ele al:
   - `tree` — `DecisionTreeClassifier(max_depth=2, random_state=42)`
   - `forest` — `RandomForestClassifier(n_estimators=200, random_state=42)`
   - `boosting` — `GradientBoostingClassifier(random_state=42)`
4. Her biri için tek satır yazdır: **ad, test doğruluğu, CV ortalaması,
   CV yayılımı** (`StratifiedKFold`, 5 kat, `shuffle=True`,
   `random_state=42`, yalnızca **eğitim** verisinde).
5. **Test kazananını** ve **CV kazananını** yan yana yazdır.
6. İkisi farklıysa `different`, aynıysa `same` yazdır.

**Beklenen çıktı:**

```
0.7
tree 0.96 0.827 0.049
forest 0.9 0.867 0.063
boosting 0.88 0.873 0.053
tree boosting
different
```

**Test sütununa bakarsan ağaç kazanıyor: 0.96.** Ormanı da artırmayı da
geçiyor. O zaman bütün bu topluluk işi neye yarıyor?

**CV sütununa bak: sıralama tersine dönüyor.** Ağaç 0.827 ile **sonuncu**,
artırma 0.873 ile birinci.

Hangisine inanacaksın? Bölüm 05'ten hatırla: 50 kayıtlık bir test kümesinde
tek bir kayıt doğruluğu 0.02 oynatıyor. Bölüm 07'deki derinlik taramasında
test sütunu 0.82 → 0.96 → 0.80 diye zıplıyordu; **0.96 o zıplamanın tepe
noktası**, gerçek bir üstünlük değil.

CV ise beş ayrı ölçümün ortalaması. Yayılımlar da yakın (0.049-0.063), yani
aradaki 0.046'lık fark gürültünün sınırında — ama en azından tek bir
çekilişe dayanmıyor.

**Son satır bu modülün en çok tekrarlanan dersi:** tek bir sayı bir model
hakkında karar verdirmiyor.
