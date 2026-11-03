# Genel Tekrar

Deney Tasarımı ve A/B Testi modülünün sonuna geldin. İstatistiksel Çıkarım
modülü bir testin sonucunu **okumayı** öğretmişti; bu modül testi **doğru
kurmayı**, gerçek hayatın tuzaklarını tanımayı ve kararı yazmayı öğretti.
Bu bölüm yolu bir kez daha yürüyor; sonunda bütün kuralları tek bir
fonksiyonda topluyoruz.

<figure class="fig">
  <div class="flow">
    <span class="node">Plan</span><span class="arrow">→</span>
    <span class="node">Atama</span><span class="arrow">→</span>
    <span class="node">Güven</span><span class="arrow">→</span>
    <span class="node">Okuma</span><span class="arrow">→</span>
    <span class="node acc">Karar</span>
  </div>
  <figcaption>Modülün yolu: önce soruyu ve kuralları yaz, rastgele ata, veriye güvenip güvenemeyeceğine bak, sonucu tuzaklara düşmeden oku ve önceden yazılmış kurallarla karar ver.</figcaption>
</figure>

## 1. Plan

| Konu | Akılda kalacak |
|---|---|
| Deney sorusu | tek cümle; bir birincil metrik, koruma metrikleri, pratik eşik |
| Metrik | hassas, değişikliğe yakın, kararla ilişkili; gelir gürültülüdür |
| Örneklem büyüklüğü | n, etkinin karesiyle ters orantılı; en az iki tam hafta |
| Rastgele atama | tuzlu karma: aynı kullanıcı hep aynı grupta, deneyler birbirinden bağımsız |

## 2. Güven

- **A/A testi:** sistem hiçbir fark yokken %5 civarında alarm veriyor mu?
- **SRM:** grup büyüklükleri plana uyuyor mu? Ki-kare p < 0,001 ise önce
  neden bulunur; sonuç okunmaz.
- **Denge:** testten önceki değerler iki grupta aynı mı?

## 3. Okuma

| Soru | Araç |
|---|---|
| İki oran | z-testi, `confint_proportions_2indep` |
| İki ortalama, çarpık veri | Welch ya da bootstrap |
| Formülü olmayan istatistik | bootstrap (atama biriminde) |
| Varsayımsız test | permütasyon |
| Oran metriği (tıklama / gösterim) | delta yöntemi |
| Gürültülü metrik | CUPED (testten önceki değerle) |

## 4. Tuzaklar

| Tuzak | Belirti | Çare |
|---|---|---|
| Sıralı bakma | her gün bakılıp anlamlı olunca durulur | son gün ya da önceden yazılmış ardışık eşikler |
| Çoklu karşılaştırma | 20 metrikte birkaç "anlamlı" | tek birincil metrik; Holm ya da BH |
| Simpson paradoksu | atama oranı zamanla değişti | tabakalı tahmin |
| Segment avı | en çarpıcı segment | önceden yazılmış birkaç segment |
| Yenilik etkisi | etki zamanla söner | uzun test, yeni kullanıcı kohortu, tutma grubu |
| Karışma | B, A'dan alıyor | küme halinde atama |
| Haydut verisi | az seçilen kol yanlı | büyüklük raporlanacaksa A/B testi |

## 5. Karar

Güven aralığı sıfıra ve önceden yazılmış eşiğe göre dört yerden birine
düşer: **uygula**, **zararlı**, **belirsiz**, **değmez**. Belirsiz sonuç
"etki yok" değildir; rapor bir sayfa, aynı sırayla ve sınırlarıyla yazılır.

## Bütün kurallar tek fonksiyonda

```python
from scipy import stats
from statsmodels.stats.proportion import confint_proportions_2indep
from ab_data import make_experiment


def analyse(test, threshold=0.003):
    n = test.groupby("group").size()
    if stats.chisquare(n).pvalue < 0.001:
        return "stop: SRM"
    k = test.groupby("group")["bought"].sum()
    low, high = confint_proportions_2indep(k["B"], n["B"], k["A"], n["A"])
    if high < 0:
        return "harm"
    if low >= threshold:
        return "ship"
    if high < threshold:
        return "not worth it"
    return "inconclusive"


for lift in [0.15, 0.0, -0.15]:
    print(lift, analyse(make_experiment(seed=161, lift=lift)))
```

```text
0.15 ship
0.0 inconclusive
-0.15 harm
```

Gerçek etki %15 iken "uygula", sıfırken "belirsiz", −%15 iken "zararlı".
Fonksiyonun kendisini de sınayalım: hiçbir şeyin değişmediği 200 A/A
testinde ne kadar sık yanlışlıkla "uygula" diyor?

```python
verdicts = [analyse(make_experiment(seed=2000 + s, lift=0.0))
            for s in range(200)]
print({v: verdicts.count(v) for v in sorted(set(verdicts))})
```

```text
{'harm': 3, 'inconclusive': 180, 'not worth it': 16, 'ship': 1}
```

200 A/A testinin 1 tanesinde "uygula" diyor: aralığın alt ucunun
hem sıfırı hem eşiği geçmesi gerektiği için yanlış lansman nadir. Kuralları
önceden yazmanın ve aralığı eşikle okumanın ölçülebilir faydası budur.

## Özet

- Plan testten önce: soru, metrik, eşik, örneklem, bakma kuralı, segment.
- Önce güven (A/A, SRM, denge), sonra okuma.
- Tuzakların her birinin tanınabilir bir belirtisi ve bilinen bir çaresi
  var.
- Karar önceden yazılmış kurallarla verilir; rapor sınırlarıyla yazılır.
