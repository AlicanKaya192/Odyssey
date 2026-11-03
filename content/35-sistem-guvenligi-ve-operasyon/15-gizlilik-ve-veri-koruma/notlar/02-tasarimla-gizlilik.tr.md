Gizlilik, bir ürün bittikten sonra eklenen bir ayar değil, baştan verilen
bir tasarım kararıdır. Buna **tasarımla gizlilik** (privacy by design) ve
**varsayılan olarak gizlilik** (privacy by default) denir. Güvenli Yazılım
Geliştirme bölümündeki güvenli varsayılanların gizlilikteki karşılığıdır.

## Tasarımda sorulacak sorular

| Soru | Neden? |
|---|---|
| Bu veriyi neden topluyoruz? | Amacı olmayan veri toplanmaz |
| Daha azıyla olur mu? | Doğum tarihi yerine "18 yaşından büyük mü?" yeter mi? |
| Ne kadar saklayacağız? | Süre en baştan yazılır |
| Kim erişecek? | En az yetki |
| Başka biriyle paylaşılacak mı? | Veri işleyenle sözleşme, kişiye bilgi |
| Kişi verisini görmek ya da sildirmek isterse ne yapacağız? | Envanter ve silme yolu hazır olmalı |

## Varsayılan olarak gizlilik

Bir ayar kullanıcıya bırakılıyorsa, varsayılan değeri **en gizli** olandır:
profil herkese açık değil kapalı başlar, isteğe bağlı veri paylaşımı
kapalıdır, konum ancak kişi açarsa kullanılır. Kişi daha fazlasını bilerek
açabilir; ama hiçbir şey yapmayan kişi korunur.

## Veri koruma etki değerlendirmesi

Yüksek risk taşıyan işler (çok sayıda kişinin sağlık verisi, sürekli konum
takibi, otomatik kararlar) başlamadan önce bir **veri koruma etki
değerlendirmesinden** geçer: hangi veri, hangi risk, hangi önlem. Bu,
Tehdit Modelleme ve STRIDE bölümündeki tehdit modellemenin kişiler
açısından yapılan hâlidir.

## Loglar ve kişisel veri

Kayıt ve İzleme bölümünde gördüğümüz kayıtlar da kişisel veri içerir: IP
adresi, kullanıcı adı, kim ne zaman nereye girdi. Bu yüzden kayıtlar da
amaçla sınırlıdır, saklama süreleri vardır ve erişimleri en az yetkiyle
sınırlanır. Güvenlik için tutulan kayıtları başka bir işe (çalışanları
izlemek gibi) kullanmak amaçla sınırlılık ilkesine aykırıdır.

## Sınır ötesi aktarım

Bir bulut hizmeti verinin başka bir ülkede saklanması anlamına gelebilir.
Kişisel verinin yurt dışına aktarılması hem KVKK'da hem GDPR'da ek
şartlara bağlıdır. Bulut Güvenliği bölümündeki sağlayıcı seçimi bu yüzden
yalnızca teknik değil hukuki bir karardır da.
