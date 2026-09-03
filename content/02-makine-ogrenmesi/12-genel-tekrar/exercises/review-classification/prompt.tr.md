Yeni veri: 800 hasta kaydı. `age`, `bmi`, `visits` (sayısal, eksik değer
var), `sex`, `region`, `smoker` (metin) ve hedef `readmitted` — hasta
taburcu olduktan sonra tekrar yatırıldı mı.

Veride bir de `followup_calls` sütunu var. **Bu alıştırmada onu
kullanmayacaksın**; sebebini üçüncü alıştırmada göreceksin.

**Yapman gerekenler:**

1. Veriyi oku. Eksik değer sayılarını ve pozitif sınıf oranını yazdır.
2. `X` olarak `followup_calls` ve `readmitted` dışındaki altı sütunu al.
   Ayır (`test_size=0.25`, `random_state=42`, `stratify=y`).
3. Test kümesindeki kayıt ve pozitif sayısını yan yana yazdır.
4. Taban çizgiyi kur (her şeye 0) ve doğruluğunu yazdır.
5. Pipeline ile `LogisticRegression(max_iter=1000)` eğit. Doğruluk,
   precision, recall ve F1'i tek satırda yazdır.
6. Karışıklık matrisini yazdır.
7. Aynı modeli `class_weight="balanced"` ile yeniden eğit ve aynı dört
   sayıyı yazdır.

**Beklenen çıktı:**

```
{'age': 0, 'sex': 0, 'region': 40, 'bmi': 56, 'visits': 32, 'smoker': 0, 'followup_calls': 0, 'readmitted': 0}
0.194
200 39
0.805
0.815 0.571 0.205 0.302
[[155   6]
 [ 31   8]]
0.65 0.293 0.564 0.386
```

**Taban çizgi 0.805, model 0.815.** Bir puanlık fark. Bölüm 09'un tablosu
tekrar karşında: pozitif sınıf %19,4 ve doğruluk bu problemde neredeyse
hiçbir şey söylemiyor.

**Karışıklık matrisi söylüyor:** 39 gerçek yeniden yatıştan **8'i**
yakalanmış, **31'i** kaçmış. Recall 0.205.

Bir hastane bu modeli kullansa yeniden yatışların beşte dördünü
göremeyecekti.

**Son satır ağırlıklandırmanın sonucu:**

| | Doğruluk | Precision | Recall | F1 |
|---|---|---|---|---|
| Varsayılan | 0.815 | 0.571 | 0.205 | 0.302 |
| `balanced` | 0.650 | 0.293 | **0.564** | 0.386 |

Recall 0.205'ten 0.564'e çıktı — 8 yerine 22 hasta yakalanıyor. Bedeli
precision'ın 0.571'den 0.293'e düşmesi ve doğruluğun 0.815'ten 0.650'ye
inmesi.

**Hangisi doğru?** Bu bir model sorusu değil, bir sağlık kararı: kaçırılan
bir yeniden yatış mı daha pahalı, yoksa boşuna takibe alınan bir hasta mı?
Model bunu cevaplayamıyor. Cevabı bilen kişi tabloya bakıp seçiyor.

**Doğruluğun düşmesine takılma.** 0.650, taban çizginin (0.805) altında
ama model artık gerçekten iş görüyor. Bu, doğruluğun yanıltıcılığının en
net hâli.
