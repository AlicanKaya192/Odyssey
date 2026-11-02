# Deney Sorusu ve Metrik Seçimi

İstatistiksel Çıkarım modülü bir A/B testinin sonucunu okumayı öğretti. Bu
modül testi **kurmayı** anlatıyor. Kurulum, sonuçtan önce başlar: ne
soruyoruz, neyi ölçeceğiz, ne olursa "işe yaradı" diyeceğiz? Bu soruların
cevabı test başlamadan yazılmazsa en doğru analiz bile yanlış soruya
cevap verir.

## Soru, değişiklik, metrik

Bir deney sorusu üç parçadan oluşur:

- **Değişiklik:** neyi değiştiriyoruz? ("Ödeme düğmesi sayfanın üstüne
  taşınacak.")
- **Beklenen etki ve gerekçe:** neden işe yarasın? ("Mobilde düğme
  görünmüyor, kişiler sepeti terk ediyor.")
- **Metrik ve eşik:** neye bakacağız, ne kadarı yeter? ("Satın alma oranı
  en az 0,5 puan artarsa.")

<figure class="fig">
  <div class="versus">
    <div class="no"><h4>Belirsiz soru</h4>"Yeni tasarım daha iyi mi?" İyi ne demek, neye bakılacak, ne kadar fark yeter? Sonuçtan sonra her metrik "iyi" diye seçilebilir.</div>
    <div class="ok"><h4>Sınanabilir soru</h4>"Düğmeyi üste taşımak, kullanıcı başına satın alma oranını en az 0,5 puan artırır mı?" Metrik, birim ve eşik baştan yazılı.</div>
  </div>
  <figcaption>Sınanabilir bir soru, sonuç gelmeden önce hangi sayının ne olursa kararı değiştireceğini söyler.</figcaption>
</figure>

## Veri: bir mağazanın iki haftası

Bu modülde çoğunlukla bir mağazanın deneyden önceki kullanıcı kaydıyla
çalışacağız. Her satır bir kullanıcı:

```python
from ab_data import make_user_log

users = make_user_log()
print(users.shape)
print(users.head(3).to_string(index=False))
```

```text
(20000, 7)
user_id platform  sessions  minutes  bought  revenue  refunded
 U00001  desktop         2      6.7       0      0.0         0
 U00002   mobile         4     25.0       0      0.0         0
 U00003  desktop         3     12.7       0      0.0         0
```

- `sessions`: ziyaret sayısı, `minutes`: toplam süre,
- `bought`: satın aldı mı (0/1), `revenue`: harcadığı tutar,
- `refunded`: iade etti mi (yalnızca alıcılar iade edebilir).

## Aday metrikler

Kullanıcı başına ortalamalar:

```python
for col in ["sessions", "minutes", "bought", "revenue"]:
    print(col, round(users[col].mean(), 3))
buyers = users[users["bought"] == 1]
print("refund rate", round(buyers["refunded"].mean(), 3))
```

```text
sessions 3.753
minutes 21.096
bought 0.117
revenue 11.413
refund rate 0.08
```

Metrikler üç türdendir:

- **Oran** (proportion): evet/hayır sorusu, `bought` gibi. Kullanıcıların
  %11,7 kadarı satın almış.
- **Ortalama:** sürekli bir değer, `revenue` ya da `minutes` gibi.
- **Oran metriği** (ratio metric): iki toplamın oranı, "sipariş başına
  tutar" ya da "iade oranı" gibi. Paydası kullanıcı sayısı olmadığı için
  özel bir hesap ister; Oran Metrikleri ve Delta Yöntemi bölümünde
  göreceğiz.

## İyi bir metrik iki şeyi birden yapar

**Anlamlı olmalı:** işin amacına bağlanmalı. Sayfada geçen süre artınca iyi
mi olur? Kişi aradığını bulamayıp dolaşıyorsa süre artar ama işler
kötüleşir. Süre tek başına iyi bir hedef değildir.

**Duyarlı olmalı:** gerçek bir değişikliği gürültünün içinden çıkarabilmeli.
Gürültüyü kabaca **değişim katsayısı** (coefficient of variation) gösterir:
standart sapmanın ortalamaya oranı.

```python
for col in ["sessions", "minutes", "bought", "revenue"]:
    x = users[col]
    print(col, round(x.std() / x.mean(), 2))
```

```text
sessions 0.82
minutes 1.1
bought 2.74
revenue 4.32
```

Gelirin değişim katsayısı en büyük: çoğu kişi hiç harcamıyor, birkaç kişi
çok harcıyor. Etki Büyüklüğü bölümünden biliyoruz ki aynı **göreli** artışı
görmek için gereken örneklem, sapma ortalamaya göre büyüdükçe karesiyle
artar. Bu yüzden gelir işin en önemli metriği olsa da en "pahalı"
olanıdır; Örneklem Büyüklüğü bölümünde bunu sayıyla göreceğiz.

## Birincil metrik, ikincil metrikler, koruma metrikleri

- **Birincil metrik** (primary metric): kararı veren tek metrik, önceden
  seçilir. Birden çok "birincil" metrik, Çoklu Karşılaştırma bölümündeki
  yanlış alarm sorununu geri getirir.
- **İkincil metrikler:** nedeni anlamaya yardım eder ("satın alma arttı,
  çünkü sepete ekleme arttı").
- **Koruma metrikleri** (guardrail metrics): bozulmaması gereken şeyler.
  Satın alma artarken iade oranı, sayfa açılış süresi ya da hata oranı
  kötüleşiyorsa değişiklik yine de reddedilebilir.

İade oranı bu veride alıcıların %8 kadarı. Paydası alıcılar:
"kullanıcı başına iade" ile karıştırılmamalı.

## Kitle farklıysa metrik de farklıdır

Aynı metrik farklı gruplarda çok farklı olabilir:

```python
print(users.groupby("platform")["bought"].mean().round(4))
```

```text
platform
desktop    0.1290
mobile     0.1098
Name: bought, dtype: float64
```

Masaüstünde satın alma oranı mobilden yüksek. Bir deneyin trafiği bir
gruba kayarsa, değişiklik hiçbir şey yapmasa bile ortalama değişir.
Rastgele atama bunun önüne geçer; A/A testi ve SRM bölümünde bu kaymanın
nasıl yakalandığını göreceğiz.

## Deney planı (ön kayıt)

Test başlamadan tek sayfalık bir plan yazılır:

1. Soru ve gerekçe.
2. Birincil metrik, birimi (kullanıcı başına) ve beklenen yön.
3. En küçük anlamlı etki (MDE) ve pratik eşik.
4. Koruma metrikleri ve sınırları.
5. Örneklem büyüklüğü, süre, atama oranı.
6. Kullanılacak test ve α.

Bu plan, sonuca bakıp metrik, eşik ya da süre değiştirmeyi engeller.

## Özet

- Deney sorusu değişikliği, gerekçeyi, metriği ve eşiği birlikte söyler.
- Metrikler oran, ortalama ya da oran metriği olabilir.
- İyi metrik hem işe bağlıdır hem de duyarlıdır; gelir önemli ama gürültülü.
- Tek birincil metrik, ayrıca ikincil ve koruma metrikleri seçilir.
- Plan test başlamadan yazılır.
