# Genel Tekrar

Bu modül güvenliği bir programın içinden başlayıp bir kurumun işleyişine
kadar götürdü: belleğin nasıl bozulduğu ve nasıl korunduğu, işletim
sisteminin izinleri, güvenli yazılım geliştirme, sırlar ve bağımlılıklar,
kayıt tutmak, saldırıyı fark etmek ve olaya müdahale etmek, kanıtı korumak,
yedekten dönmek, bulut, gizlilik, etik ve sorumlu açıklama. Bu bölüm
hepsini bir arada görüyor; sonunda 40 karışık soru ve birden çok bölümü
birleştiren beş alıştırma var.

## Modülün haritası

| Konu | Ana fikir |
|---|---|
| **Bellek güvenliği** | Sınır denetimi olmayan dillerde taşan veri komşu belleği bozar; Python sınırı kendisi denetler. |
| **Bellek korumaları** | ASLR, DEP ve canary açığı kapatmaz, sömürmeyi zorlaştırır; katmanlı savunma. |
| **İşletim sistemi güvenliği** | İşletim sistemi hakemdir: kullanıcı kipi, süreç yalıtımı, varsayılan ret, günlük işte standart hesap. |
| **Dosya izinleri** | Sahip, grup, diğerleri; okuma, yazma, çalıştırma; herkese yazılabilir dosya tehlikelidir. |
| **Yetki yükseltme** | Yatay ve dikey yükseltme; her istekte sahiplik denetimi, istemciden gelen alana izin listesi. |
| **Güvenli yazılım geliştirme** | Güvenlik SDLC'nin her adımında; güvenli başarısız ol, güvenli varsayılan, girdiyi izin listesiyle doğrula. |
| **Kod inceleme ve statik analiz** | Tehlikeli kalıpları kod çalışmadan bulmak; incelemede ikinci göz. |
| **Bağımlılıklar ve tedarik zinciri** | Sabit sürüm, güvenlik duyurularıyla karşılaştırma, benzer adlı paketler, kilit dosyasındaki özet. |
| **Sır yönetimi** | Sır koda ve depoya yazılmaz; ortamdan ya da kasadan okunur, sızınca döndürülür. |
| **Kayıt ve izleme** | Yapılı kayıt, UTC zaman, kişisel veri ve sır kayda girmez. |
| **Saldırı tespiti** | İmza ve anomali; kesinlik ile duyarlılık dengesi; olayları ilişkilendirmek. |
| **Olay müdahalesi** | Hazırlık, tespit, sınırlama, temizleme, kurtarma, ders çıkarma. |
| **Adli bilişim** | Kanıt özeti, gözetim zinciri, uçuculuk sırası, zaman çizelgesi. |
| **Yedek ve felaket kurtarma** | 3-2-1, RPO ve RTO, geri yükleme denemesi; denenmemiş yedek yedek değildir. |
| **Bulut güvenliği** | Paylaşılan sorumluluk; olayların çoğu yapılandırma hatası; IAM'de varsayılan ret. |
| **Gizlilik ve veri koruma** | Amaçla sınırlılık, veri en aza indirme, takma ad, k-anonimlik, saklama süresi. |
| **Etik ve hukuk** | Testi saldırıdan ayıran yazılı izin; kapsam, zaman penceresi, veri işleme. |
| **Sorumlu açıklama** | Önce sahibine gizlice bildir, düzeltmeyle birlikte duyur. |

## Bir olayın yolu

Modülün operasyon bölümleri tek bir olayda birleşiyor: kayıtlar okunuyor,
şüpheli bir desen fark ediliyor, olayın zaman çizelgesi çıkarılıyor ve
raporda kişisel veri maskeleniyor.

<figure class="fig">
<div class="flow">
<span class="node">Kayıt satırları</span>
<span class="arrow">→</span>
<span class="node acc">Eşikle tespit</span>
<span class="arrow">→</span>
<span class="node acc">Zaman çizelgesi</span>
<span class="arrow">→</span>
<span class="node ok">Maskeli rapor</span>
</div>
<figcaption>Kayıt ve İzleme, Saldırı Tespiti, Adli Bilişim ve Gizlilik bölümleri tek bir akışta.</figcaption>
</figure>

```python
from collections import Counter

LOG = [
    "2026-11-02T09:00:05 FAIL user=ada ip=10.0.0.7",
    "2026-11-02T09:00:09 FAIL user=ada ip=10.0.0.7",
    "2026-11-02T09:00:12 FAIL user=root ip=10.0.0.7",
    "2026-11-02T09:00:15 OK user=ada ip=10.0.0.7",
    "2026-11-02T09:03:40 FAIL user=bob ip=10.0.0.9",
]


def parse(line):
    stamp, status, *pairs = line.split()
    fields = dict(pair.split("=", 1) for pair in pairs)
    return stamp, status, fields["user"], fields["ip"]


events = [parse(line) for line in LOG]
fails = Counter(ip for _, status, _, ip in events if status == "FAIL")
suspects = sorted(ip for ip, count in fails.items() if count >= 3)
print("suspects:", suspects)
for stamp, status, user, ip in events:
    if ip in suspects:
        print(stamp[11:], status, user[0] + "***")
```

```text
suspects: ['10.0.0.7']
09:00:05 FAIL a***
09:00:09 FAIL a***
09:00:12 FAIL r***
09:00:15 OK a***
```

Aynı adresten üç başarısız denemenin ardından **başarılı** bir giriş geldi:
bu artık yalnızca bir alarm değil, bir olaydır ve Olay Müdahalesi
bölümündeki adımlar başlar (hesabı kilitle, oturumları kapat, parolayı
değiştir). Tek başarısız denemesi olan `10.0.0.9` eşiğe ulaşmadı. Rapordaki
kullanıcı adları kişisel veri olduğu için maskelendi; olayın anlaşılması
için tam ada gerek yok.

## Sık karışan çiftler

| İkisi | Fark |
|---|---|
| ASLR / DEP | ASLR adresleri rastgele yapar; DEP veri alanında kod çalışmasını engeller |
| Yatay / dikey yetki yükseltme | Başka bir kullanıcının verisine / daha yüksek bir role ulaşmak |
| Statik analiz / dinamik test | Kodu çalıştırmadan okumak / çalışırken denemek |
| Sır / yapılandırma | Sızınca zarar veren değer / sızınca zarar vermeyen ayar |
| Kayıt / izleme | Olayı yazmak / yazılanı sürekli izleyip uyarmak |
| İmza tabanlı / anomali tabanlı tespit | Bilinen deseni aramak / olağandan sapmayı aramak |
| Sınırlama / temizleme | Yayılmayı durdurmak / kök nedeni ortadan kaldırmak |
| RPO / RTO | Ne kadar veri kaybı / ne kadar kesinti kabul edilir |
| IDS / IPS | Saldırıya benzeyeni tespit edip uyarır / durdurur |
| Takma ad / anonim | Anahtarla geri dönebilir, veri kişisel / kimseyi göstermez |
| Koordineli / tam açıklama | Düzeltmeyle birlikte / düzeltme beklemeden |

## Özet

- Savunma **katmanlıdır**: tek bir koruma her şeyi durdurmaz, her katman
  saldırganın işini zorlaştırır.
- **En az yetki** her yerde aynı fikir: dosya izni, süreç, bulut rolü,
  test izni.
- Güvenlik yazılımın **her aşamasında**: tasarımda, kodda, bağımlılıkta,
  yayında.
- Operasyon döngüsü: **kaydet, izle, tespit et, müdahale et, kanıtı koru,
  kurtar, ders çıkar**.
- **Denenmemiş yedek** ve **denenmemiş plan** güvence vermez.
- Gizlilik ve etik, teknik bilginin **nasıl kullanıldığını** belirler; izin
  yazılı olana verilir.
