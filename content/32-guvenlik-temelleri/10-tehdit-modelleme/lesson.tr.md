# Tehdit Modelleme ve STRIDE

Bir açığı kapatmanın en ucuz zamanı, o açık daha yazılmadan öncesidir.
**Tehdit modelleme** (threat modelling), bir sistemi kurmadan ya da
değiştirmeden önce "burada ne ters gidebilir?" sorusunu **düzenli bir
yolla** sormaktır. Kod incelemesi yazılmış satırlara bakar; tehdit
modelleme tasarıma, yani parçaların nasıl bağlandığına bakar.

## Dört soru

Tehdit modellemenin bütün yöntemleri dört soruya dayanır:

1. **Ne üzerinde çalışıyoruz?** Sistemin bir çizimi.
2. **Ne ters gidebilir?** Tehditlerin listesi.
3. **Bununla ilgili ne yapacağız?** Her tehdide bir cevap (önlem, kabul,
   aktarma; Riski Değerlendirmek bölümündeki dört cevap).
4. **İşi iyi yaptık mı?** Liste eksiksiz mi, önlemler uygulandı mı?

Bu bölüm ilk iki soruya odaklanıyor.

## Sistemi çizmek: veri akış şeması

Sistemi çizmenin yaygın yolu **veri akış şemasıdır** (data flow diagram,
DFD). Yalnızca beş parçası var:

| Parça | Anlamı | Örnek |
|---|---|---|
| **Dış varlık** (external entity) | Senin denetiminde olmayan kişi ya da sistem | Öğrenci, bir ödeme hizmeti |
| **Süreç** (process) | Veriyi işleyen kod | Web uygulaması |
| **Veri deposu** (data store) | Verinin durduğu yer | Veritabanı, dosya |
| **Veri akışı** (data flow) | Parçalar arasında giden veri | Giriş isteği, sorgu |
| **Güven sınırı** (trust boundary) | Güven düzeyinin değiştiği çizgi | İnternet ile iç ağ arası |

Bir okul not sisteminin en basit hâli:

<figure class="fig"><div class="flow">
  <span class="node">Öğrenci</span><span class="arrow">→</span>
  <span class="node acc">Web uygulaması</span><span class="arrow">→</span>
  <span class="node">Not veritabanı</span>
</div><figcaption>Öğrenci internette, uygulama ve veritabanı iç ağda. İlk ok bir güven sınırını geçiyor.</figcaption></figure>

**Güven sınırı** en önemli parçadır. Saldırıların çoğu bir sınırı geçen
veri akışında olur: dışarıdan gelen her şey denetlenmeden içeride
kullanılmamalıdır. Bir akışın sınırı geçip geçmediğini bulmak kolaydır;
iki ucunun bölgesi farklıysa geçiyordur:

```python
zones = {"student": "internet", "web app": "internal", "grades db": "internal"}
flows = [("student", "web app"), ("web app", "grades db"), ("grades db", "web app")]
for src, dst in flows:
    crosses = zones[src] != zones[dst]
    print(f"{src} -> {dst}:", "crosses boundary" if crosses else "same zone")
```

```text
student -> web app: crosses boundary
web app -> grades db: same zone
grades db -> web app: same zone
```

## Ne ters gidebilir? STRIDE

Boş bir sayfaya "ne ters gidebilir?" yazmak zordur. **STRIDE** bu soruyu
altı kategoriye böler; her harf bir tehdit türü ve her tür bir güvenlik
özelliğini bozar:

```python
STRIDE = {
    "S": ("Spoofing", "authenticity"),
    "T": ("Tampering", "integrity"),
    "R": ("Repudiation", "non-repudiation"),
    "I": ("Information disclosure", "confidentiality"),
    "D": ("Denial of service", "availability"),
    "E": ("Elevation of privilege", "authorization"),
}
for letter, (threat, prop) in STRIDE.items():
    print(letter, f"{threat:<23}", prop)
```

```text
S Spoofing                authenticity
T Tampering               integrity
R Repudiation             non-repudiation
I Information disclosure  confidentiality
D Denial of service       availability
E Elevation of privilege  authorization
```

Türkçesiyle ve örnekleriyle:

| Harf | Tehdit | Bozduğu özellik | Not sisteminde örnek |
|---|---|---|---|
| **S** | Kimlik taklidi | Kimlik doğruluğu | Başkasının parolasıyla öğretmen gibi giriş |
| **T** | Kurcalama | Bütünlük | Not değerinin yolda ya da veritabanında değiştirilmesi |
| **R** | İnkâr | İnkâr edilemezlik | Not değiştiren öğretmenin "ben yapmadım" demesi; kayıt yok |
| **I** | Bilgi ifşası | Gizlilik | Bütün notların hata mesajında görünmesi |
| **D** | Hizmet engelleme | Erişilebilirlik | Sınav sonucu günü sitenin isteklerle boğulması |
| **E** | Yetki yükseltme | Yetkilendirme | Öğrencinin not girme sayfasını kullanabilmesi |

Altı harfin ilk beşi CIA'ya ve onun yanındaki kavramlara (Güvenlik Nedir
bölümü) karşılık gelir; altıncısı yetkilendirmeye. Bu yüzden STRIDE bir
kontrol listesi gibi çalışır: her parça için altı soru sorulur.

## Her parçaya hangi harfler?

Her harf her parçaya uymaz. Bir veri deposu kimlik taklidi yapmaz; bir
dış varlığı kurcalayamazsın (senin denetiminde değil). Hangi harflerin
hangi parçaya sorulacağı bir tabloyla belirlenir; buna **parça başına
STRIDE** (STRIDE per element) denir:

```python
PER_ELEMENT = {"external_entity": "SR", "process": "STRIDE",
               "data_store": "TRID", "data_flow": "TID"}
system = [("student", "external_entity"), ("web app", "process"),
          ("grades db", "data_store"), ("login request", "data_flow"),
          ("query", "data_flow")]
total = 0
for name, kind in system:
    letters = PER_ELEMENT[kind]
    total += len(letters)
    print(f"{name:<14} {letters}")
print("threats to consider:", total)
```

```text
student        SR
web app        STRIDE
grades db      TRID
login request  TID
query          TID
threats to consider: 18
```

Beş parçalık küçük bir çizim bile 18 soru üretiyor. Her biri
için "bu tehdit burada mümkün mü, öyleyse ne yapıyoruz?" diye düşünülür.
Bazılarının cevabı "zaten önlemi var" ya da "bu sistemde anlamsız"
olacaktır; önemli olan hiçbirinin atlanmamasıdır. Veri deposundaki **R**
harfi, deponun bir kayıt (log) deposu olduğu durum içindir: kayıtlar
kurcalanırsa inkâr kolaylaşır.

## Bulunan tehditlerle ne yapılır?

Her tehdit bir satır olur: hangi parça, hangi harf, ne olabilir, olasılık
ve etki (Riski Değerlendirmek bölümündeki puanlar), cevap ve sorumlu kişi.
Sonra sıralanır ve en yüksek puanlılardan başlanır. Tehdit modeli bir kez
yazılıp çekmeceye konmaz: sisteme yeni bir parça, yeni bir veri akışı ya
da yeni bir güven sınırı eklendiğinde güncellenir.

## Ne zaman yapılır?

- Yeni bir sistem tasarlanırken, kod yazılmadan önce.
- Büyük bir değişiklikte: yeni bir dış hizmet, yeni bir veri türü, yeni
  bir giriş yolu.
- Bir olaydan sonra: model o olayı öngörmüş müydü?

Tehdit modelleme bir uzmanın tek başına yaptığı iş değildir. En iyi sonuç,
sistemi yazanlarla birlikte bir masa başında, şemanın üstünde konuşarak
alınır.

## Özet

- Tehdit modelleme "ne ters gidebilir?" sorusunu tasarım aşamasında,
  düzenli bir yolla sorar. Dört soru: ne yapıyoruz, ne ters gidebilir, ne
  yapacağız, iyi yaptık mı.
- **Veri akış şeması:** dış varlık, süreç, veri deposu, veri akışı ve
  **güven sınırı**. Saldırılar en çok sınırı geçen akışlarda olur.
- **STRIDE:** kimlik taklidi, kurcalama, inkâr, bilgi ifşası, hizmet
  engelleme, yetki yükseltme; her biri bir güvenlik özelliğini bozar.
- **Parça başına STRIDE** hangi harfin hangi parçaya sorulacağını söyler.
- Tehditler puanlanır, cevaplanır ve model sistem değiştikçe güncellenir.
