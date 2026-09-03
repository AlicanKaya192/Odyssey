Model "emin değilsen negatif de" diyor çünkü toplam hatayı azaltmaya
çalışıyor. Ona **bir pozitifi kaçırmanın daha pahalı olduğunu** söylemenin
bir yolu var.

```python
LogisticRegression(max_iter=1000, class_weight="balanced")
```

`"balanced"` her sınıfa sıklığının tersi oranında ağırlık veriyor.

**Yapman gerekenler:**

1. Veriyi hazırla, ayır (`stratify=y`) ve ölçekle.
2. Dört modeli sırayla ele al:
   - `logreg` — `LogisticRegression(max_iter=1000)`, ölçekli veriyle
   - `logreg-bal` — aynısı, `class_weight="balanced"` ile
   - `forest` — `RandomForestClassifier(n_estimators=200, random_state=42)`,
     **ölçeksiz** veriyle
   - `forest-bal` — aynısı, `class_weight="balanced"` ile
3. Her biri için tek satır yazdır: **ad, doğruluk, precision, recall, F1**
   (üç ondalık).
4. Son satırda ağırlıklı lojistik regresyonun recall'ünden varsayılanınkini
   çıkar ve yazdır.

**Beklenen çıktı:**

```
logreg 0.955 0.75 0.286 0.414
logreg-bal 0.88 0.269 0.667 0.384
forest 0.955 0.75 0.286 0.414
forest-bal 0.952 0.615 0.381 0.471
0.381
```

**Ağırlıklandırma recall'ü 0,286'dan 0,667'ye çıkardı.** 6 yerine 14
dolandırıcılık yakalanıyor. Son satır bu farkı yazıyor: **0,381**.

**Ama bedeli aynı satırda duruyor:** precision 0,75'ten 0,269'a düştü.
Model artık 52 işleme "dolandırıcılık" diyor ve 38'i yanlış alarm.
Doğruluk da 0,955'ten 0,880'e indi.

**Bu bir takas, bir iyileştirme değil.** Hangisinin doğru olduğu
problemin kendisine bağlı: kaçan bir dolandırıcılık mı daha pahalı, yoksa
boşuna aranan bir müşteri mi? Bu soruyu model cevaplayamıyor.

**Ormanda etki daha ölçülü:** recall 0,286'dan 0,381'e, precision 0,75'ten
0,615'e. F1 ise yükseliyor (0,414 → 0,471) — bu veride en dengeli sonuç.

Sebebi ağacın karar biçimi: lojistik regresyon bütün sınırı kaydırıyor,
ağaç ise yalnızca yaprakların oyunu değiştiriyor.
