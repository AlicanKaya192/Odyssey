## Üç ayak

| Ayak | Sorduğu soru | Bozan olay | Koruyan önlem |
|---|---|---|---|
| **Gizlilik** (confidentiality) | Yalnızca yetkisi olan mı görüyor? | Sızıntı, çalınan cihaz, yanlış paylaşım | Kimlik doğrulama, erişim denetimi, şifreleme |
| **Bütünlük** (integrity) | Bilgi doğru ve tam mı, değişirse fark edilir mi? | Yetkisiz değişiklik, yarım kalan kopya, bozuk disk | Yazma yetkisini sınırlamak, özet (hash), kayıt |
| **Erişilebilirlik** (availability) | Gerektiğinde ulaşılıyor mu? | Aşırı yük, arıza, fidye yazılımı | Yedek, yedeklilik, yük sınırı |

## Yanındaki kavramlar

| Kavram | Anlamı |
|---|---|
| **Varlık** (asset) | Korunmaya değer her şey: veri, hizmet, donanım, itibar. |
| **Güvenlik olayı** (security incident) | CIA'dan en az birini bozan ya da bozmaya çalışan olay. |
| **Sızıntı** (data leak) | Gizli bilginin yetkisiz kişilere geçmesi. |
| **Hizmet engelleme** (denial of service) | Sistemi gerçek kullanıcılara hizmet veremez hâle getirmek. |
| **Fidye yazılımı** (ransomware) | Dosyaları şifreleyip açmak için para isteyen zararlı yazılım. |
| **Kimlik doğruluğu** (authenticity) | Mesajın ya da kişinin söylediği kaynaktan gelmesi. |
| **Hesap verebilirlik** (accountability) | Her işlemin yapana kadar izlenebilmesi. |
| **İnkâr edilemezlik** (non-repudiation) | Yapılan işlemin sonradan reddedilememesi. |
| **SLA** (service level agreement) | Erişilebilirlik için verilen söz, genelde yüzde olarak. |

## Hatırla

- Üç ayak birbirini zorlayabilir: kilitleyip anahtarı atmak gizliliği
  artırır, erişilebilirliği bitirir.
- Bütünlüğü bozan her şey saldırı değildir; arızalar da sayılır.
- Bir olayı adlandırırken "hangi ayak?" diye sor; önlem ona göre seçilir.
