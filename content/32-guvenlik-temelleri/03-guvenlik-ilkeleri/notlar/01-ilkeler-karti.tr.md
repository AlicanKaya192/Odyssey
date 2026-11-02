| İlke | İncelemede sorulacak soru | Çiğnendiği bir örnek |
|---|---|---|
| **En az yetki** (least privilege) | Bu hesap ya da program gerçekten bu kadar yetkiye ihtiyaç duyuyor mu? | Web uygulamasının veritabanına yönetici hesabıyla bağlanması |
| **Varsayılan olarak reddet** (fail-safe defaults) | Listede olmayan bir şey gelince ne oluyor? | Yalnızca `.exe`'yi yasaklayan yükleme sayfası |
| **Varsayılan olarak güvenli** (secure by default) | Hiçbir ayara dokunulmazsa sistem güvenli mi? | Kurulumla gelen `admin` / `admin` parolası |
| **Güvenli başarısızlık** (fail securely) | Hata olunca kapı açık mı kalıyor, kapalı mı? | İzin dosyası okunamayınca herkese izin vermek |
| **Derinlemesine savunma** (defence in depth) | Bu önlem aşılırsa arkasında ne var? | Tek parolayla korunan, şifresiz yedekler |
| **Tam aracılık** (complete mediation) | İzin her istekte mi denetleniyor? | Yetkisi alınan kişinin açık oturumunun sürmesi |
| **Açık tasarım** (open design) | Kod herkese açılsa güvenlik bozulur mu? | Gizli bir adrese güvenen yönetim sayfası |
| **Basitlik** (economy of mechanism) | Bu denetim bir oturuşta okunup anlaşılabiliyor mu? | Yüzlerce istisnası olan izin kuralı |
| **Yetki ayrılığı** (separation of privilege) | Tek bir kişi ya da tek bir anahtar yetiyor mu? | Ödemeyi hazırlayan kişinin onu onaylayabilmesi |
| **Kullanılabilirlik** (psychological acceptability) | İnsanlar bunu atlatmaya çalışır mı? | Her hafta değiştirilmesi zorunlu, karmaşık parola |

## İki terim

- **İzin listesi** (allowlist): yalnızca listedekiler serbest.
- **Engel listesi** (blocklist): yalnızca listedekiler yasak. Unutulan şey
  geçer; tek başına kullanılmaz.

## Derinlemesine savunmanın şartı

Katmanların aşılma olasılıkları ancak katmanlar **birbirinden bağımsızsa**
çarpılabilir. Aynı parolaya, aynı sunucuya ya da aynı kişiye dayanan
katmanlar birlikte düşer.
