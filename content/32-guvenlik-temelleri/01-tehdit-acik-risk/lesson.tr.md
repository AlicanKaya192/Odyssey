# Tehdit, Açık ve Risk

Güvenlik konuşmalarında dört kelime hep birlikte geçer: **varlık**,
**tehdit**, **açık** ve **risk**. Günlük dilde birbirinin yerine
kullanılırlar ama güvenlikte her biri ayrı bir şeyi anlatır. Bu bölüm o
dört kelimeyi ve onlara verilen cevabı, **önlemi**, birbirinden ayırıyor.

Bir ev düşün. Evdeki eşyalar **varlık**. Mahallede dolaşan bir hırsız
**tehdit**. Kilitlenmeyen bir arka pencere **açık**. Hırsızın o pencereyi
bulup içeri girme ihtimali ve girerse kaybedeceklerin, **risk**. Pencereye
takılan kilit ise bir **önlem**.

## Tehdit

**Tehdit** (threat), bir varlığa zarar verebilecek her şeydir. Zarar
vermesi gerekmez; verebilmesi yeter. Tehdidin arkasında bir kişi ya da grup
varsa ona **tehdit aktörü** (threat actor) denir. Aktörler amaçlarına ve
güçlerine göre çok farklıdır:

- **Meraklı ya da acemi kişiler:** hazır araçları rastgele deneyenler.
  Güçleri az, ama sayıları çok.
- **Para için çalışan suç grupları:** fidye yazılımı, kart bilgisi
  çalmak, dolandırıcılık. Örgütlüler ve sabırlılar.
- **İçeriden biri** (insider): çalışan, eski çalışan ya da yüklenici. Zaten
  içeride olduğu için birçok önlemin arkasında durur. Her zaman kötü
  niyetli de değildir; yanlışlıkla dosya silen çalışan da bu gruptadır.
- **Bir amaç için saldıranlar** (hacktivist): siyasi ya da toplumsal bir
  mesaj vermek isteyenler.
- **Devlet destekli gruplar:** çok güçlü, çok sabırlı, belirli hedefleri
  olan gruplar.

Her tehdidin arkasında bir insan yoktur. Yangın, sel, elektrik kesintisi
ve donanım arızası da tehdittir; erişilebilirliği en sık bozanlar
bunlardır.

## Açık

**Açık** ya da **zafiyet** (vulnerability), bir tehdidin kullanabileceği
zayıflıktır. Açık her yerde olabilir:

- **Yazılımda:** girdiyi denetlemeyen bir fonksiyon, bir hata.
- **Ayarda:** herkese açık bırakılmış bir paylaşım, değiştirilmemiş
  varsayılan parola.
- **Süreçte:** işten ayrılanın hesabının kapatılmaması.
- **İnsanda:** sahte bir e-postaya inanıp parola yazmak.

Bir açığı kullanmanın yoluna **istismar** (exploit) denir. Bu patikada
istismar yazmıyoruz; yalnızca neden mümkün olduğunu anlayıp açığı
kapatmayı öğreniyoruz.

Tehdit ile açık ayrı şeylerdir ve **ikisi de gerekir**. Hırsız yoksa açık
pencere bir şey kaybettirmez; pencere kilitliyse hırsız o yoldan giremez.
Güvenlikte çoğu zaman tehdidi ortadan kaldıramazsın (dünyadaki bütün
saldırganları durduramazsın), ama açığı kapatabilirsin.

## Risk

**Risk**, bir tehdidin bir açığı kullanıp bir varlığa zarar verme
**ihtimali** ile bu zararın **büyüklüğünün** birleşimidir:

<figure class="fig"><div class="flow">
  <span class="node">Tehdit</span><span class="arrow">→</span>
  <span class="node">Açık</span><span class="arrow">→</span>
  <span class="node">Varlık</span><span class="arrow">→</span>
  <span class="node acc">Etki</span>
</div><figcaption>Risk bu zincirin tamamıdır. Bir halka eksikse risk de yoktur.</figcaption></figure>

Kabaca **risk = olasılık × etki** diye düşünülür. Olasılığı yüksek ama
etkisi küçük bir olay (kantin menüsünün değişmesi) ile olasılığı düşük ama
etkisi büyük bir olay (bütün sağlık kayıtlarının sızması) aynı dikkati
hak etmez. Riski sayıya dökmeyi bir sonraki bölümde, Riski
Değerlendirmek'te yapacağız.

## Önlem

**Önlem** ya da **kontrol** (control), riski azaltmak için yapılan her
şeydir. Önlemler ne zaman işe yaradıklarına göre üçe ayrılır:

| Tür | Ne zaman çalışır | Örnek |
|---|---|---|
| **Önleyici** (preventive) | Olay olmadan önce, olmasını engeller | Kilit, parola, güvenlik duvarı |
| **Tespit edici** (detective) | Olay olurken ya da sonra, fark eder | Kamera, kayıt (log), alarm |
| **Düzeltici** (corrective) | Olaydan sonra, zararı geri alır | Yedekten geri yükleme, yama |

İyi bir sistemde üç türden de vardır. Yalnızca önleyici önlemi olan bir
sistem, önlem bir gün aşıldığında bunu fark edemez; yalnızca tespit edici
önlemi olan sistem ise olayları yalnızca seyreder.

## Bilinen açıklar: CVE

Yazılımlarda bulunan açıklar herkese duyurulur, böylece kullananlar
kendilerini koruyabilir. Her duyurulan açığa **CVE** (Common
Vulnerabilities and Exposures) adlı ortak listede bir kimlik verilir:
`CVE-YIL-NUMARA`. Yıl, kimliğin verildiği yıldır; numara en az dört
basamaklıdır. Bu kimlik sayesinde herkes aynı açıktan söz ettiğini bilir.

Aşağıdaki kimlikler örnek; biçimine bak:

```python
ids = ["CVE-2017-10001", "CVE-2023-20002", "CVE-2025-30003"]
for cve in ids:
    year = int(cve.split("-")[1])
    print(cve, "year:", year, "age:", 2026 - year)
```

```text
CVE-2017-10001 year: 2017 age: 9
CVE-2023-20002 year: 2023 age: 3
CVE-2025-30003 year: 2025 age: 1
```

Kimliği verildikten yıllar sonra bile eski açıklar kullanılmaya devam
eder. Sebep basit: açığın **yaması** (patch, düzeltilmiş sürüm) çıkmıştır,
ama herkes yazılımını güncellememiştir. Saldırıların büyük kısmı yeni ve
bilinmeyen açıklardan değil, yaması çoktan çıkmış açıklardan yararlanır.
Henüz yaması olmayan, yeni bulunmuş açığa **sıfırıncı gün açığı**
(zero-day) denir; az ama tehlikelidir.

## Açığın ağırlığı: CVSS

Her açık aynı derecede tehlikeli değildir. **CVSS** (Common Vulnerability
Scoring System) bir açığa 0 ile 10 arasında bir puan verir: açığa uzaktan
mı ulaşılıyor, parola gerekiyor mu, neyi bozuyor gibi sorulara bakılarak.
Puan ayrıca bir **şiddet** (severity) adıyla anılır:

| Puan | Şiddet |
|---|---|
| 0.0 | None (yok) |
| 0.1 – 3.9 | Low (düşük) |
| 4.0 – 6.9 | Medium (orta) |
| 7.0 – 8.9 | High (yüksek) |
| 9.0 – 10.0 | Critical (kritik) |

Bir tarama ya da denetim çoğu zaman uzun bir bulgu listesi verir. İlk iş
onları puana göre sıralamaktır:

```python
findings = [("login page", 7.5), ("old library", 9.8),
            ("verbose errors", 5.3), ("missing header", 3.1)]
for name, score in sorted(findings, key=lambda f: f[1], reverse=True):
    print(f"{score:>4} {name}")
```

```text
 9.8 old library
 7.5 login page
 5.3 verbose errors
 3.1 missing header
```

CVSS puanı açığın **kendisini** anlatır, senin sistemindeki **riski**
değil. 9.8 puanlı bir açık, internete hiç açılmayan ve önemsiz veri tutan
bir makinede, 7.5 puanlı ama herkesin ulaşabildiği bir giriş sayfasındaki
açıktan daha az acil olabilir. Puan bir başlangıçtır; karar varlığa ve
ortama bakılarak verilir.

## Özet

- **Varlık** korunan şey, **tehdit** zarar verebilecek şey, **açık**
  tehdidin kullanabileceği zayıflık, **risk** ikisinin buluşma ihtimali ve
  etkisidir.
- Tehdit aktörleri meraklılardan devlet destekli gruplara kadar uzanır;
  doğa ve arızalar da tehdittir.
- Önlemler **önleyici**, **tespit edici** ve **düzelticidir**; iyi bir
  sistemde üçü de vardır.
- Bilinen açıklar **CVE** kimliğiyle anılır, **CVSS** ile puanlanır.
- Saldırıların çoğu yaması çıkmış eski açıkları kullanır: güncellemek en
  ucuz önlemlerden biridir.
