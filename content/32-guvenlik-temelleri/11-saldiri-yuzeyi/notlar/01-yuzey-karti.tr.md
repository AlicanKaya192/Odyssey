## Terimler

| Terim | Anlamı |
|---|---|
| **Saldırı yüzeyi** (attack surface) | Saldırganın sisteme ulaşabildiği bütün noktaların toplamı |
| **Giriş noktası** (entry point) | Bu noktaların her biri: form, uç nokta, port, USB girişi, çalışan |
| **Envanter** (inventory) | Sistemde nelerin olduğunun listesi |
| **Gölge BT** (shadow IT) | Bilgi işlemin haberi olmadan kurulan sistemler |
| **Açıklık** (exposure) | Giriş noktasına kimlerin ulaşabildiği |

## Bir giriş noktasına sorulacaklar

1. Kimler ulaşabiliyor: internet, iç ağ, yalnızca yerel?
2. Kimlik doğrulama gerekiyor mu?
3. Hangi veriyi alıyor, hangi veriye dokunuyor?
4. Gerçekten kullanılıyor mu (kayıtlar)?
5. Sahibi kim, en son ne zaman güncellendi?

## Küçültme listesi

- Kullanılmayan uç noktaları, sayfaları, hizmetleri kaldır.
- Kurulu ama kullanılmayan paketleri kaldır.
- Yönetim arayüzlerini internetten ulaşılamaz yap.
- Veritabanlarını yalnızca uygulamanın ulaşabileceği yere koy.
- Hata ayıklama araçlarını canlı sistemde kapat.
- Yeni özellikleri varsayılan olarak kapalı başlat.
- Her sürümde uç nokta listesinin farkına bak.

## Hatırla

- Saklamak küçültmek değildir: gizli adres bir gün sızar.
- Unutulmuş kapı en tehlikelisidir: ne güncellenir ne izlenir.
- Dış kütüphaneler de yüzeyin parçasıdır; az bağımlılık, küçük yüzey.
