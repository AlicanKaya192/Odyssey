# MLOps Nedir

Makine Öğrenmesi patikasında bir modeli eğittin, test verisinde ölçtün ve
iyi bir sayı gördün. Çoğu ders orada biter. Gerçek bir işte ise asıl iş
orada başlıyor: model her gün yeni veriyle karşılaşacak, birileri onu
kullanacak, veri değişecek ve model bir gün sessizce kötüleşecek. Bu
modül, bir modeli defterden (notebook) çıkarıp **güvenilir bir sisteme**
dönüştürmeyi anlatıyor. Bu bölümde bunun neden ayrı bir iş olduğunu ve
hangi parçalardan oluştuğunu görüyoruz.

## Modülün örneği: abonelik iptali

Bütün modül boyunca aynı örnekle çalışacağız. Bir abonelik servisi,
hangi müşterilerin aboneliğini iptal edeceğini (**churn**) önceden
bilmek istiyor; böylece o müşterilere bir indirim önerebilir. Her
müşterinin beş özelliği var:

- `tenure`: kaç aydır abone
- `monthly_fee`: aylık ücret
- `support_calls`: destek hattını kaç kez aradığı
- `usage_hours`: ayda kaç saat kullandığı
- `plan`: `basic` ya da `pro`

Hedef sütun `churned`: müşteri iptal ettiyse `1`, etmediyse `0`.

Veri bir dosyadan değil, `ml_data.py` modülünden geliyor. Bu modül her
alıştırmanın yanında salt okunur olarak duruyor. `make_customers(n)`
her bilgisayarda aynı `n` müşteriyi üretiyor, çünkü içinde sabit
tohumlu (seed) bir rastgele sayı üreteci var:

```python
from ml_data import make_customers

rows = make_customers(2000)
print(len(rows), "customers")
for key, value in rows[0].items():
    print(key, "=", value)
churn = sum(r["churned"] for r in rows) / len(rows)
print("churn rate:", round(churn, 3))
```

```text
2000 customers
id = C00-00001
tenure = 67
monthly_fee = 15.78
support_calls = 1
usage_hours = 47.6
plan = basic
churned = 0
churn rate: 0.288
```

Her on müşteriden yaklaşık üçü iptal ediyor. `make_customers`'ın bir
de `month` (ay) parametresi var: veriyi zamanda ileri götürüyor. Bunun
neden gerektiğini birazdan göreceğiz.

## Defterde model bitti mi?

Makine Öğrenmesi patikasındaki gibi bir model eğitelim. `plan` metin
olduğu için onu sayıya çeviriyoruz (`pro` ise `1`):

```python
from sklearn.linear_model import LogisticRegression
from ml_data import make_customers, NUMERIC


def to_xy(rows):
    X = [[r[c] for c in NUMERIC] + [1 if r["plan"] == "pro" else 0] for r in rows]
    y = [r["churned"] for r in rows]
    return X, y


X, y = to_xy(make_customers(2000))
model = LogisticRegression(max_iter=1000).fit(X, y)

X_test, y_test = to_xy(make_customers(1000, seed=99))
print("test accuracy:", round(model.score(X_test, y_test), 3))
```

```text
test accuracy: 0.813
```

`NUMERIC`, `ml_data.py`'nin içindeki dört sayısal sütunun adı.
`seed=99` farklı bir tohum: eğitimde hiç görülmemiş müşteriler. Model
yeni müşterilerde 0,813 doğruluğa ulaşıyor: kabaca her beş
müşteriden dördünü doğru tahmin ediyor. Defterde iş bitmiş gibi
görünüyor.

Şimdi aynı modeli, eğitildikten sonraki aylarda gelen müşterilerde
deneyelim. Model hiç değişmiyor; yalnızca müşteriler değişiyor:

```python
for month in [0, 2, 4, 6]:
    X_new, y_new = to_xy(make_customers(1000, seed=99, month=month))
    print("month", month, "accuracy:", round(model.score(X_new, y_new), 3))
```

```text
month 0 accuracy: 0.813
month 2 accuracy: 0.777
month 4 accuracy: 0.674
month 6 accuracy: 0.686
```

Doğruluk altı ay içinde 0,813 iken 0,686 oldu ve kimse
bunu fark etmedi, çünkü model hata vermiyor. Her müşteri için bir tahmin
üretmeye devam ediyor; yalnızca tahminleri eskisinden çok daha sık yanlış çıkıyor. Bu
modüldeki bütün işlerin özü bu cümlede: **bir yazılım hatası programı
durdurur, bir modelin kötüleşmesi ise sessizdir.**

Defterde sorulmayan sorular şunlar:

- Model hangi veriyle, hangi kodla, hangi ayarlarla eğitildi? Aynısını
  yarın yeniden üretebilir miyiz?
- Yeni bir model eskisinden gerçekten iyi mi? Kim karar veriyor?
- Model kullanıcıya nasıl ulaşıyor? Saniyede kaç tahmin yapabiliyor?
- Modelin kötüleştiğini nasıl anlayacağız? Anlayınca ne yapacağız?

## MLOps: makine öğrenmesi + DevOps

CI/CD ve DevOps modülünde kod için bir hat kurduk: her değişiklikte kod
kendiliğinden test ediliyor, paketleniyor ve yayına hazırlanıyordu.
**MLOps** (machine learning operations) aynı fikri makine öğrenmesi
sistemlerine uyguluyor. Ama arada önemli bir fark var:

<figure class="fig">
  <div class="versus">
    <div><h4>Sıradan yazılım</h4>Davranışı yalnızca koddan gelir. Kod değişmedikçe program aynı şeyi yapar. Hat kodu test eder ve yayınlar.</div>
    <div><h4>Makine öğrenmesi sistemi</h4>Davranışı kod <b>ve veriden</b> gelir. Kod hiç değişmese de veri değişince model kötüleşebilir. Hat kodu, veriyi ve modeli birlikte izler.</div>
  </div>
  <figcaption>ML sisteminde değişebilen üç şey var: kod, veri ve model.</figcaption>
</figure>

Bu yüzden MLOps'un üç ek işi var:

1. **Veriyi de denetlemek:** eğitime giren veri beklenen biçimde mi?
   (Veri Doğrulama bölümü)
2. **Üçünü birlikte sürümlemek:** hangi model, hangi veriyle, hangi
   kodla üretildi? (Tekrarlanabilir Eğitim, Sürümleme, Deney Takibi)
3. **Yayından sonra izlemek:** model gerçek dünyada hâlâ iyi mi?
   (İzleme, Veri Kayması, Kavram Kayması)

## Yaşam döngüsü

Bir ML sisteminin hayatı bir çizgi değil, bir döngü:

<figure class="fig">
  <div class="flow">
    <span class="node">Veri</span>
    <span class="arrow">→</span>
    <span class="node">Eğit</span>
    <span class="arrow">→</span>
    <span class="node">Değerlendir</span>
    <span class="arrow">→</span>
    <span class="node acc">Sun</span>
    <span class="arrow">→</span>
    <span class="node">İzle</span>
  </div>
  <figcaption>İzlemede bir sorun görülünce yeni veriyle döngü baştan başlar.</figcaption>
</figure>

- **Veri:** veriyi topla, temizle, doğrula.
- **Eğit:** modeli eğit; ayarları ve sonucu kaydet.
- **Değerlendir:** yeni modeli eskisiyle aynı ölçütle karşılaştır;
  yeterince iyi değilse yayına çıkmasın.
- **Sun** (serve): modeli tahmin isteyenlerin kullanabileceği hâle
  getir, örneğin bir API'nin arkasına koy.
- **İzle:** gelen veriye ve tahminlerin başarısına bak. Bozulma görülünce
  yeni veriyle yeniden eğit.

Yukarıdaki ölçümde eksik olan parça son kutuydu: model sunulmuş ama
izlenmiyordu.

## Model kodu buzdağının ucu

Bir ML sisteminde modeli eğiten kod genellikle en küçük parçadır.
Etrafında onu çalışır tutan çok daha büyük bir düzen var:

<figure class="fig anat">
  <div class="anat-row"><span>Veri toplama</span><span>Veriyi kaynaklardan düzenli olarak almak.</span></div>
  <div class="anat-row"><span>Veri doğrulama</span><span>Eksik, bozuk ya da beklenmedik değerleri eğitime girmeden yakalamak.</span></div>
  <div class="anat-row"><span>Özellik hazırlama</span><span>Ham veriyi modelin beklediği sayılara çevirmek; eğitimde ve sunmada aynı şekilde.</span></div>
  <div class="anat-row"><span><b>Model kodu</b></span><span>Modeli eğiten birkaç satır.</span></div>
  <div class="anat-row"><span>Kayıt ve sürümleme</span><span>Her modelin nereden geldiğini saklamak.</span></div>
  <div class="anat-row"><span>Sunma</span><span>Tahminleri hızlı ve güvenilir şekilde vermek.</span></div>
  <div class="anat-row"><span>İzleme</span><span>Kötüleşmeyi fark etmek ve haber vermek.</span></div>
</figure>

Bu parçalardan biri ihmal edilince sistem zamanla kırılgan hâle geliyor:
kimse modeli yeniden üretemiyor, eğitimdeki ve sunmadaki veri
hazırlığı birbirinden ayrışıyor ya da kötüleşme aylarca fark edilmiyor.
Yazılımda bunun adı **teknik borç** (technical debt): bugün kısa yoldan
gidersen yarın faiziyle ödersin. ML sistemlerinde bu borç kodun dışında,
veride ve süreçte birikiyor.

## Olgunluk seviyeleri

Ekiplerin MLOps'ta nerede olduğunu anlatmak için sık kullanılan bir
sınıflama var:

- **Seviye 0, elle:** her adım elle yapılıyor. Biri defterde modeli
  eğitip dosyayı başka birine veriyor. Yeniden eğitim aylar sürüyor.
- **Seviye 1, otomatik eğitim hattı:** veriden modele giden adımlar bir
  hat olarak yazılmış; yeni veri gelince model kendiliğinden yeniden
  eğitiliyor ve değerlendiriliyor (sürekli eğitim, continuous training).
- **Seviye 2, hattın kendisi de CI/CD'de:** eğitim hattının kodu
  değişince o da test ediliyor ve yayınlanıyor; CI/CD ve DevOps
  modülündeki her şey eğitim hattına da uygulanıyor.

Her ekibin seviye 2'ye ihtiyacı yok. Ayda bir değişen küçük bir model
için seviye 1 bile fazla olabilir. Önemli olan, sistemin şu anda hangi
seviyede olduğunu bilmek ve riskine göre seçmek.

## Bu modülde nasıl çalışacağız

- Bütün alıştırmalar Python. Veri `ml_data.py`'den geliyor; sonuçlar her
  bilgisayarda aynı.
- Gerçek bir bulut servisi, sunucu ya da hesap yok. Model kaydı, deney
  takibi ve özellik deposu gibi araçların ne yaptığını onları küçük
  Python sınıflarıyla kendimiz kurarak görüyoruz; derslerde gerçek
  araçların adları da geçiyor.
- Modeller scikit-learn ile; Makine Öğrenmesi patikasındaki kadarını
  bilmen yeterli.

## Özet

- Defterde iyi ölçülen bir model yalnızca başlangıç. Model sessizce
  kötüleşebilir: hata vermez, yanlış tahmin etmeye devam eder.
- **MLOps**, DevOps'un fikirlerini ML sistemlerine uygulamak. Farkı:
  davranış koddan ve veriden gelir; kod, veri ve model birlikte izlenir.
- Yaşam döngüsü: **veri → eğit → değerlendir → sun → izle**, sonra yine
  veri.
- Model kodu sistemin küçük bir parçası; doğrulama, sürümleme, sunma ve
  izleme ihmal edilince teknik borç birikir.
- Olgunluk: seviye 0 elle, seviye 1 otomatik eğitim hattı, seviye 2 hattın
  kendisi de CI/CD'de.
