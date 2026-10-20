# Tekrarlanabilir Eğitim

Dün modeli eğittin ve 0,788 ölçtün. Bugün hiçbir şeye dokunmadan aynı
kodu yeniden çalıştırdın ve 0,766 çıktı. Hangisi doğru? Bir şey mi
bozuldu? Eski sonuca nasıl geri dönersin? Bir eğitim **tekrarlanabilir**
(reproducible) değilse bu soruların hiçbirine cevap veremezsin. Bu
bölümde sonucu oynatan şeyleri tek tek buluyor ve sabitliyoruz.

## Aynı kod, farklı sonuç

Bir rastgele orman (random forest) modelini aynı veriyle üç kez
eğitelim. Veri her seferinde aynı: `make_customers(2000)`.

```python
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from ml_data import make_customers, NUMERIC


def to_xy(rows):
    X = [[r[c] for c in NUMERIC] + [1 if r["plan"] == "pro" else 0] for r in rows]
    y = [r["churned"] for r in rows]
    return X, y


X, y = to_xy(make_customers(2000))
for attempt in [1, 2, 3]:
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25)
    model = RandomForestClassifier(n_estimators=50).fit(X_train, y_train)
    print("attempt", attempt, "accuracy:", round(model.score(X_test, y_test), 3))
```

```text
attempt 1 accuracy: 0.774
attempt 2 accuracy: 0.734
attempt 3 accuracy: 0.784
```

Üç deneme, üç farklı sonuç. Sen bu kodu çalıştırsan yine başka üç sayı
görürdün. Kod da veri de aynıyken sonucun değişmesi, işin içinde
**rastgelelik** olduğunu gösteriyor.

## Rastgelelik nereden geliyor?

Yukarıdaki kodda iki yer rastgele davranıyor:

- **`train_test_split`** satırları bölmeden önce karıştırıyor. Her
  çalıştırmada test kümesine başka müşteriler düşüyor.
- **`RandomForestClassifier`** her ağacı rastgele seçilmiş satırlarla ve
  her bölmede rastgele seçilmiş sütunlarla kuruyor.

Başka birçok yöntem de rastgelelik kullanıyor: k-ortalamalar
başlangıç merkezlerini rastgele seçiyor, bir sinir ağı ağırlıklarına
rastgele değerlerle başlıyor. Bilgisayardaki rastgelelik aslında
**sözde rastgele** (pseudo-random): bir başlangıç sayısından, yani
**tohumdan** (seed) hesaplanan bir sayı dizisi. Tohum aynıysa dizi de
aynı.

## Tohumu sabitlemek

scikit-learn'de tohum `random_state` parametresiyle veriliyor. İki
rastgele adıma da bir tohum verelim:

```python
for attempt in [1, 2, 3]:
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.25, random_state=0)
    model = RandomForestClassifier(n_estimators=50, random_state=0)
    model.fit(X_train, y_train)
    print("attempt", attempt, "accuracy:", round(model.score(X_test, y_test), 3))
```

```text
attempt 1 accuracy: 0.768
attempt 2 accuracy: 0.768
attempt 3 accuracy: 0.768
```

Üç deneme artık birebir aynı. Bu kodu sen de çalıştırsan aynı sayıyı
görürsün.

Tohumu verirken bir kural: **tohumu her rastgele adıma ayrı ayrı ver.**
Programın başına bir kez `random.seed(0)` ya da `np.random.seed(0)`
yazmak da işe yarıyor gibi görünür, ama o tek ortak üreteç programın her
yerinde kullanılır. Araya rastgele sayı çeken yeni bir satır eklenince
sonraki bütün sayılar kayar. Python'da kendi üretecini kurmak da mümkün:
`random.Random(0)` yalnızca senin kullandığın bir üreteç verir.

## Tohum da bir ayar

Tohum sabitlenince sonuç tekrarlanıyor. Peki tohum değişince sonuç ne
kadar oynuyor? Önce bölmenin tohumunu, sonra modelin tohumunu değiştirip
bakalım:

```python
for seed in [0, 1, 2, 3, 4]:
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.25, random_state=seed)
    model = RandomForestClassifier(n_estimators=50, random_state=0)
    model.fit(X_train, y_train)
    print("split seed", seed, "accuracy:", round(model.score(X_test, y_test), 3))
for seed in [0, 1, 2]:
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.25, random_state=0)
    model = RandomForestClassifier(n_estimators=50, random_state=seed)
    model.fit(X_train, y_train)
    print("model seed", seed, "accuracy:", round(model.score(X_test, y_test), 3))
```

```text
split seed 0 accuracy: 0.768
split seed 1 accuracy: 0.788
split seed 2 accuracy: 0.758
split seed 3 accuracy: 0.786
split seed 4 accuracy: 0.762
model seed 0 accuracy: 0.768
model seed 1 accuracy: 0.768
model seed 2 accuracy: 0.764
```

Yalnızca bölme değişince doğruluk 0,758 ile 0,788
arasında oynadı. Model tohumunun etkisi bundan çok daha küçük. Buradan
iki ders çıkıyor:

- **İki modeli aynı bölmede karşılaştır.** Biri bir bölmede, öbürü başka
  bir bölmede ölçülürse aradaki farkın bir kısmı yalnızca şanstır.
- **Tohumu sonuca göre seçme.** Beş tohumu deneyip en iyi çıkanı
  raporlamak, modeli olduğundan iyi gösterir. Tohum eğitimden önce
  seçilir ve değiştirilmez. Tek bir bölmenin şansından kurtulmanın yolu
  çapraz doğrulama: birçok bölmenin ortalaması.

## Ayarlar tek yerde

Sonucu etkileyen her şey, yani verinin boyu, tohumlar ve modelin
ayarları, kodun içine dağılmış sabitler olarak durursa birini değiştirip
kayda geçirmeyi unutmak kolay. Hepsini tek bir sözlükte, bir **yapılandırma**
(configuration, kısaca config) içinde toplayalım. Eğitim fonksiyonu
yalnızca bu sözlüğe baksın:

```python
import json

CONFIG = {"rows": 2000, "data_seed": 7, "split_seed": 0,
          "n_estimators": 50, "model_seed": 0}


def train(config):
    X, y = to_xy(make_customers(config["rows"], seed=config["data_seed"]))
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.25, random_state=config["split_seed"])
    model = RandomForestClassifier(n_estimators=config["n_estimators"],
                                   random_state=config["model_seed"])
    model.fit(X_train, y_train)
    return model, round(model.score(X_test, y_test), 3)


model, accuracy = train(CONFIG)
print("accuracy:", accuracy)
print(json.dumps(CONFIG, indent=2))
```

```text
accuracy: 0.768
{
  "rows": 2000,
  "data_seed": 7,
  "split_seed": 0,
  "n_estimators": 50,
  "model_seed": 0
}
```

Artık "bu model nasıl eğitildi?" sorusunun cevabı bir sözlük. Sözlük
JSON olarak bir dosyaya yazılıp modelin yanında saklanabilir; aynı
sözlükle `train` yeniden çağrılınca aynı model çıkar. Gerçek projelerde
yapılandırma çoğu zaman ayrı bir YAML ya da JSON dosyasında durur ve
koddan ayrı okunur.

## Veriyi parmak iziyle tanımak

Yapılandırma kodun ayarlarını sabitliyor. Ya veri? Bu modülde veri bir
tohumdan üretiliyor, ama gerçek bir projede veri her gün değişen bir
tablodan geliyor. "Model hangi veriyle eğitildi?" sorusuna dosya adı
yetmez: aynı adlı dosyanın içi değişmiş olabilir.

Çözüm, verinin içeriğinden bir **özet** (hash) hesaplamak. SHA-256 gibi
bir özet fonksiyonu herhangi uzunluktaki veriden sabit uzunlukta bir
metin üretir; tek bir değer değişince özetin tamamı değişir. Bu yüzden
özete verinin **parmak izi** (fingerprint) denir:

```python
import hashlib


def fingerprint(rows):
    text = json.dumps(rows, sort_keys=True)
    return hashlib.sha256(text.encode("utf-8")).hexdigest()[:12]


rows = make_customers(2000)
print("data:", fingerprint(rows))
rows[0]["tenure"] = rows[0]["tenure"] + 1
print("one value changed:", fingerprint(rows))
print("again from the seed:", fingerprint(make_customers(2000)))
```

```text
data: a91a352912da
one value changed: 7de66b6647f6
again from the seed: a91a352912da
```

2000 müşteriden birinin tek bir değeri değişince parmak izi tamamen
değişti; aynı tohumdan yeniden üretilen veri ise aynı parmak izini
verdi. `sort_keys=True` sözlüklerin anahtarlarını sıraya diziyor: aynı
veri, anahtarları başka sırayla yazılmış diye farklı görünmesin. Özetin
tamamı 64 karakter; burada ilk 12'si yetiyor.

## Ortam: kütüphane sürümleri

Kod, ayarlar ve veri aynı olsa bile scikit-learn'ün başka bir sürümü
başka bir sonuç verebilir: bir varsayılan değer değişmiş, bir hesap
yöntemi düzeltilmiş olabilir. Makine Öğrenmesi Kütüphaneleri
modülünde gördüğün gibi bir sürümde kaydedilen modeli başka bir sürümde
açmak da sorun çıkarabiliyor. Bu yüzden iki şey yapılır:

- `requirements.txt`'te sürümler `==` ile sabitlenir
  (`scikit-learn==1.9.1`). CI/CD ve DevOps modülündeki temiz makine aynı
  sürümleri kurar.
- Eğitimin kaydına sürümler de yazılır.

## Eğitim kaydı

Şimdi hepsini bir araya getirelim. Bir eğitimin **kaydı** (run record),
o eğitimi yeniden üretmek için gereken her şeyi tutar:

```python
import sys
import sklearn

record = {
    "config": CONFIG,
    "data": fingerprint(make_customers(CONFIG["rows"], seed=CONFIG["data_seed"])),
    "python": sys.version.split()[0],
    "scikit-learn": sklearn.__version__,
    "accuracy": accuracy,
}
print(json.dumps(record, indent=2))
```

```text
{
  "config": {
    "rows": 2000,
    "data_seed": 7,
    "split_seed": 0,
    "n_estimators": 50,
    "model_seed": 0
  },
  "data": "a91a352912da",
  "python": "3.14.7",
  "scikit-learn": "1.9.1",
  "accuracy": 0.768
}
```

Altı ay sonra biri "bu model nereden geldi?" diye sorarsa cevap bu
kayıtta: hangi ayarlar, hangi veri, hangi ortam ve ölçülen sonuç. Deney
Takibi bölümünde bu kayıtları saklayan ve karşılaştıran küçük bir araç
kuracağız.

## Tekrarlanabilirliği sınamak

Tohumları vermeyi unutmak kolay; yeni eklenen bir adım tohumsuz
kalabilir. Bunu yakalamanın yolu, CI/CD ve DevOps modülündeki gibi bir
**test** yazmak: aynı yapılandırmayla iki kez eğit ve iki modelin
tahminlerini karşılaştır.

```python
model_a, _ = train(CONFIG)
model_b, _ = train(CONFIG)
X_check, _ = to_xy(make_customers(500, seed=99))
same = (model_a.predict_proba(X_check) == model_b.predict_proba(X_check)).all()
print("same predictions:", same)
```

```text
same predictions: True
```

Doğruluğu değil **tahminleri** karşılaştırıyoruz: iki farklı model
tesadüfen aynı doğruluğu verebilir, ama 500 müşterinin hepsinde aynı
olasılığı veriyorsa aynı modeldir. Bu test hatta konursa, tohumsuz bir
adım eklendiği gün hat kırmızıya döner.

## Özet

- Aynı kod ve veriyle farklı sonuç almanın nedeni **rastgelelik**:
  bölmedeki karıştırma, modelin içindeki rastgele seçimler.
- Rastgelelik bir **tohumdan** hesaplanır. scikit-learn'de
  `random_state`; tohumu her rastgele adıma ayrı ver.
- Bölmenin tohumu sonucu modelin tohumundan çok daha fazla oynatabilir.
  Modelleri aynı bölmede karşılaştır; tohumu sonuca göre seçme.
- Sonucu etkileyen bütün ayarları tek bir **yapılandırmada** topla.
- Verinin **parmak izi** (içeriğinin özeti) hangi verinin kullanıldığını
  kesin söyler.
- Kütüphane sürümlerini sabitle ve **eğitim kaydına** yaz.
- Tekrarlanabilirliği bir testle sına: aynı ayarla iki eğitim, aynı
  tahminler.
