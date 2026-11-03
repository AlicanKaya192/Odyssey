# Olay Müdahalesi

Saldırı Tespiti bölümü bir uyarıyla bitti: `bob`'un hesabına dört başarısız
denemenin ardından giriş yapıldı. Şimdi ne olacak? Bir uyarının gerçek bir
**güvenlik olayı** (security incident) olduğu anlaşıldığında yapılanların
bütününe **olay müdahalesi** (incident response) denir.

Olay anında herkes stres altındadır; o an karar vermeye çalışmak hatalara
yol açar. Bu yüzden müdahale **önceden** planlanır: kimin ne yapacağı,
kime haber verileceği, hangi sırayla ilerleneceği yazılıdır. Bu bölüm o
planın adımlarını ve her adımda kullanılan küçük araçları, sahte olay
verisiyle anlatıyor.

## Müdahalenin adımları

<figure class="fig"><div class="flow">
  <span class="node">Hazırlık</span><span class="arrow">→</span>
  <span class="node acc">Tespit ve analiz</span><span class="arrow">→</span>
  <span class="node acc">Sınırlama, temizleme, kurtarma</span><span class="arrow">→</span>
  <span class="node ok">Olay sonrası</span>
</div><figcaption>Yaygın bir çerçevenin dört adımı; son adım yeniden hazırlığa döner.</figcaption></figure>

| Adım | Ne yapılır? |
|---|---|
| **Hazırlık** | Plan, roller, iletişim listesi, yanıt kılavuzları, kayıt ve yedeklerin hazır olması |
| **Tespit ve analiz** | Uyarı gerçek mi? Ne oldu, ne zaman başladı, neyi etkiliyor? Öncelik ver |
| **Sınırlama** | Zararın yayılmasını durdur: makineyi ağdan ayır, hesabı kilitle |
| **Temizleme** | Kök nedeni gider: açığı kapat, ele geçirilen parolaları sıfırla |
| **Kurtarma** | Sistemleri temiz hâlleriyle geri aç, yakından izle |
| **Olay sonrası** | Ne öğrendik? Hangi önlem, kimin sorumluluğunda, ne zamana kadar? |

## Önceliklendirme

Aynı anda birden çok olay olabilir; hepsine aynı hızla bakılamaz. Öncelik
iki soruyla belirlenir: **etki** (ne kadar zarar veriyor?) ve **aciliyet**
(ne kadar hızlı büyüyor?). Basit bir yöntem ikisini 1–3 arasında puanlayıp
çarpmaktır:

```python
INCIDENTS = [
    ("payment service down", 3, 3),
    ("phishing email reported", 1, 2),
    ("admin login from new country", 3, 2),
    ("laptop lost, disk encrypted", 2, 2),
    ("old test server scan alert", 1, 1),
]
for name, impact, urgency in INCIDENTS:
    score = impact * urgency
    level = "P1" if score >= 6 else "P2" if score >= 4 else "P3"
    print(level, score, name)
```

```text
P1 9 payment service down
P3 2 phishing email reported
P1 6 admin login from new country
P2 4 laptop lost, disk encrypted
P3 1 old test server scan alert
```

Ödeme hizmetinin durması ve yönetici hesabına alışılmadık yerden giriş en
öne çıktı. Diski şifreli olduğu için kaybolan dizüstü bilgisayar orta
öncelikte kaldı: şifreleme, etkiyi küçülten bir önceden alınmış önlemdir.

## Analiz: zaman çizelgesi

"Ne oldu?" sorusunun cevabı bir **zaman çizelgesidir** (timeline): farklı
sistemlerin kayıtlarındaki olaylar tek bir sıraya dizilir. Kayıt ve İzleme
bölümünde gördüğümüz gibi, bunun için bütün zamanlar önce UTC'ye çevrilir:

```python
from datetime import datetime, timezone

SOURCES = {
    "vpn": [("2026-11-01T02:14:00+00:00", "login bob from 203.0.113.9")],
    "web": [("2026-11-01T05:16:30+03:00", "admin page opened by bob")],
    "db": [("2026-11-01T02:20:05+00:00", "customers table exported"),
           ("2026-11-01T02:15:10+00:00", "new db user created")],
}
events = []
for source, items in SOURCES.items():
    for stamp, text in items:
        when = datetime.fromisoformat(stamp).astimezone(timezone.utc)
        events.append((when, source, text))
for when, source, text in sorted(events):
    print(when.strftime("%H:%M:%S"), f"{source:<4}", text)
```

```text
02:14:00 vpn  login bob from 203.0.113.9
02:15:10 db   new db user created
02:16:30 web  admin page opened by bob
02:20:05 db   customers table exported
```

Üç kaynaktan dört olay tek bir hikâyeye dönüştü: uzak bağlantıyla giriş,
bir dakika sonra veritabanında yeni bir kullanıcı, ardından yönetici
sayfası ve en sonda tablonun dışa aktarılması. Web sunucusunun kaydı yerel
saatle `05:16` görünüyordu; UTC'ye çevrilmeseydi en sona düşer ve hikâye
yanlış okunurdu.

## Sınırlama: kimi ayırmalı?

Sınırlamanın amacı, araştırma sürerken zararın **yayılmasını**
durdurmaktır. Analizde bulunan **tehlike göstergeleri** (indicators of
compromise, IOC), örneğin şüpheli bir alan adı ya da adres, diğer
makinelerin kayıtlarında aranır; göstergeyle temas etmiş makineler ağdan
ayrılır:

```python
INDICATORS = {"update-check.example", "203.0.113.66"}
HOSTS = {
    "pc-ada": ["mail.example.org", "intranet.local"],
    "pc-bob": ["update-check.example", "intranet.local"],
    "srv-db": ["203.0.113.66"],
    "srv-web": ["cdn.example.net"],
}
to_isolate = sorted(h for h, seen in HOSTS.items() if INDICATORS & set(seen))
print(to_isolate)
```

```text
['pc-bob', 'srv-db']
```

Dört makineden ikisi göstergelerden biriyle temas etmiş. Sınırlama kararı
bir dengedir: ayrılan sunucu iş görmez (erişilebilirlik kaybı), ayrılmayan
sunucu zararı yayabilir. Bir başka önemli kural: ayırırken makine
**kapatılmaz** ve silinmez; üzerindeki iz, Adli Bilişim Temelleri
bölümünde göreceğimiz incelemenin malzemesidir.

## Ölçmek: ne kadar sürede?

Müdahalenin ne kadar iyi gittiği sürelerle ölçülür. Kayıt ve İzleme
bölümünde andığımız iki süre:

- **Tespit süresi:** olayın başlamasından fark edilmesine.
- **Müdahale süresi:** fark edilmesinden kapanmasına.

```python
from datetime import datetime

INCIDENTS = [
    ("2026-10-03T08:00", "2026-10-03T11:30", "2026-10-03T15:00"),
    ("2026-10-12T22:10", "2026-10-13T06:40", "2026-10-13T09:10"),
    ("2026-10-25T13:00", "2026-10-25T13:20", "2026-10-25T14:50"),
]


def hours(a, b):
    delta = datetime.fromisoformat(b) - datetime.fromisoformat(a)
    return delta.total_seconds() / 3600


detect = [round(hours(start, found), 1) for start, found, closed in INCIDENTS]
respond = [round(hours(found, closed), 1) for start, found, closed in INCIDENTS]
print("detect:", detect, "mean", round(sum(detect) / len(detect), 1))
print("respond:", respond, "mean", round(sum(respond) / len(respond), 1))
```

```text
detect: [3.5, 8.5, 0.3] mean 4.1
respond: [3.5, 2.5, 1.5] mean 2.5
```

Ortalama tespit süresi 4,1 saat, ama tek bir olay (gece başlayan
ikinci olay) ortalamayı yukarı çekiyor: gece nöbetinde izleme zayıfmış.
Ölçmenin değeri tam olarak budur: sayılar, olay sonrası toplantıda neyin
düzeltileceğini gösterir.

## Olay sonrası: suçlu değil ders

Her olay bir **olay sonrası değerlendirmeyle** (post-incident review)
kapanır. Amaç suçlu bulmak değil, aynı olayın tekrar etmemesini
sağlamaktır: insanlar hata yapacağı için sistemin o hatayı tolere
etmesi aranır. Toplantının çıktısı somut **eylem maddeleridir**: her
birinin bir sahibi ve bir son tarihi olur ve kapanana kadar izlenir.

## Özet

- **Olay müdahalesi** önceden planlanır: roller, iletişim, kılavuzlar.
- Adımlar: hazırlık; tespit ve analiz; sınırlama, temizleme, kurtarma;
  olay sonrası.
- **Önceliklendirme** etki ve aciliyetle yapılır.
- **Zaman çizelgesi** farklı kaynakların olaylarını UTC'de tek sıraya
  dizer.
- **Sınırlama** tehlike göstergeleriyle temas eden makineleri ayırır;
  makine kapatılmaz, iz korunur.
- **Tespit ve müdahale süreleri** ölçülür; olay sonrası değerlendirme suçlu
  değil eylem maddesi üretir.
