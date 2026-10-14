# Güvenlik, Önyargı ve Sorumluluk

Üretken modeller veriden öğrenir; verideki adaletsizliği, kişisel bilgiyi
ve hatayı da öğrenir. Bu bölüm üç riski ölçerek ele alıyor: **önyargı**
(model bir grubu sistemli olarak dezavantajlı bırakıyor mu?), **kişisel
veri** (metinde kimlik bilgisi sızıyor mu?) ve **sorumluluk** (sistemi
kim, nasıl denetliyor?). Prompt üzerinden yapılan saldırılar (prompt
injection) Modül 2'nin konusu.

## Önyargı veriden gelir

Bir şirket geçmiş işe alım kararlarıyla bir aday eleme modeli eğitmek
istiyor. Yapay bir veri kuralım: adayların gerçek yeteneği (`skill`), bundan
gürültülü ölçülen deneyimi, bir grup bilgisi (A ya da B) ve grupla güçlü
ilişkili bir özellik: bir kulübe üyelik (B grubunda %80, A'da %20). Bir aday
yeteneği belli bir eşiği geçiyorsa **gerçekten uygun**. Ama geçmiş kararlar
B grubuna karşı yanlı verilmiş:

```python
import numpy as np
from sklearn.linear_model import LogisticRegression


def make_applicants(n, seed):
    rng = np.random.default_rng(seed)
    group = rng.integers(0, 2, n)
    skill = rng.normal(0, 1, n)
    club = (rng.random(n) < np.where(group == 1, 0.8, 0.2)).astype(int)
    experience = skill + rng.normal(0, 0.8, n)
    suitable = (skill > 0.3).astype(int)
    noise = rng.normal(0, 0.5, n)
    hired = (skill - 0.8 * group + noise > 0.3).astype(int)
    X = np.column_stack([experience, club, group])
    return X, group, suitable, hired


X, group, suitable, hired = make_applicants(4000, 0)
X_test, g_test, s_test, _ = make_applicants(4000, 1)
for k, name in [(0, "A"), (1, "B")]:
    print(name, "suitable", suitable[group == k].mean().round(2),
          "hired in the past", hired[group == k].mean().round(2))
```

```text
A suitable 0.37 hired in the past 0.37
B suitable 0.4 hired in the past 0.17
```

İki grupta uygun aday oranı yakın (%37 ve %40); geçmişte işe alınma oranı
ise B'de A'nın yarısından az. Modeli bu geçmiş kararlarla eğitirsek ne öğrenir?

## Grubu çıkarmak yetmez

Üç model eğitiyoruz: bütün özelliklerle, grup sütunu çıkarılmış olarak ve
yalnızca deneyimle. Her birinde iki şeye bakıyoruz: her grubun **seçilme
oranı** ve **gerçekten uygun adayların** seçilme oranı (fırsat eşitliği,
equal opportunity).

```python
def report(name, chosen):
    rates = []
    for k in (0, 1):
        sel = chosen[g_test == k].mean()
        fair = chosen[(g_test == k) & (s_test == 1)].mean()
        rates.append(f"{sel:.2f}/{fair:.2f}")
    print(f"{name:16} A {rates[0]}  B {rates[1]}")


for name, cols in [("all features", [0, 1, 2]),
                   ("without group", [0, 1]),
                   ("experience only", [0])]:
    model = LogisticRegression().fit(X[:, cols], hired)
    report(name, model.predict(X_test[:, cols]))
```

```text
all features     A 0.33/0.67  B 0.10/0.24
without group    A 0.24/0.52  B 0.15/0.35
experience only  A 0.17/0.40  B 0.18/0.41
```

Bütün özelliklerle eğitilen model geçmişin önyargısını öğreniyor: uygun
adayların A'da %67'si, B'de %24'ü seçiliyor. Grup sütunu çıkarılınca fark
küçülüyor ama kapanmıyor (%52'ye %35): kulüp üyeliği grubu ele veriyor ve
model önyargıyı onun üzerinden sürdürüyor. Böyle bir özelliğe **vekil
değişken** (proxy) denir. Yalnızca deneyimle fark kapanıyor (%40'a %41);
ama A grubunda uygun adayların seçilme oranı %52'den %40'a iniyor: modelin
bilgisi azaldı ve etiketler hâlâ yanlı geçmişten geliyor. Gerçek veride
vekiller her zaman bu kadar görünür değildir (adres, okul, boşluk yılları).

## Bir düzeltme ve bedeli

Bir yol, B grubu için eşiği, iki grupta uygun adayların seçilme oranı
eşitlenecek kadar düşürmek. Grup bilgisi modele girmiyor ama karar
aşamasında kullanılıyor:

```python
model = LogisticRegression().fit(X[:, [0, 1]], hired)
p = model.predict_proba(X_test[:, [0, 1]])[:, 1]
target = (p >= 0.5)[(g_test == 0) & (s_test == 1)].mean()
best = min(np.arange(0.20, 0.51, 0.01), key=lambda t: abs(
    (p >= t)[(g_test == 1) & (s_test == 1)].mean() - target))
print("threshold for B", round(best, 2))
report("adjusted", (p >= np.where(g_test == 1, best, 0.5)).astype(int))
```

```text
threshold for B 0.35
adjusted         A 0.24/0.52  B 0.24/0.53
```

B için eşik 0,35'e inince uygun adayların seçilme oranı iki grupta
eşitleniyor (%52 ve %53). Bedeli: B grubunun genel seçilme oranı %15'ten
%24'e çıkıyor ve iki grup artık farklı eşiklerle değerlendiriliyor. Bu bir
teknik ayar gibi görünse de bir **politika kararıdır**: hangi adalet
ölçüsünün (eşit seçilme oranı, eşit fırsat…) seçileceği teknik değil,
kurumsal ve hukuki bir karardır; gruba göre farklı karar kuralı bazı hukuk
düzenlerinde tartışmalı ya da yasaktır. Asıl çözüm çoğu zaman veridedir:
yanlı etiketleri düzeltmek ve eksik kalan grupları toplamak.

## Kişisel veriyi maskelemek

Destek talepleri, belgeler ve sohbet geçmişi e-posta adresi, telefon
numarası gibi **kişisel veri** taşır. Bu veri modele (ya da kayıtlara)
gitmeden önce maskelenebilir. Düzenli ifadelerle basit bir maskeleyici
yazıp örnek cümlelerde deneyelim:

```python
import re

PATTERNS = {
    "EMAIL": r"[\w.+-]+@[\w-]+\.[\w.]+",
    "PHONE": r"\+?\d[\d\s()-]{8,}\d",
    "ORDER": r"ORD-\d{5}",
}


def mask(text):
    for label, pattern in PATTERNS.items():
        text = re.sub(pattern, f"[{label}]", text)
    return text


SAMPLES = [
    "Please email me at ana.k@example.com about ORD-48213.",
    "Call me on +90 532 123 45 67 tomorrow.",
    "My number is (555) 123-4567.",
    "Write to ana dot k at example dot com.",
    "Order ORD-48213 arrived but the box was empty.",
]
for text in SAMPLES:
    print(mask(text))
```

```text
Please email me at [EMAIL] about [ORDER].
Call me on [PHONE] tomorrow.
My number is ([PHONE].
Write to ana dot k at example dot com.
Order [ORDER] arrived but the box was empty.
```

E-posta, sipariş numarası ve uluslararası biçimdeki telefon maskelendi.
Ama iki açık var: parantezli numarada ilk parantez dışarıda kaldı
("([PHONE]."), harflerle yazılmış e-posta ise ("ana dot k at example dot
com") hiç yakalanmadı. Düzenli ifadeler yaygın biçimleri ucuza yakalar,
alışılmadık yazımları kaçırır. Maskeleyici de bir denetçi gibi örnek
cümlelerle ölçülür (08) ve kaçırdığı biçimler listelenir.

## Sorumluluk: kontrol listesi

Teknik önlemler tek başına yetmez; bir sistemi kimin, nasıl denetlediği
de tasarımın parçasıdır:

- **Ölç ve yaz:** gruplara göre başarıyı ölç, sonuçları ve bilinen
  sınırları belgele.
- **İnsan döngüde kalsın:** işe alım, kredi, sağlık gibi kişiyi etkileyen
  kararlarda son söz insanın; model öneri verir.
- **Şeffaf ol:** kullanıcıya bir model ile konuştuğunu ve modelin hata
  yapabileceğini söyle.
- **Az veri:** göreve gerekmeyen kişisel veriyi hiç toplama; gerekeni
  maskele, saklama süresini sınırla.
- **Kayıt tut ve geri bildirim al:** hatalı ya da zararlı çıktılar
  bildirilebilsin, incelensin.

## Özet

- Model, geçmiş kararlardaki önyargıyı öğrenir; bölümde uygun adayların B
  grubunda seçilme oranı A'nın üçte biri kadardı.
- Grup sütununu çıkarmak yetmedi: grupla ilişkili bir özellik (kulüp)
  önyargıyı taşıdı.
- Düzeltmelerin bedeli var: grup başına eşik fırsatı eşitledi ama seçilme
  oranlarını değiştirdi; bu bir teknik değil kurumsal ve hukuki karardır.
- Kişisel veri maskelemesi düzenli ifadelerle ucuzdur ama alışılmadık
  yazımları kaçırır; ölçülerek kullanılır.
- Sorumluluk tasarımın parçasıdır: ölç, belgele, insanı döngüde tut.
