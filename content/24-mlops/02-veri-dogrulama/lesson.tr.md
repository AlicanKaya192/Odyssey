# Veri Doğrulama

Her ay yeni müşteri verisi geliyor ve model bu veriyle yeniden
eğitiliyor. Bir ay, veriyi hazırlayan ekip ücretleri kuruş cinsinden
göndermeye başlıyor. Kimse haber vermiyor. Eğitim kodu çalışıyor, model
kaydediliyor, hat yeşil. Ama model artık daha kötü. Bu bölümde bozuk
verinin eğitime girmeden nasıl yakalanacağını görüyoruz: buna **veri
doğrulama** (data validation) deniyor.

## Bozuk veri sessizce geçer

Önce temiz veriyle eğitip test kümesinde ölçen küçük bir fonksiyon
yazalım. Test kümesi hep aynı: `make_customers(500, seed=99)`.

```python
from sklearn.ensemble import RandomForestClassifier
from ml_data import make_customers, NUMERIC


def to_xy(rows):
    X = [[r[c] for c in NUMERIC] + [1 if r["plan"] == "pro" else 0] for r in rows]
    y = [r["churned"] for r in rows]
    return X, y


X_test, y_test = to_xy(make_customers(500, seed=99))


def evaluate(rows):
    model = RandomForestClassifier(n_estimators=50, random_state=0)
    model.fit(*to_xy(rows))
    return round(model.score(X_test, y_test), 3)


print("clean batch:", evaluate(make_customers(2000)))
```

```text
clean batch: 0.79
```

Şimdi aynı veriyi üç farklı biçimde bozalım. Bunlar gerçek projelerde
sık görülen hatalar:

- Ücret kuruş cinsinden geliyor (29,90 yerine 2990).
- Paket adı büyük harfle yazılıyor (`"pro"` yerine `"PRO"`).
- Bazı satırlarda kullanım süresi boş (`None`).

```python
cents = make_customers(2000)
for row in cents:
    row["monthly_fee"] = round(row["monthly_fee"] * 100)
print("fees in cents:", evaluate(cents))

upper = make_customers(2000)
for row in upper:
    row["plan"] = row["plan"].upper()
print("plan in capitals:", evaluate(upper))

holes = make_customers(2000)
for row in holes[::10]:
    row["usage_hours"] = None
print("empty usage:", evaluate(holes))
```

```text
fees in cents: 0.744
plan in capitals: 0.78
empty usage: 0.782
```

Üçünde de **hiçbir hata çıkmadı**. Ücreti kuruşla gelen veride doğruluk
0,79'dan 0,744'e düştü: model büyük sayılara
göre kurallar öğrendi, test kümesindeki gerçek ücretler o kuralların
hiçbirine uymadı. Büyük harfli paket adı `to_xy`'de `"pro"`ya eşit
olmadığı için bütün müşteriler `basic` sayıldı. Boş değerleri ise
scikit-learn'ün ağaçları kendiliğinden işleyebiliyor; yine sessiz.

İşte tehlike burada: kod hata verseydi hemen fark ederdik. Veri hatası
çoğu zaman kodu durdurmuyor, yalnızca modeli kötüleştiriyor. Bu yüzden
veriyi **eğitimden önce** kendimiz denetlemeliyiz.

## Kurallar: veri sözleşmesi

Önce verinin nasıl olması gerektiğini yazalım. Her sütun için bir kural:
sayılar hangi aralıkta olmalı, metinler hangi değerleri alabilir. Bu
kurallar topluluğuna **şema** (schema) ya da veriyi gönderenle alan
arasındaki anlaşma olduğu için **veri sözleşmesi** (data contract)
deniyor:

```python
SCHEMA = {
    "tenure": {"min": 1, "max": 72},
    "monthly_fee": {"min": 5, "max": 100},
    "support_calls": {"min": 0, "max": 10},
    "usage_hours": {"min": 0, "max": 100},
    "plan": {"allowed": ["basic", "pro"]},
    "churned": {"allowed": [0, 1]},
}


def check_row(row, schema):
    problems = []
    for column, rule in schema.items():
        value = row.get(column)
        if value is None:
            problems.append(f"{column}: missing")
        elif "allowed" in rule:
            if value not in rule["allowed"]:
                problems.append(f"{column}: {value!r} is not allowed")
        elif not isinstance(value, (int, float)):
            problems.append(f"{column}: {value!r} is not a number")
        elif not rule["min"] <= value <= rule["max"]:
            problems.append(f"{column}: {value} is out of range")
    return problems


row = make_customers(1)[0]
print("clean row:", check_row(row, SCHEMA))
bad = {**row, "tenure": -3, "monthly_fee": "29.90", "usage_hours": None, "plan": "PRO"}
for problem in check_row(bad, SCHEMA):
    print(problem)
```

```text
clean row: []
tenure: -3 is out of range
monthly_fee: '29.90' is not a number
usage_hours: missing
plan: 'PRO' is not allowed
```

`check_row` her sütuna dört soruyu sırayla soruyor:

1. **Değer var mı?** `row.get(column)` sütun hiç yoksa da `None` verir;
   eksik sütun ile boş değer aynı yere düşer.
2. **İzin verilen değerlerden biri mi?** Yalnızca `allowed` kuralı olan
   sütunlarda.
3. **Sayı mı?** `"29.90"` tırnaklı, yani metin; sayı gibi görünse de
   sayı değil. `isinstance(value, (int, float))` değerin bu iki türden
   biri olup olmadığını soruyor.
4. **Aralıkta mı?** `min <= value <= max`.

Temiz satır boş liste veriyor: hiçbir sorun yok. `{value!r}` değeri
`repr` biçiminde yazıyor, yani metni tırnaklarıyla: çıktıda `'PRO'`yu
görünce bunun bir metin olduğunu anlıyorsun.

## Bir partiyi denetlemek

Veri satır satır değil **parti** (batch) hâlinde geliyor: bu ayın 1000
müşterisi gibi. Bir partide hangi sütunda kaç sorun olduğunu sayalım.
Önce bir parti bozalım: her 40 satırdan birinde paket adı büyük harf,
her 25 satırdan birinde kullanım süresi boş.

```python
from collections import Counter

batch = make_customers(1000, seed=21)
for i, row in enumerate(batch):
    if i % 40 == 0:
        row["plan"] = row["plan"].upper()
    if i % 25 == 0:
        row["usage_hours"] = None


def report(rows, schema):
    counts = Counter()
    bad_rows = 0
    for row in rows:
        problems = check_row(row, schema)
        if problems:
            bad_rows += 1
        for problem in problems:
            counts[problem.split(":")[0]] += 1
    return bad_rows, counts


bad_rows, counts = report(batch, SCHEMA)
print("bad rows:", bad_rows, "of", len(batch))
for column, n in counts.most_common():
    print(" ", column, n)
```

```text
bad rows: 60 of 1000
  usage_hours 40
  plan 25
```

Bozuk satır sayısı iki sorunun toplamından az, çünkü bazı satırlarda
ikisi birden var (hem 40'a hem 25'e bölünen sıra numaraları). Rapor,
sorunun **nerede** olduğunu da söylüyor: kullanım süresi ve paket adı.
Veriyi gönderen ekibe götürülecek bilgi tam olarak bu.

## Karantina mı, ret mi?

Sorunlu satırları bulduk. Şimdi ne yapacağız? İki yol var:

- **Karantina** (quarantine): bozuk satırları ayır, incelemek için
  sakla, sağlam satırlarla devam et. Arada bir yanlış girilmiş birkaç
  satır için doğru seçim.
- **Ret** (reject): partinin tamamını geri çevir. Bozuk satırların payı
  büyükse bir şey sistemli olarak bozulmuştur; kuralların yakalamadığı
  başka hatalar da olabilir. O partiyle eğitmek riskli.

İkisini birleştiren bir **kapı** (gate) yazalım: bozuk satırları
karantinaya al, ama payları sınırı geçerse partiyi reddet.

```python
def gate(rows, schema, max_bad_share=0.05):
    good, quarantine = [], []
    for row in rows:
        if check_row(row, schema):
            quarantine.append(row)
        else:
            good.append(row)
    share = len(quarantine) / len(rows)
    if share > max_bad_share:
        raise ValueError(f"batch rejected: {share:.1%} of the rows are bad")
    return good, quarantine


try:
    gate(batch, SCHEMA)
except ValueError as error:
    print(error)

small = make_customers(1000, seed=22)
small[10]["tenure"] = 0
small[20]["plan"] = "gold"
good, quarantine = gate(small, SCHEMA)
print("accepted:", len(good), "quarantined:", len(quarantine))
```

```text
batch rejected: 6.0% of the rows are bad
accepted: 998 quarantined: 2
```

Birinci partide bozuk satırların payı sınırı geçti ve kapı **hata
fırlattı** (`raise`). Bu bilerek yapılıyor: eğitim betiği kapıdan sonra
devam edemez, betik hata koduyla biter ve CI/CD ve DevOps modülünde
gördüğün gibi hat kırmızıya döner. İkinci partide yalnızca iki satır
bozuk; onlar karantinaya alındı, kalan satırlarla eğitim sürebilir.

`if check_row(row, schema):` boş olmayan bir listeyi `True` sayar: en az
bir sorun varsa satır karantinaya gider.

## Kuralların göremediği bozulma

Kurallar tek tek değerlere bakıyor. Ya her değer kendi başına geçerli
ama veri yine de yanlışsa? Diyelim ki destek kayıtlarını tutan sistem bu
ay bozuldu ve bütün müşterilerin destek araması `0` geldi. `0` geçerli
bir değer; hiçbir kural itiraz etmez. Ama ölçünce bu da modeli
bozuyor: aynı biçimde bozulmuş 2000 müşteriyle eğitilen modelin
doğruluğu 0,744 (temiz veriyle 0,79).

Bunu yakalamak için tek tek değerlere değil, sütunun **bütününe**
bakarız. Eğitim verisinden bir **profil** (profile) çıkarırız: her
sayısal sütunun ortalaması ve standart sapması. Yeni partinin
ortalaması eğitimdekinden ne kadar uzaklaşmış, onu ölçeriz. Uzaklığı
standart sapma cinsinden yazınca bütün sütunlar aynı ölçekle
karşılaştırılabilir:

```python
import statistics


def profile(rows, columns):
    result = {}
    for column in columns:
        values = [row[column] for row in rows if row[column] is not None]
        result[column] = {"mean": statistics.mean(values),
                          "std": statistics.pstdev(values)}
    return result


def compare(reference, rows, columns, limit=0.5):
    new = profile(rows, columns)
    for column in columns:
        old = reference[column]
        shift = abs(new[column]["mean"] - old["mean"]) / old["std"]
        status = "CHECK" if shift > limit else "ok"
        print(f"{column:14} {shift:.2f}  {status}")


reference = profile(make_customers(2000), NUMERIC)
print("normal batch")
compare(reference, make_customers(1000, seed=21), NUMERIC)
lost = make_customers(1000, seed=21)
for row in lost:
    row["support_calls"] = 0
print("calls lost")
compare(reference, lost, NUMERIC)
print("bad rows by the rules:", report(lost, SCHEMA)[0])
```

```text
normal batch
tenure         0.01  ok
monthly_fee    0.02  ok
support_calls  0.01  ok
usage_hours    0.02  ok
calls lost
tenure         0.01  ok
monthly_fee    0.02  ok
support_calls  0.68  CHECK
usage_hours    0.02  ok
bad rows by the rules: 0
```

Normal partide bütün kaymalar çok küçük: aynı müşteri kitlesinden
gelen başka bir parti. Destek aramaları kaybolan partide ise
`support_calls` sütunu 0,68 standart sapma kaymış ve
işaretlenmiş. Aynı partide kurallar **tek bir** bozuk satır bile
bulmadı. İki denetim birbirini tamamlıyor:

- **Kurallar** tek tek değerlerdeki hataları yakalar: eksik, yanlış tür,
  aralık dışı, izin verilmeyen değer.
- **Profil karşılaştırması** sütunun bütünündeki değişimi yakalar: her
  değer geçerli ama dağılım yanlış.

Profil karşılaştırması bir uyarıdır, kesin hüküm değil: müşteriler
gerçekten değişmiş de olabilir. "CHECK" bir insanın bakması gerektiğini
söyler. Yayından sonra verinin zamanla değişmesini Veri Kayması
bölümünde daha sağlam yöntemlerle ölçeceğiz.

## Hattaki yeri

Doğrulama eğitimden önce, hattın ayrı bir adımı olarak çalışır:

<figure class="fig">
  <div class="flow">
    <span class="node">Yeni veri</span>
    <span class="arrow">→</span>
    <span class="node acc">Kural denetimi</span>
    <span class="arrow">→</span>
    <span class="node acc">Profil karşılaştırması</span>
    <span class="arrow">→</span>
    <span class="node">Eğitim</span>
    <span class="arrow">→</span>
    <span class="node">Değerlendirme</span>
  </div>
  <figcaption>Kapı geçilmezse eğitim hiç başlamaz.</figcaption>
</figure>

Aynı kurallar **tahmin anında** da işe yarar: modele gelen bir istekte
paket adı `"PRO"` ise sessizce yanlış bir tahmin vermek yerine açık bir
hata döndürmek daha iyidir. FastAPI ile REST API Yazmak modülünde Pydantic'in hatalı
isteği `422` ile geri çevirmesi aynı fikir. Eğitimdeki ve tahmindeki
denetimlerin aynı olması önemli; Eğitim-Sunma Farkı bölümünde buna
döneceğiz.

## Kurallar nereden gelir?

Şemadaki sayıları iki yerden bulursun:

- **Alan bilgisi:** Hizmet en fazla 72 ay önce başladıysa abonelik
  süresi 72'yi geçemez. Paket yalnızca `basic` ya da `pro` olabilir. Bu
  kurallar veriyi gönderen ekiple birlikte yazılır; sözleşme kelimesi
  buradan geliyor.
- **Referans veri:** Güvenilen eğitim verisindeki en küçük ve en büyük
  değerler, görülen kategoriler. Bu yol hızlıdır ama dar kalabilir:
  eğitimde en yüksek ücret 58 ise 60 ödeyen gerçek bir müşteri
  reddedilir. Bu yüzden çıkarılan aralığa pay bırakılır ve kurallar bir
  insanın gözünden geçer.

Gerçek projelerde bu işi kolaylaştıran kütüphaneler var (pandera, Great
Expectations gibi): şemayı yazarsın, tablo her partide denetlenir. Fikir
bu bölümde yazdığımızın aynısı.

## Özet

- Veri hatası çoğu zaman **kodu durdurmaz**, yalnızca modeli kötüleştirir.
  Bu yüzden veri eğitimden önce denetlenir.
- **Şema** (veri sözleşmesi) her sütunun kuralını yazar: aralık, izin
  verilen değerler, eksik olmaması.
- Bir partide sorunlar sütun sütun sayılır; rapor sorunun nerede
  olduğunu söyler.
- Az sayıda bozuk satır **karantinaya** alınır; bozuk satırların payı
  büyükse parti **reddedilir** ve hat durur.
- Her değer geçerliyken dağılım bozulmuş olabilir: yeni partinin
  **profilini** eğitim verisininkiyle karşılaştır.
- Kurallar alan bilgisinden ve referans veriden gelir; çıkarılan
  aralıklara pay bırakılır.
