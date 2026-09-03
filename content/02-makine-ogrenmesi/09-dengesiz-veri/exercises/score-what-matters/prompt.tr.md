Bir hiperparametre taraması yapacaksın: hangi ayar daha iyi? Bunu
çapraz doğrulamayla ölçeceksin. Ama `cross_val_score` varsayılan olarak
**doğruluk** hesaplıyor.

Dengesiz veride bunun ne demek olduğunu ölçelim.

**Yapman gerekenler:**

1. Veriyi hazırla, ayır (`stratify=y`) ve ölçekle.
2. `StratifiedKFold(n_splits=5, shuffle=True, random_state=42)` kur.
3. Şu beş ölçüyü sırayla dene: **accuracy, recall, f1, roc_auc,
   average_precision**. Her biri için `LogisticRegression(max_iter=1000)`
   modelini **eğitim** verisinde çapraz doğrula.
4. Her ölçü için tek satır yazdır: **ölçü adı, ortalama, yayılım**
   (üç ondalık).
5. Son satırda yayılımı **en dar** olan ölçünün adını ve **en geniş** olanın
   adını yan yana yazdır.

**Beklenen çıktı:**

```
accuracy 0.952 0.008
recall 0.317 0.188
f1 0.397 0.183
roc_auc 0.93 0.028
average_precision 0.521 0.144
accuracy recall
```

**Doğruluğun yayılımı 0,008.** Beş katın hepsi neredeyse aynı sayıyı
veriyor.

Bu iyi bir şey gibi görünüyor — kararlı, güvenilir. Değil. **Bir
hiperparametre taramasında bu ölçü hiçbir şey söyleyemez:** hangi ayarı
denersen dene, sonuç 0,95 civarında kalıyor. Sıralama yapamıyorsun.

**Recall'ün yayılımı 0,188** — yirmi üç kat fazla. Sebebi açık: her katta
yalnızca ~17 pozitif var ve birkaçının kaçması sayıyı belirgin oynatıyor.

Bu **gürültü**, evet. Ama içinde gerçek bir sinyal de var; doğrulukta
sinyalin kendisi yok.

**`roc_auc` ve `average_precision` ikisi arasında duruyor:** azınlık
sınıfına duyarlılar (0,930 ve 0,521 birbirinden çok farklı) ama tek tek
kayıtlara bağlı olmadıkları için yayılımları daha dar (0,028 ve 0,144).

**Uygulamada:** dengesiz veride hiperparametre araması genelde
`average_precision` ile yapılıyor. `GridSearchCV` de aynı `scoring`
parametresini alıyor.

**Genel kural:** yayılımı sıfıra yakın bir ölçü kararlı değil, **kör**.
