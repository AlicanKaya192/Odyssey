# Odyssey nedir?

Odyssey, veri bilimi ve makine öğrenmesini yapılandırılmış bir müfredat
üzerinden öğreten, çevrimdışı çalışan bir masaüstü uygulamasıdır.

Amacı, dağınık kaynaklar arasında gezinmek yerine tek bir yerde ilerleyen ve
ölçülebilir bir öğrenme akışı sunmaktır: her konunun nerede başlayıp nerede
bittiği bellidir, ilerleme kaydedilir, öğrenilenin sınandığı bir adım vardır.

## Nasıl işliyor?

Her bölüm dört parçadan oluşur: konu anlatımı, ders notları, sınav ve kod
alıştırmaları. Bölüm ancak sınav geçildiğinde ve alıştırmalar çözüldüğünde
tamamlanmış sayılır.

Bölümler sırayla açılır. Bir bölüme geçebilmek için bir öncekinin
tamamlanmış olması gerekir; böylece müfredat, üzerine inşa edildiği temel
olmadan ilerlemez.

Kodu uygulamanın içinde yazarsınız. Çalıştırdığınızda program kodu kendi
ortamında yürütür, çıktısını ve ürettiği değişkenleri denetler, hangi
koşulun sağlandığını ve hangisinin sağlanmadığını tek tek gösterir.

## İlkeler

**Değerlendirme deterministiktir.** Alıştırmalar önceden tanımlanmış
kurallarla denetlenir: çıktı karşılaştırması, değişken ve fonksiyon
denetimleri, kodun yapısına bakan kontroller. Aynı kod her çalıştırmada aynı
sonucu verir. Uygulamada dil modeli bulunmaz ve dışarıdaki bir servise
istek gönderilmez; API alıştırmalarının sunucusu da programın içinde çalışır.
Yalnızca Docker Desktop'ın taban imajları indirmesi ve FastAPI sunucusunun
tarayıcıda açılan belge sayfası internete çıkar.

**Verileriniz cihazınızda kalır.** İlerleme, yazdığınız kod ve ayarlar
`%APPDATA%\Odyssey` klasöründeki yerel bir veritabanında tutulur. Hiçbir veri
dışarı aktarılmaz. Yeni sürüme geçildiğinde bu klasöre dokunulmaz; ilerleme
korunur.

**Açık kaynaktır.** Uygulama MIT lisansıyla dağıtılır; kaynak kodu
incelenebilir, değiştirilebilir ve yeniden dağıtılabilir.

## Şu an nerede?

1.0 sürümüyle açık beta dönemi bitti; uygulama uçtan uca çalışır: öğrenme yolu, konu
anlatımı, ders notları, sınavlar, kod alıştırmaları, kademeli ipuçları,
alıştırma ve sınavlarda geçmiş denemeler, ilerleme kaydı, profil, rozetler,
XP, seviyeler ve unvanlar, çalışma zamanlayıcısı, önerilen rotalar, kendi
notlarınız, genel arama, tanıtım turu, Türkçe/İngilizce arayüz, açık/koyu
tema ve uygulama içi güncelleme hazırdır.

On altı patika tamamlanmıştır: **Python Temelleri**, **CS50 Python**,
**Git**, **Algoritmalar**, **Temel Kütüphaneler**, **SQL**, **Matematik**,
**Veri Bilimi**, **Makine Öğrenmesi**, **Zaman Serileri**,
**Doğal Dil İşleme**, **Büyük Veri**, **API**, **Docker**,
**GenAI ve Prompt Mühendisliği** ve **Sistem Tasarımı**. Bazı patikalar
birden fazla modülden oluşur: Matematik, sıfırdan başlayan biri için temel
matematik ile makine öğrenmesinin dayandığı doğrusal cebir, kalkülüs,
olasılık ve istatistik; Algoritmalar, temel algoritmalardan sıfırdan
yazılan makine öğrenmesi algoritmalarına üç modül; Temel Kütüphaneler,
standart kütüphaneden scikit-learn'e dört modül; Sistem Tasarımı, CI/CD ve
MLOps. CS50 Python, Harvard'ın CS50 programlamaya giriş dersinin videolu ve
Türkçe altyazılı uyarlamasıdır. Toplamda 466 bölüm, 12165 sınav sorusu,
2140 alıştırma ve 300 matematik problemi bulunur.

Programı ilk kez kullanıyorsanız **Ayarlar › Öğrenme › Tanıtım turu**
bütün ekranları sırayla gösterir.

macOS sürümü yol haritasındadır.

Hangi değişikliğin hangi sürümde geldiğini **Sürüm Notları** ekranından
izleyebilirsiniz.
