# Genel Tekrar

MLOps ve ML Sistem Tasarımı modülünün sonuna geldin. Defterde iyi ölçülen
bir modelin neden yalnızca başlangıç olduğuyla başladık; eğitimi
tekrarlanabilir yaptık, veriyi denetledik, veriyi ve modeli sürümledik.
Sonra deneyleri, kaydı ve kapıyı kurduk; modeli sunduk ve canlıda izledik.
Zamanla gelen değişimi (veri ve kavram kayması) ölçtük, yeni modeli
dikkatle canlıya aldık. En sonda ölçeklenmeyi, tasarımı ve bütün hattı
gördük. Bu bölüm yolu bir kez daha yürüyor.

<figure class="fig">
  <div class="flow">
    <span class="node">Temeller</span>
    <span class="arrow">→</span>
    <span class="node">Deneyden kayda</span>
    <span class="arrow">→</span>
    <span class="node">Canlıda</span>
    <span class="arrow">→</span>
    <span class="node">Zamanla</span>
    <span class="arrow">→</span>
    <span class="node acc">Sistem</span>
  </div>
  <figcaption>Modülün yolu: tekrarla, kaydet, sun, izle, tasarla.</figcaption>
</figure>

## 1. Temeller (Bölüm 0–3)

- **MLOps** DevOps'un fikirlerini ML sistemlerine uygular; davranış
  koddan **ve** veriden gelir. Yaşam döngüsü: veri → eğit → değerlendir →
  sun → izle (0).
- **Tekrarlanabilirlik:** rastgelelik tohumdan gelir; her rastgele adıma
  ayrı tohum, ayarlar tek yapılandırmada, verinin parmak izi ve kütüphane
  sürümleri eğitim kaydında (1).
- **Veri doğrulama:** veri hatası kodu durdurmaz, modeli bozar. Şema,
  karantina ya da ret, profil karşılaştırması (2).
- **Sürümleme:** büyük dosya Git'e değil içerik adresli depoya; Git'e
  işaret dosyası; soy kaydı modeli verisine bağlar (3).

## 2. Deneyden kayda (Bölüm 4–6)

- **Deney takibi:** her deney kendiliğinden kayda; temel çizgi; seçim
  doğrulamada, rapor testte bir kez; kazananın laneti (4).
- **Model kaydı:** değişmeyen sürüm numaraları, canlıyı gösteren etiket,
  kapı (`min_gain`), geri dönüş etiketi çevirmek, model kartı (5).
- **ML için CI:** özellik testleri, kalite kapısı (alt sınır, temel
  çizgiye pay, dilimler), davranış testleri; ölçümler her durumda
  saklanır (6).

## 3. Canlıda (Bölüm 7–9)

- **Sunma:** model bir kez yüklenir; toplu ya da anlık; cevapta model
  sürümü; hız p50 ve p95 ile (7).
- **Eğitim-sunma farkı:** hata çıkmaz, tahmin bozulur. Özellik kodu tek
  yerde; her özellik tahmin anı itibarıyla; özellik deposu (8).
- **İzleme:** üç katman (sistem, veri ve tahmin, model kalitesi); her
  tahmin kaydedilir; uyarı üst üste aşılmayla (9).

## 4. Zamanla (Bölüm 10–12)

- **Veri kayması:** PSI (0,1 / 0,25), KS; önce gürültü; p-değeri büyük
  örneklemde yanıltır; her kayma zarar vermez (10).
- **Kavram kayması:** ilişki değişir, etiketsiz görülmez; kalibrasyon
  bozulur; son pencere; kapı güncel kümeyle (11).
- **Gölge, kanarya, A/B:** gölge risksiz; kanarya kimlikten kovayla, aşama
  başına en az müşteri; A/B'den önce A/A gürültüsü (12).

## 5. Sistem (Bölüm 13–15)

- **Ölçeklenme:** doluluk %100'e yaklaşınca bekleme patlar; yatay
  ölçeklenme durumsuz sunucu ister; önbellek anahtarı müşteri + model
  sürümü; model boyu gecikmeyle tartılır (13).
- **Tasarım:** önce hedef ve iş ölçüsü; eşik ölçüye göre; yedek plan
  önceden yazılır ve sınanır (14).
- **Bitirme:** izle → tetikle → doğrula → eğit → kapı, her ay; kayma tek
  başına model değiştirmez, kapı tek başına yetmez (15).

## Hepsi birlikte: bir yayını denetlemek

Modülün kurallarını kullanarak bir model yayınının kaydını okuyup
sorunlarını listeleyen küçük bir denetçi yazalım. Aşağıdaki kayıtta bu
modülde gördüğümüz sekiz sorun var:

```python
release = {
    "version": 4,
    "seed": None,
    "data_digest": "",
    "trained_month": 5,
    "gate_month": 0,
    "gain": 0.001,
    "threshold": 0.5,
    "fallback": None,
    "monitors": ["accuracy"],
}


def audit(release, min_gain=0.003):
    problems = []
    if release["seed"] is None:
        problems.append("no fixed seed: training can't be repeated")
    if not release["data_digest"]:
        problems.append("no data digest: the data can't be traced")
    if release["gate_month"] < release["trained_month"]:
        problems.append("gate set is older than the training data")
    if release["gain"] < min_gain:
        problems.append(f"gain {release['gain']} is below {min_gain}")
    if release["threshold"] == 0.5:
        problems.append("threshold left at the default 0.5")
    if release["fallback"] is None:
        problems.append("no fallback")
    for needed in ["drift", "calibration"]:
        if needed not in release["monitors"]:
            problems.append(f"{needed} is not monitored")
    return problems


for problem in audit(release):
    print(problem)
```

```text
no fixed seed: training can't be repeated
no data digest: the data can't be traced
gate set is older than the training data
gain 0.001 is below 0.003
threshold left at the default 0.5
no fallback
drift is not monitored
calibration is not monitored
```

Her satır bir bölüme dayanıyor: tohum (1), veri özeti (1 ve 3), eski kapı
kümesi (11), kapıdaki pay (5), varsayılan eşik (14), yedek plan (14),
kayma (10) ve kalibrasyon (11) izlemesi. Gerçek ekiplerde bu denetim bir
**yayın kontrol listesidir** ve hattın içinde koşar: listeden geçmeyen
sürüm kayda "canlı" etiketiyle girmez.

## Sonra

Bu modülde her şeyi tek bir bilgisayarda, küçük ve ölçülebilir parçalarla
kurduk: kayıt bir sözlük, depo bir klasör, hat bir fonksiyondu. Gerçek
projelerde aynı işleri hazır araçlar yapar; ama neye baktıklarını bilmek,
onları doğru kurmanın ve uyarılarını anlamanın tek yolu. Kural aynı:
**ölç, kaydet, kapıdan geçir, izle.**
