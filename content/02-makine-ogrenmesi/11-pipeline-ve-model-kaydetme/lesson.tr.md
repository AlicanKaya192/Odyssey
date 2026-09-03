# Pipeline ve Modeli Kaydetmek

Bölüm 04'te modele veri hazırlamayı öğrendin: eksik değerleri doldur,
metin sütunlarını kodla, sayıları ölçekle. Kural tek cümleydi — **önce
ayır, sonra dokun.**

O kuralı elle uygulamak sandığından zor. Bu bölüm onu **yapısal olarak
imkânsız** hâle getiriyor, ve sonunda modeli diske kaydetmeyi gösteriyor.

Veri 600 abone: `city`, `plan` (metin), `tenure`, `monthly`, `support`
(sayı) ve hedef `churn`. Üç sütunda eksik değer var: `city` 24, `monthly`
48, `support` 30.

## Elle yapmanın hâli

Bu veriyi bir modele vermek için gereken adımlar:

```python
# 1. sayisal sutunlarin medyani (EGITIMDEN)
median = X_train[num].median()
X_train[num] = X_train[num].fillna(median)
X_test[num] = X_test[num].fillna(median)

# 2. metin sutunlarinin modu (EGITIMDEN)
mode = X_train[cat].mode().iloc[0]
X_train[cat] = X_train[cat].fillna(mode)
X_test[cat] = X_test[cat].fillna(mode)

# 3. metin sutunlarini kodla (EGITIMDE fit)
encoder = OneHotEncoder(handle_unknown="ignore")
encoder.fit(X_train[cat])

# 4. sayilari olcekle (EGITIMDE fit)
scaler = StandardScaler()
scaler.fit(X_train[num])

# 5. ikisini birlestir
# 6. modeli egit
```

Altı adım, dört tane "eğitimden" uyarısı ve iki ayrı `fit`. Şimdi asıl
soru: **altı ay sonra tek bir yeni abone geldiğinde bu altı adımı aynı
sırayla ve aynı sayılarla tekrar edebilecek misin?**

`median` ve `mode` değerlerini bir yere yazdın mı? `encoder` ile
`scaler`'ı kaydettin mi? Sütun sırasını hatırlıyor musun?

Bu adımların **hepsi modelin bir parçası.** Ayrı durdukları sürece
kaybolmaya, karışmaya ve sızmaya açıklar.

## Pipeline

`Pipeline` bu adımları tek bir nesneye bağlıyor:

```python
from sklearn.pipeline import Pipeline

pipe = Pipeline([
    ("prepare", preprocessor),
    ("model", LogisticRegression(max_iter=1000)),
])

pipe.fit(X_train, y_train)
prediction = pipe.predict(X_test)
```

`fit` çağrıldığında son adım dışındaki her adımın `fit_transform`'u,
son adımın `fit`'i çalışıyor. `predict` çağrıldığında her adımın
`transform`'u, sonra son adımın `predict`'i.

**Kritik nokta:** `transform` çağrıldığında hiçbir adım yeniden
öğrenmiyor. Medyan eğitimde hesaplandı ve orada kaldı.

## Farklı sütunlara farklı işlem

Sayısal sütunlara medyan + ölçekleme, metin sütunlarına mod + kodlama
gerekiyor. `ColumnTransformer` bunu yapıyor:

```python
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer

numeric = ["tenure", "monthly", "support"]
text = ["city", "plan"]

preprocessor = ColumnTransformer([
    ("num", Pipeline([
        ("impute", SimpleImputer(strategy="median")),
        ("scale", StandardScaler()),
    ]), numeric),
    ("cat", Pipeline([
        ("impute", SimpleImputer(strategy="most_frequent")),
        ("encode", OneHotEncoder(handle_unknown="ignore")),
    ]), text),
])
```

İç içe iki `Pipeline` bir `ColumnTransformer` içinde. Karmaşık görünüyor
ama okunuşu düz: **sayısal sütunlara şunu, metin sütunlarına bunu yap.**

Sonuç, dokuz sütunluk bir matris:

```
num__tenure  num__monthly  num__support
cat__city_Ankara  cat__city_Bursa  cat__city_Izmir
cat__plan_basic   cat__plan_plus   cat__plan_pro
```

Ölçüm: taban çizgi 0.573, pipeline'ın test doğruluğu **0.793.**

**`handle_unknown="ignore"` neden var:** test kümesinde eğitimde
görülmemiş bir şehir çıkarsa `OneHotEncoder` varsayılan olarak hata
veriyor. `ignore` o satırın bütün şehir sütunlarını sıfır yapıyor.
Üretimde bu ayar olmadan model ilk beklenmedik değerde çöküyor.

## Asıl kazanç: sızıntı imkânsızlaşıyor

Bölüm 05'te `cross_val_score` öğrendin. Onu **elle hazırlanmış** veriyle
kullanmak sessiz bir sızıntı:

```python
X_prepared = scaler.fit_transform(X_train)      # butun egitim verisini gordu
cross_val_score(model, X_prepared, y_train, cv=skf)
```

Ölçekleyici bütün eğitim verisinin ortalamasını öğrendi; sonra bu veri
beş kata bölündü. Her katın "doğrulama" kısmı, ölçekleyicinin zaten
gördüğü satırlardan oluşuyor.

**Pipeline verilirse `cross_val_score` her katta bütün adımları baştan
eğitiyor:**

```python
cross_val_score(pipe, X_train, y_train, cv=skf)
```

Bu, sızıntıyı bir dikkat meselesi olmaktan çıkarıp **yapısal olarak
imkânsız** hâle getiriyor.

### Ne kadar fark ediyor

Ölçekleme ve doldurma için etki genelde küçük. Ama **hedefe bakan** bir
adım varsa büyüyor.

Eğitim verisine 200 tane **tamamen rastgele** sütun ekleyip, `SelectKBest`
ile en iyi 15 sütunu seçelim:

| Seçim nerede yapıldı | CV doğruluğu |
|---|---|
| Çapraz doğrulamanın **dışında** | **0.780** |
| Pipeline'ın **içinde** | **0.716** |

**6,4 puanlık fark, tamamen uydurma.** Seçici bütün eğitim verisine bakıp
"şu 15 sütun hedefe en çok benziyor" dedi; o sütunların bir kısmı yalnızca
gürültüydü ve tesadüfen o veride hedefe benziyordu. Sonra aynı veride
doğrulanınca iyi görünüyorlar.

Pipeline içinde her kat kendi seçimini yapıyor ve numara bozuluyor.

**Not:** `train_test_split` bölüm 04'te öğrendiğin ilk savunma; bu ikinci
savunma **çapraz doğrulamanın içi** için.

## Hiperparametre araması

Pipeline `GridSearchCV` ile doğrudan çalışıyor. Adım adı ile parametre adı
**iki alt çizgiyle** birleşiyor:

```python
from sklearn.model_selection import GridSearchCV

grid = {"model__C": [0.01, 0.1, 1, 10, 100]}
search = GridSearchCV(pipe, grid, cv=skf, scoring="accuracy")
search.fit(X_train, y_train)

print(search.best_params_)   # {'model__C': 0.1}
print(search.best_score_)    # 0.74
```

Ölçülen tarama:

```
C=0.01   0.711
C=0.1    0.740      <- en iyi
C=1      0.738
C=10     0.736
C=100    0.736
```

`C` lojistik regresyonun düzenlileştirme ayarı: küçük değer modeli
kısıtlıyor, büyük değer serbest bırakıyor. Burada 0.1 ile 100 arasındaki
fark 0.004 — yani bu veride `C` pek bir şey değiştirmiyor. **Bunu da
ölçerek öğrendik.**

**Ön işleme adımları da aranabiliyor:**

```python
grid = {
    "prepare__num__impute__strategy": ["median", "mean"],
    "model__C": [0.1, 1, 10],
}
```

Üç seviye alt çizgi: `prepare` adımının `num` bölümündeki `impute`
adımının `strategy` parametresi. Doldurma stratejisi artık bir
hiperparametre.

`search.best_estimator_` en iyi ayarla **bütün eğitim verisinde yeniden
eğitilmiş** pipeline'ı veriyor; `search.predict(...)` doğrudan onu
kullanıyor.

## Modeli kaydetmek

Eğitilmiş bir model bellekte duruyor. Program kapanınca gidiyor.

```python
import joblib

joblib.dump(pipe, "model.joblib")
loaded = joblib.load("model.joblib")
```

**Kaydedilen şey pipeline'ın tamamı:** medyanlar, mod, kodlayıcının
öğrendiği kategoriler, ölçekleyicinin ortalama ve standart sapması, model
katsayıları ve sütun sırası. Hepsi tek dosyada.

Yüklenen model ham veriyle çalışıyor — **eksik değerli ham veriyle bile:**

```python
new = pd.DataFrame([
    {"city": "Bursa", "plan": "basic", "tenure": 3,
     "monthly": 140.0, "support": 4},
    {"city": "Izmir", "plan": "pro", "tenure": 48,
     "monthly": 45.0, "support": 0},
    {"city": None, "plan": "plus", "tenure": 20,
     "monthly": None, "support": 1},
])
print(loaded.predict(new))              # [1 0 0]
print(loaded.predict_proba(new)[:, 1])  # [0.993 0.007 0.466]
```

Üçüncü satırda `city` ve `monthly` eksik. Pipeline onları eğitimde
öğrendiği medyan ve modla dolduruyor ve tahmin üretiyor: 0.466 — kararsız,
ama çalışıyor.

**Elle hazırlanmış bir modelde bu satır bir çökme olurdu.**

## Kaydedilen dosyanın taşımadıkları

<figure class="fig">
  <div class="anat">
    <div class="anat-row"><span class="anat-key">Taşıdığı</span><span>Bütün adımlar, öğrenilmiş sayılar, sütun sırası</span></div>
    <div class="anat-row"><span class="anat-key">Taşımadığı</span><span>Kütüphane sürümleri</span></div>
    <div class="anat-row"><span class="anat-key">Taşımadığı</span><span>Eğitim verisi ve nereden geldiği</span></div>
    <div class="anat-row"><span class="anat-key">Taşımadığı</span><span>Seçtiğin karar eşiği</span></div>
    <div class="anat-row"><span class="anat-key">Taşımadığı</span><span>Ölçtüğün skorlar</span></div>
  </div>
  <figcaption>Dosyanın yanına bir metin dosyası koymak, altı ay sonraki sana yapılmış bir iyilik.</figcaption>
</figure>

**Sürüm uyumu gerçek bir sorun.** `joblib` dosyası Python nesnelerini
saklıyor; farklı bir scikit-learn sürümünde yüklemek uyarı verebiliyor ya
da çalışmayabiliyor. Modelin yanına `requirements.txt` koymak alışkanlık
hâline gelmeli.

**`pickle` yerine `joblib`** kullanılıyor: aynı işi yapıyor ama büyük NumPy
dizilerinde belirgin biçimde daha hızlı ve daha küçük dosya üretiyor.

**Güvenlik uyarısı:** `joblib.load` dosyanın içindeki Python nesnelerini
kuruyor. Güvenmediğin bir kaynaktan gelen model dosyası, açıldığında kod
çalıştırabiliyor. Kendi ürettiğin dosyalar dışında dikkatli ol.

## Tam akış

<figure class="fig">
  <div class="flow">
    <span class="node"><b>1</b><br>oku ve<br>ayır</span>
    <span class="arrow">&rarr;</span>
    <span class="node"><b>2</b><br>pipeline<br>kur</span>
    <span class="arrow">&rarr;</span>
    <span class="node"><b>3</b><br>modelleri<br>karşılaştır</span>
    <span class="arrow">&rarr;</span>
    <span class="node"><b>4</b><br>ayarları<br>ara</span>
    <span class="arrow">&rarr;</span>
    <span class="node acc"><b>5</b><br>testte<br>bir kez ölç</span>
    <span class="arrow">&rarr;</span>
    <span class="node"><b>6</b><br>kaydet ve<br>notunu yaz</span>
  </div>
  <figcaption>Üçüncü ve dördüncü adım hep eğitim tarafında; test kümesi yalnızca beşinci adımda açılıyor.</figcaption>
</figure>

## Bu bölümde neyi atladık

- **`RandomizedSearchCV`.** Izgaranın her noktasını denemek yerine rastgele
  bir kısmını deniyor. Parametre sayısı arttığında ızgara üstel büyüyor;
  rastgele arama aynı süreyle çok daha geniş bir alanı tarıyor.
- **`FunctionTransformer` ve kendi adımını yazmak.** `fit` ve `transform`
  metotları olan herhangi bir sınıf pipeline'a girebiliyor; kendi özellik
  üretme kodun da öyle.
- **Model servis etmek.** Kaydedilen dosyayı bir HTTP servisine koymak,
  sürümlemek, izlemek. Bunlar makine öğrenmesi değil yazılım mühendisliği
  konuları ve ayrı bir alan (MLOps).
- **Model kayması (drift).** Üretimdeki veri zamanla eğitim verisinden
  uzaklaşıyor ve model sessizce kötüleşiyor. Çözüm izleme ve düzenli
  yeniden eğitim.

Bu bölümün özeti: **model yalnızca son adım değil; ön işlemenin tamamı
modelin parçası, o yüzden birlikte eğitiliyor ve birlikte kaydediliyor.**
