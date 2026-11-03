Tek bir sunucunun kayıtlarına bakmak kolaydır. Ama bir kurumda yüzlerce
sunucu, uygulama ve ağ cihazı vardır ve bir saldırı birkaçına birden
dokunur. Bu yüzden kayıtlar tek bir yerde toplanır.

## Merkezî kayıt

Her sistem kayıtlarını, yerelde tutmanın yanında, bir **merkezî kayıt
sistemine** gönderir. Faydaları:

- **Bütün resim:** bir kullanıcının aynı dakikada hangi sistemlere
  dokunduğu tek bir sorguyla görülür.
- **Dayanıklılık:** saldırgan bir sunucunun kayıtlarını silse bile kopyası
  merkezde durur.
- **Ortak biçim:** kayıtlar aynı alan adlarına ve UTC saatine çevrilir;
  karşılaştırmak kolaylaşır.
- **Erişim denetimi:** kayıtları kimin okuyabileceği tek yerden yönetilir.

Kayıtları toplayan, ilişkilendiren ve kurallara göre uyarı üreten
sistemlere genel olarak **SIEM** (Security Information and Event
Management) denir.

## Uyarıdan yorgunluğa

İzlemenin en sık başarısızlığı uyarı **eksikliği** değil, **fazlalığıdır**.
Günde yüzlerce önemsiz uyarı üreten bir sistemde gerçek uyarı gözden
kaçar; buna **uyarı yorgunluğu** (alert fatigue) denir. Bunu azaltmak
için:

| Yöntem | Ne yapar? |
|---|---|
| Eşikleri ölçerek ayarlamak | Olağan gürültüyü uyarıdan ayırır |
| Uyarıları gruplamak | Aynı kaynaktan gelen yüz uyarıyı tek olaya indirir |
| Önem derecesi vermek | Önce kritik olana bakılır |
| Her uyarıya bir yanıt yazmak | "Bu uyarı gelince ne yapılır?" belli olur |
| Kimsenin bakmadığı uyarıyı kaldırmak | Gürültü azalır |

Bu konu Saldırı Tespiti bölümünde ölçülerek ayrıntılı anlatılıyor.

## Kayıtlar da korunur

Kayıtlar, sistemin en hassas verilerinden biridir: kim, ne zaman, nereden
bağlandı. Bu yüzden kayıt sistemi de en az yetkiyle açılır, kayıtlar
iletilirken şifrelenir, kayıtları silme ya da değiştirme yetkisi çok az
kişide olur ve bu işlemlerin kendisi de kaydedilir.

## İzlemenin ölçüsü

Bir izleme düzeninin ne kadar iyi çalıştığı iki süreyle ölçülür:

- **Tespit süresi:** olayın başlamasıyla fark edilmesi arasında geçen süre.
- **Müdahale süresi:** fark edilmesiyle durdurulması arasında geçen süre.

İkisi de olay müdahalesinde kullanılan ölçülerdir (Olay Müdahalesi
bölümü); izleme ne kadar iyiyse birincisi o kadar kısalır.
