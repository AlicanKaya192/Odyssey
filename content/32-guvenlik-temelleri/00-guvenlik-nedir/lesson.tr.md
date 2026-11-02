# Güvenlik Nedir? CIA Üçlüsü

Bir bilgisayar sistemi bir şeyi saklar ya da bir iş yapar: notlarını tutan
bir okul sistemi, para gönderen bir banka uygulaması, fotoğraflarını
yedekleyen bir telefon. **Bilgi güvenliği** (information security) bu
sistemin, sahiplerinin istediği gibi çalışmaya devam etmesini sağlamaktır:
bilgiyi yalnızca görmesi gerekenler görür, kimse onu fark edilmeden
değiştiremez, gerektiğinde de ona ulaşılır.

Bu patika **savunma** tarafından bakar. Saldırıları öğreneceksin, ama
amacı onları yapmak değil; neden işe yaradıklarını anlayıp nasıl
kapatıldığını görmek. Alıştırmalar hep senin bilgisayarında, senin
kurduğun küçük örneklerde çalışır.

## Neyi koruyoruz? Varlık

Güvenlik bir soruyla başlar: **neyi** koruyoruz? Korunmaya değer her şeye
**varlık** (asset) denir:

- **Veri:** öğrenci notları, müşteri adresleri, parolalar, kaynak kod.
- **Hizmet:** bir web sitesi, bir ödeme sistemi, bir e-posta sunucusu.
- **Donanım:** sunucular, dizüstü bilgisayarlar, telefonlar.
- **Güven ve itibar:** insanların sana veri emanet etmeye devam etmesi.

Her varlığın değeri farklıdır; o yüzden hepsi aynı sıkılıkla korunmaz.
Kantindeki menüyle öğrencilerin sağlık bilgisi aynı kilidin arkasında
durmaz. Hangi varlığın ne kadar korunacağına karar vermeyi sonraki iki
bölümde (Tehdit, Açık ve Risk; Riski Değerlendirmek) öğreneceksin.

## CIA üçlüsü

Bir varlığın "güvende" olması üç ayrı şey demektir. Baş harfleriyle
**CIA üçlüsü** (CIA triad) denir; istihbarat örgütüyle ilgisi yok:

<figure class="fig anat">
  <div class="anat-row"><span><b>C</b>: Gizlilik (Confidentiality)</span><span>Bilgiyi yalnızca görmeye yetkisi olanlar görür. Bozulursa: not listesi herkesin eline geçer.</span></div>
  <div class="anat-row"><span><b>I</b>: Bütünlük (Integrity)</span><span>Bilgi yetkisiz ya da fark edilmeden değiştirilemez. Bozulursa: havale tutarı yolda 100'den 900'e çevrilir.</span></div>
  <div class="anat-row"><span><b>A</b>: Erişilebilirlik (Availability)</span><span>Bilgi ve hizmet, yetkisi olanlara gerektiğinde ulaşılabilir. Bozulursa: sınav günü sistem açılmaz.</span></div>
  <figcaption>Güvenliğin üç ayağı. Bir olay bunlardan birini, ikisini ya da üçünü birden bozabilir.</figcaption>
</figure>

Üçü birbirinden bağımsızdır ve **birbirini zorlayabilir**. Bir dosyayı
kasaya kilitleyip anahtarı atarsan gizliliği mükemmel olur, ama
erişilebilirliği sıfıra iner. Güvenlik işinin büyük kısmı bu üçü
arasında denge kurmaktır.

### Gizlilik

**Gizlilik** (confidentiality), bilginin yalnızca yetkisi olanlara
açılmasıdır. Bozulmasına **sızıntı** (data leak, veri sızıntısı) denir:
yanlış ayarlanmış bir paylaşım klasörü, çalınan bir dizüstü bilgisayar,
yanlış kişiye giden bir e-posta. Korumak için kim olduğunu doğrulamak
(kimlik doğrulama), kimin neyi göreceğine karar vermek (erişim denetimi)
ve bilgiyi okunamaz hâle getirmek (şifreleme) kullanılır. Üçünün de
kendi bölümü var.

### Bütünlük

**Bütünlük** (integrity), bilginin doğru ve tam kalmasıdır: kimse onu
yetkisiz değiştiremez, değişirse de fark edilir. Bütünlüğü bozan olay her
zaman saldırı değildir; yarıda kesilen bir dosya kopyası ya da bozulan
bir disk de bütünlüğü bozar. Korumak için yazma yetkisini sınırlamak,
değişiklikleri kayda geçirmek ve verinin **parmak izini** almak kullanılır.

Parmak izi şöyle bir şeydir: bir metinden kısa, sabit uzunlukta bir değer
hesaplanır ve metindeki en küçük değişiklik bu değeri tamamen değiştirir.
Bu değere **özet** (hash) denir; nasıl çalıştığı Kriptografi modülünün
konusu. Şimdilik yalnızca davranışına bakalım:

```python
import hashlib

original = "pay 100 to Ada"
changed = "pay 900 to Ada"
for text in [original, changed]:
    print(hashlib.sha256(text.encode()).hexdigest()[:16], text)
```

```text
7765ba48a9885011 pay 100 to Ada
81313d488d626434 pay 900 to Ada
```

İki metin arasında tek bir karakter farkı var (`1` yerine `9`), ama
özetlerin ilk 16 karakteri bile hiç benzemiyor. Orijinal metnin özetini
güvenli bir yerde saklayan biri, metin değişince bunu hemen anlar.

### Erişilebilirlik

**Erişilebilirlik** (availability), sistemin gerektiğinde çalışıyor
olmasıdır. Bir sunucuyu taşıyamayacağı kadar istekle boğmak (hizmet
engelleme, denial of service), bir disk arızası, elektrik kesintisi ya da
dosyaları kilitleyen bir zararlı yazılım erişilebilirliği bozar. Korumak
için yedek almak, aynı hizmeti birden fazla makinede çalıştırmak
(yedeklilik, redundancy) ve aşırı yükü sınırlamak kullanılır.

Erişilebilirlik çoğu zaman bir yüzdeyle söz verilir: "sistem yılın
%99,9'unda açık olacak". Bu söze **hizmet düzeyi anlaşması** (service
level agreement, SLA) denir. Yüzdeler birbirine çok yakın görünür, ama
kapalı kalınabilecek süre büyük ölçüde değişir:

```python
minutes_per_year = 365 * 24 * 60
for percent in [99, 99.9, 99.99, 99.999]:
    down = minutes_per_year * (1 - percent / 100)
    print(f"{percent}% -> {down:.1f} minutes per year")
```

```text
99% -> 5256.0 minutes per year
99.9% -> 525.6 minutes per year
99.99% -> 52.6 minutes per year
99.999% -> 5.3 minutes per year
```

Her "9" eklendiğinde izin verilen kesinti on kat azalıyor. %99 yılda
3,65 gün kapalı kalmak demek; %99,999 ise yılda beş dakika.
Bu yüzden yüksek erişilebilirlik çok pahalıdır.

## Bir olay hangi ayağı bozar?

Bir **güvenlik olayı** (security incident), CIA'dan en az birini bozan ya
da bozmaya çalışan her şeydir. Olayı doğru adlandırmak, doğru önlemi
seçmenin ilk adımıdır. Bir olayın hangi ayakları bozduğunu bulan küçük bir
fonksiyon:

```python
def pillars(leaked, modified, unreachable):
    found = []
    if leaked:
        found.append("C")
    if modified:
        found.append("I")
    if unreachable:
        found.append("A")
    return found


print("grades leaked:", pillars(True, False, False))
print("amount changed:", pillars(False, True, False))
print("site down 3 hours:", pillars(False, False, True))
print("files locked, copy sold:", pillars(True, True, True))
```

```text
grades leaked: ['C']
amount changed: ['I']
site down 3 hours: ['A']
files locked, copy sold: ['C', 'I', 'A']
```

Son satır **fidye yazılımına** (ransomware) bir örnek: dosyaları şifreleyip
açmak için para isteyen zararlı yazılım. Dosyalar kullanılamaz
(erişilebilirlik), içerikleri değiştirilmiştir (bütünlük) ve saldırgan
çoğu zaman bir kopyasını da alıp satmakla tehdit eder (gizlilik). Tek bir
olay üç ayağı birden bozabilir.

## CIA'nın yanındaki üç kavram

CIA temeldir ama her şeyi anlatmaz. Sık karşılaşacağın üç kavram daha:

- **Kimlik doğruluğu** (authenticity): bir mesajın ya da kişinin gerçekten
  söylediği kaynaktan gelmesi. "Bu e-postayı gerçekten bankam mı
  gönderdi?"
- **Hesap verebilirlik** (accountability): her işlemin kimin yaptığına
  kadar izlenebilmesi. Bunun için kayıt (log) tutulur.
- **İnkâr edilemezlik** (non-repudiation): bir kişinin yaptığı işlemi
  sonradan "ben yapmadım" diye reddedememesi. Dijital imza bunu sağlar
  (Kriptografi modülü).

## Güvenlik bir denge

Mükemmel güvenlik yoktur; yalnızca "bu varlık için yeterli" güvenlik
vardır. Her önlemin bir bedeli var: para, zaman ve kullanım kolaylığı. Her
girişte üç ayrı parola isteyen bir sistem daha güvenli görünür, ama
insanlar parolaları kâğıda yazıp ekrana yapıştırmaya başlar ve sonuç daha
kötü olur.

<figure class="fig"><div class="versus">
  <div class="no"><h4>Güvenlik bir ürün</h4>Bir kez satın alınır, kurulur ve biter. "Güvenlik duvarımız var, güvendeyiz."</div>
  <div class="ok"><h4>Güvenlik bir süreç</h4>Varlıklar, tehditler ve sistem sürekli değişir. Risk düzenli ölçülür, önlemler gözden geçirilir, olaylardan ders çıkarılır.</div>
</div><figcaption>Tek bir önlem hiçbir sistemi kalıcı olarak korumaz.</figcaption></figure>

## Özet

- Güvenlik bir **varlığı** korumaktır; önce neyin korunduğu belirlenir.
- **Gizlilik:** yalnızca yetkisi olan görür. **Bütünlük:** fark edilmeden
  değişmez. **Erişilebilirlik:** gerektiğinde ulaşılır.
- Bir olay birden fazla ayağı bozabilir; fidye yazılımı üçünü birden.
- Erişilebilirlik yüzdesindeki her "9" izin verilen kesintiyi on kat
  azaltır.
- Güvenlik bir denge ve bir süreçtir; kullanılamayan önlem işe yaramaz.
