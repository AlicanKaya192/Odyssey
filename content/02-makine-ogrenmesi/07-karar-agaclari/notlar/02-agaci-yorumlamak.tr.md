Karar ağacının en çok övülen yanı **okunabilir** olması. Bu doğru, ama
okunabilir olmak ile doğru okunmak aynı şey değil. Bu not ikincisiyle
ilgili.

## Bir düğümü okumak

```
visits <= 18.5
gini = 0.425
samples = 150
value = [104, 46]
class = stays
```

| Satır | Cümleye çevirisi |
|---|---|
| `visits <= 18.5` | "Ayda 18.5'ten az mı giriyor?" |
| `samples = 150` | Bu düğüme 150 kayıt düşmüş |
| `value = [104, 46]` | 104'ü kalıyor, 46'sı ayrılıyor |
| `gini = 0.425` | Karışıklık orta düzeyde |
| `class = stays` | Çoğunluk "kalıyor" |

**`samples` en çok atlanan satır.** Yaprakta 3 kayıt varsa o yaprağın
kuralı üç kişiye bakarak kurulmuş demektir; genellenebilir bir bilgi
taşımıyor olabilir.

Kural okurken her zaman "kaç kayda dayanıyor" diye bakılıyor.

## Aynı etiketi veren iki yaprak

Bazen bir bölünme iki tarafta da aynı sınıfı veriyor:

```
|--- income <= 41500 --> class: 0    (samples 20, value [11, 9])
|--- income >  41500 --> class: 0    (samples 75, value [74, 1])
```

Bölünme etiketi değiştirmiyor. Ağaç neden bölmüş?

Çünkü ağaç **etiketi değil safsızlığı** en iyiliyor. Sol yaprak 11'e 9
(gini 0.495, neredeyse en karışık), sağ yaprak 74'e 1 (gini 0.026,
neredeyse saf). Çoğunlukları aynı ama **güven düzeyleri** bambaşka.

Bu fark `predict_proba` çağırınca ortaya çıkıyor:

```python
model.predict_proba(X_test)
```

Sol yaprağa düşen bir kayıt için %55, sağ yaprağa düşen için %99.

**Pratik sonucu:** yalnızca `predict` kullanıp `predict_proba`'ya bakmayan
biri bu iki kaydı aynı sayıyor. Eşik ayarı (bölüm 03) tam olarak bu farkı
kullanıyor.

## Özellik önemi: üç tuzak

### 1. Önem sebep demek değil

`visits` en önemli sütun çıktı diye "müşterileri daha çok girmeye teşvik
edersek ayrılmazlar" sonucu çıkmıyor. Model birlikte değişimi görüyor,
sebebi değil.

Belki az giren müşteriler zaten ayrılmaya karar vermiş olanlar. O durumda
ziyaret sayısı bir **sonuç**, sebep değil.

### 2. İlişkili sütunlar önemi paylaşıyor

İki sütun neredeyse aynıysa (metrekare ve oda sayısı gibi) ağaç birini
seçiyor; öteki sıfıra yakın önem alıyor.

Yanlış sonuç: "oda sayısı fiyatı etkilemiyor." Doğrusu: "metrekare zaten
aynı bilgiyi taşıdığı için ağaç ona ihtiyaç duymadı."

Kontrol yolu: sütunları teker teker çıkarıp modelin ne kadar kötüleştiğine
bakmak.

### 3. Çok değerli sütunlar şişiyor

Sürekli bir sayısal sütunda binlerce olası eşik var; iki kategorili bir
sütunda tek bir eşik. Ağaç ilkinde tesadüfen iyi bir bölünme bulmakta daha
şanslı.

Uç örneği: veriye **müşteri numarası** koyarsan ağaç onunla her kaydı
ayırabiliyor ve o sütun en önemli görünüyor. Oysa hiçbir bilgi taşımıyor.

**Kimlik, sıra numarası, tarih damgası gibi sütunlar modele girmeden
çıkarılıyor.**

## Daha güvenilir bir ölçü

`feature_importances_` yerine **permütasyon önemi** kullanılabiliyor:

```python
from sklearn.inspection import permutation_importance

result = permutation_importance(model, X_test, y_test,
                                n_repeats=10, random_state=42)

for name, value in zip(X.columns, result.importances_mean):
    print(name, round(float(value), 3))
```

Yaptığı iş basit: bir sütunun değerlerini **karıştırıyor** ve modelin skoru
ne kadar düştüğüne bakıyor. Çok düşüyorsa o sütun gerçekten kullanılıyor.

İki üstünlüğü var:

- **Test kümesinde ölçülebiliyor**, yani gerçekten genelleşen bilgiyi
  gösteriyor.
- **Çok değerli sütunlar şişmiyor**, çünkü ölçüm bölünme sayısına değil
  skora bakıyor.

Bir sınırı da var: ilişkili sütunlarda hâlâ yanıltıyor. Biri karıştırılsa
bile öteki aynı bilgiyi taşıdığı için skor düşmüyor ve ikisi de "önemsiz"
görünüyor.

## Kararsızlık

Aynı veriden birkaç satır çıkarıp ağacı yeniden eğitirsen **kök bölünmesi
bile değişebiliyor.**

Sebebi açgözlülük: ilk bölünme iki aday arasında kıl payı karar veriyor ve
o karar değişince altındaki bütün ağaç yeniden şekilleniyor.

**Bunun iki sonucu var:**

- Tek bir ağacın kurallarını "keşfedilmiş gerçek" gibi sunmak yanlış.
  Yarın başka bir ağaç başka kurallar verebilir.
- Özellik önemi de kararsız: bugün `visits`, on satır sonra `income` en
  önemli çıkabiliyor.

Kararlılığı ölçmenin yolu var: farklı `random_state` ya da farklı alt
örneklerle birkaç ağaç eğitip kök bölünmesinin değişip değişmediğine
bakmak.

**Çözüm topluluk yöntemleri:** çok sayıda ağacın ortalaması, tek bir ağacın
kararsızlığını söndürüyor. Bir sonraki bölümün konusu.

## Kuralı sunarken

Ağaç kuralları paydaşlara anlatılabiliyor ve bu büyük bir avantaj. Ama
sunarken üç şey birlikte söyleniyor:

| Söylenen | Neden |
|---|---|
| Kural | "18'den az giren ve geliri düşük olanlar ayrılıyor" |
| Kaç kayda dayandığı | `samples` — 5 kayıtlık kural genellenemez |
| Ne kadar kesin olduğu | `value` dağılımı — 11'e 9 ile 74'e 1 aynı şey değil |

Yalnızca kuralı söylemek, güven düzeyi ve dayanak sayısı olmadan yanıltıcı.

Ve her zaman: **bu bir kural, bir sebep açıklaması değil.**
