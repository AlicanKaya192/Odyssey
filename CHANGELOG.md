# Odyssey — Değişiklik Günlüğü

Uygulama içindeki Sürüm Notları ekranı bu dosyayı gösterir. Yeni bir sürüm
yayınlamadan önce buraya yazılır; hem GitHub'daki sürüm açıklaması hem
uygulamanın içindeki metin aynı kaynaktan gelir.

## Sürüm numaraları nasıl ilerliyor?

`BÜYÜK.ORTA.KÜÇÜK` — üç parça:

- **Küçük** (`0.1.0` → `0.1.1`): düzeltmeler ve küçük eklemeler. Geliştirme
  boyunca çoğunlukla burası artar.
- **Orta** (`0.1.x` → `0.2.0`): bir aşama tamamlandığında. Örneğin içerik
  aktarımı bittiğinde.
- **Büyük** (`0.x` → `1.0.0`): benden başkasının kullanabileceği ilk sürüm.

Ders içeriğinin ayrı bir sürümü var (`content_version`). Sadece bir ders notu
düzeltildiğinde uygulamanın tamamı yeniden indirilmiyor.

---

## [0.5.0] — yayınlanmadı

### Eklendi
- **Rozetler geldi.** On iki rozet var: ilk programını çalıştırmak, bir
  sınavı hatasız bitirmek, üst üste yedi gün çalışmak gibi. Kazanılmayanlar
  da profilde duruyor ve üstlerine gelince nasıl kazanıldıkları yazıyor —
  neyin mümkün olduğunu görmek için.
- **Etkinlik takvimi geldi.** Bir yılın bütün günleri kare kare duruyor; bir
  günün karesi o gün ne kadar çalıştığına göre koyulaşıyor. Bir günün
  üstüne gelince o gün ne yaptığın yazıyor. Sağdaki listeden yıl
  seçilebiliyor; yeni bir yıla girildiğinde o yıl kendiliğinden ekleniyor.
  Takvim geriye dönük olarak da dolu: daha önce okuduğun dersler ve
  çözdüğün alıştırmalar kendi tarihlerine yerleşti.

### Değişti
- **Ayarlarda tema seçimi artık iki düğme.** Ay koyu temayı, güneş açık
  temayı seçiyor; hangisinin açık olduğu tek bakışta belli oluyor.
  Önceden aç/kapa anahtarıydı ve "kapalı"nın koyu tema demek olduğu ancak
  açıklamayı okuyunca anlaşılıyordu.
- **Ayarlar ve profil düzenleme pencereleri ekranın ortasında sabit
  duruyor.** Taşınamıyor, boyutları değiştirilemiyor.
- **Profil sayfası yeniden düzenlendi.** Solda fotoğraf, ad ve genel
  ilerleme; sağda rozet duvarı; altta etkinlik takvimi. Rozetler bir
  sayfaya sığmadığında oklarla ileri geri geçiliyor. Eskiden sayfanın
  yarısı boştu ve uzun yazılar kırpılıyordu.
- **Öğrenme yolundaki sayılar kesir gösteriyor.** "13" yerine "13/65",
  "3" yerine "3/15" — kaç tanesinden kaçının bittiği görünüyor. Profilde
  aynı dört sayı ikinci kez yazıyordu, oradan kaldırıldı.
- **Profil düzenleme ayrı bir pencerede açılıyor.** "Düzenle" dendiğinde
  arka plan kararıyor ve ad, soyad, fotoğraf tek bir pencerede
  dolduruluyor. Alanlar dar bir sütuna sıkıştığı için yazılar
  okunmuyordu.

### Düzeltildi
- **Sınav süresi ayarı artık o an uygulanıyor.** Sınav açıkken ayarlardan
  süreyi kaldırdığında sayaç anında duruyor, geri açtığında sayaç yeniden
  başlıyor. Eskiden sınavdan çıkıp yeniden girmek gerekiyordu.
- **Tema değiştirirken ekranın bir an bozulması giderildi.** Açıktan koyuya
  geçerken arada stilsiz bir kare görünebiliyordu.
- **İpuçları daha çabuk çıkıyor.** Bir şeyin üstüne geldiğinde açıklamanın
  görünmesi için beklenen süre kısaldı.

---

## [0.4.0] — 1 Eylül 2026

### Eklendi
- **Sınavlar büyütüldü: 150 → 250 soru.** Modüller bölümünden itibaren her
  bölümde **20 soru** var. Genel Tekrar sınavı **50 soruya** çıktı ve on
  dört bölümün tamamını kapsıyor — `print` ayrıntılarından veritabanı
  işlemlerine kadar. Süreler de soru sayısına göre yeniden ayarlandı.
- **Liste üreteçleri, `lambda` ve `sorted(key=...)` eklendi.** Bunlar gerçek
  Python kodunun her yerinde olduğu hâlde müfredatta hiç geçmiyordu:
  `[x * 2 for x in items]` yazımı, süzme, sözlük üreteci; bir listeyi neye
  göre sıralayacağını söylemek; kaç argüman geleceği belli olmayan
  fonksiyonlar (`*args` / `**kwargs`). Listeler ve Fonksiyonlar bölümlerine
  birer ders notu ve ikişer alıştırma olarak girdi.
- **Kütüphane kurmak** anlatıldı: `pip install`, sanal ortam neden gerekiyor,
  `requirements.txt` ve `ModuleNotFoundError` neden çıkıyor. Veri Bilimi
  patikasına geçildiğinde ilk gereken şey buydu ve yalnızca iki cümlede
  geçiyordu.
- **Başlangıç ve Değişkenler bölümlerine zor alıştırma eklendi.** İki bölümde
  de en zor alıştırma orta seviyede kalıyordu.
- **Demetlerle çalışma alıştırması** eklendi. Bölümün adı "Listeler ve
  Demetler" olmasına rağmen hiçbir alıştırma demet istemiyordu.
- **Python Temelleri tamamlandı.** Dört bölüm daha yazıldı ve modül bitti:
  **Dosya İşlemleri** (`with`, kipler, `encoding`, satır sonları, veri
  dosyası okuma), **Nesne Tabanlı Programlama** (`class`, `__init__`,
  `self`, `__str__`, kalıtım), **Veritabanı İşlemleri** (`sqlite3`, tablo
  kurma, `?` yer tutucusu, `SELECT`/`WHERE`/`GROUP BY`, `commit`) ve
  **Genel Tekrar** (öğrenilenlerin birbirine nasıl bağlandığı, hızlı
  başvuru sayfası, buradan sonrası). On beş bölümün tamamı artık açık.
- **Modüller bölümünden itibaren alıştırma sayısı beşe çıktı.** Her bölümde
  bir kolay, iki orta, iki zor alıştırma var. Zor olanlar tek bir konuyu
  değil, birden fazla bölümü aynı anda kullanıyor.
- **Koşul Durumları bölümüne iki ders notu eklendi** — karşılaştırma
  sözlüğü ve koşul tuzakları. O bölümün hiç ders notu yoktu.
- **Başlangıç bölümüne ikinci ders notu eklendi:** veri biliminde Python
  ekosistemi, hangi kütüphanenin ne işe yaradığı ve nerede öğrenileceği.
- **Tip Belirtimleri bölümü.** Bir fonksiyonun ne beklediğini ve ne
  döndürdüğünü yazma biçimi: `text: str`, `-> int`, `list[str]`,
  `dict[str, int]`, değer olmayabildiğinde `int | None`, değer döndürmeyen
  fonksiyonlar için `-> None` ve eski kodda karşına çıkan `Optional[str]`
  yazımı. Belirtimlerin çalışma anında **kontrol edilmediği**, yani bir
  kural değil bir not oldukları ayrıca anlatılıyor. İki ders notu (tip
  sözlüğü, uzun belirtimleri çözme rehberi), on soruluk sınav ve üç
  alıştırma.
- **Konu anlatımlarında şemalar.** Anlatılan şeyin çizimle daha çabuk
  oturduğu yerlerde artık şema var: bir fonksiyon imzasının hangi parçası
  ne demek, `dict[str, int]` içindeki iki tipin hangisinin anahtar hangisinin
  değer olduğu, belirtimin çalışma anında ne olduğu. Şemalar sayfanın
  kendisiyle çiziliyor; temayla birlikte renk değiştiriyor ve metinle
  birlikte büyüyüp küçülüyor.
- **Hata Yakalama bölümü.** İki tür hata, traceback okumak, `try` / `except`,
  hangi hatayı yakalayacağın, çıplak `except` neden kötü, `as error`, `else`
  ve `finally`, `raise` ile hatayı kendin çıkarmak. İki ders notu (hata
  türleri sözlüğü, traceback okuma rehberi), on soruluk sınav ve üç alıştırma.
- **Sınavlar yeniden yazıldı.** Her bölümde artık **10 soru** var (önce 4'tü,
  bir bölümde 3). Modülün tamamında artık 150 soru var. Konu ilerledikçe sorular
  zorlaşıyor, kod okumaya dayanan soruların payı artıyor ve her bölümün
  sonunda bir tane düşündüren soru duruyor.
- **Modüller bölümü.** `import`, `from ... import ...`, `as` ile takma ad,
  kendi dosyanı modül olarak kullanmak ve `if __name__ == "__main__"`.
  İki ders notu (standart kütüphane turu, import biçimleri ve sık yapılan
  hatalar), on soruluk sınav ve üç alıştırma. Son alıştırmada yanına
  konan gerçek bir modül dosyasını import ediyorsun.
- **API ve Docker öğrenme patikaları** eklendi. İçerikleri henüz
  hazırlanmadı, ikisi de kilitli görünüyor.
- **Ayarlara kilidi kaldırma seçeneği geldi.** Açtığında bölümler sırayla
  açılmıyor; istediğin bölüme istediğin an girebiliyorsun.
- **Ayarlara sınav süresini kaldırma seçeneği geldi.** Açtığında sınavlarda
  süre sınırı olmuyor.
- **Sınav başlangıç ekranı.** Sekmeye dokununca sorular hemen açılmıyor;
  önce kaç soru olduğu, ne kadar süre tanındığı ve **önceki denemenin notu**
  görünüyor. Hazır olduğunda başlatıyorsun.
- **Sınavlarda süre.** Konu zorlaştıkça soru başına tanınan süre artıyor.
  Süre dolunca sınav kendiliğinden gönderiliyor. Sayaç sağ üst köşede,
  kaydırmayla kaymıyor ve metnin üstünü örtmüyor.
- **Her denemede sorular ve şıklar karışıyor.** Aynı sırada üst üste
  ikiden fazla doğru cevap gelmiyor.
- **Hakkında ekranı.** Bilgi, Sık Sorulanlar, Bağlantılarım, Ekstra İçerikler
  ve Lisans tek ekranda toplandı; aralarında üstteki sekmelerle geçiliyor.
- **Sık Sorulanlar sayfası.** Uygulama hakkında en sık sorulan sorular;
  başlığa tıklayınca cevabı açılıyor.
- **Bilgi sayfası.** Uygulamanın ne olduğunu, nasıl çalıştığını ve hangi
  ilkelere göre kurulduğunu anlatıyor.
- **Profil fotoğrafı.** Profil ekranından kendi fotoğrafını seçebiliyorsun;
  şeritteki profil düğmesinde de görünüyor. Görsel bilgisayarındaki veri
  klasörüne kopyalanıyor, hiçbir yere gönderilmiyor.
- **Bölümler sırayla açılıyor.** Bir bölüm, önündeki bölüm tamamlanmadan
  açılmıyor; kilitli halkanın altında hangi bölümü bitirmen gerektiği
  yazıyor. Tamamladığın bölümlere istediğin zaman geri dönebiliyorsun.
- Ekstra İçerikler'e `CS_Complete_Terminology_Guide` projesi eklendi.
- Alıştırmada istenen değişken adını kullanmadıysan ama doğru değeri başka
  bir adla tuttuysan, uygulama artık bunu söylüyor: "`second` adında bir
  değişkenin var ve değeri doğru, ama alıştırma bunu `seconds` adıyla
  istiyor." Önceden yalnızca "böyle bir değişken tanımlamamışsın" diyordu.

### Değişti
- **Ayarlarda dil seçimi TR / EN düğmeleriyle yapılıyor.** Aç/kapa anahtarı
  iki seçenek arasında seçim için uygun değildi; hangi tarafın hangi dil
  olduğu ancak açıklama okununca anlaşılıyordu.
- **Ayarlar ekranı yeniden düzenlendi.** Dil ve tema açılır kutulardaydı;
  ayar sayısı artınca bu düzen dağılıyordu. Artık her ayar tek bakışta
  okunuyor: solda adı ve ne işe yaradığı, sağda açık mı kapalı mı olduğunu
  konumuyla gösteren bir anahtar. Ayarlar Görünüm ve Öğrenme diye ikiye
  ayrıldı.
- **Program artık koyu temayla açılıyor.**
- **Sol şerit yediden beş simgeye indi.** Bağlantılarım, Ekstra İçerikler ve
  Lisans artık Hakkında ekranının sekmeleri.
- **Şeridin tepesinde genel ilerleme halkası var.** Yüzde ortasında yazıyor;
  ders okurken de, alıştırma çözerken de ne kadarını bitirdiğin ekranda
  kalıyor. Tıklayınca öğrenme yoluna dönüyor.
- **Ekran başlıkları ortalandı** ve altlarına ince bir vurgu çizgisi geldi;
  geri düğmesi en sola alındı.
- **Modül yolu sayfanın ortasına hizalandı.** Sola yaslanmış duruyordu.
- **Şerit simgeleri iki tonlu çizildi.** Yalnız çizgiden oluşan hâlleri
  cansız duruyordu; gövdeleri kendi renginde hafifçe dolduruldu.
- **Açık tema yumuşatıldı.** Sayfa fazla parlaktı ve uzun metin okurken
  gözü yoruyordu; kartlar saf beyazdı. Soluk yazılar da (süre,
  "Başlanmadı", sayfa içi başlık listesi) koyu temadakinden belirgin
  şekilde daha zor okunuyordu. İkisi de koyu temanın seviyesine çekildi.

### Düzeltildi
- **Alıştırmayı geçince alt alta birden fazla "Geçti" satırı çıkıyordu.**
  Bir alıştırmada altıya kadar kontrol olduğu için panel bunlarla doluyor,
  çıktı aşağı itiliyordu. Artık geçince tek satır yazıyor; bir şey
  tutmadığında da yalnızca tutmayan satırlar görünüyor. Boşalan yer
  çıktıya verildi, kutu iki katına yakın büyüdü.
- **Kod hata verdiğinde panel yanıltıcı şeyler söylüyordu.** İki nokta
  unutulmuş bir sınıf için "Book adında bir sınıf tanımlamamışsın"
  yazıyordu — oysa sınıf yazılmıştı, sorun söz dizimindeydi. Kod hiç
  çalışmadığında artık yalnızca hatanın kendisi ve satır numarası
  gösteriliyor.
- **Sayfalara ilk girişte ekran bir an siyah kalıyordu.** Ders anlatımı,
  ders notu, Hakkında ve Sürüm Notları ekranları tarayıcı motoruyla
  çiziliyor; her biri ilk kez açıldığında ilk kare gelene kadar siyah
  görünüyordu. Bu ilk çizim artık açılışta, pencere daha görünmeden
  yapılıyor.
- **Konu anlatımında sayfa kayarken sıçrıyordu.** Metnin sonuna inince
  "okundu" işareti konuyor, o da sağdaki ilerleme kutusunu güncelliyordu;
  kutu güncellenirken sayfanın tamamı yeniden yükleniyor ve okuduğun yer
  kayıyordu. Kutu artık sayfa yeniden yüklenmeden yerinde değişiyor.
- **Konu anlatımında sağdaki başlık listesi.** Sayfanın sonuna inince
  işaret yukarı fırlıyordu ve son başlığa ("Özet") hiç gelmiyordu.
- **Sınav sorularındaki kod düz metin olarak görünüyordu.** Renk yoktu ve
  daha kötüsü **girinti kayboluyordu** — Python'da girinti kodun kendisi.
  Artık ders anlatımındaki kod blokları gibi görünüyor.
- `>=` ekranda tek bir `≥` işareti olarak çiziliyordu; yazı tipinin
  ligatürleri yüzünden. Artık yazıldığı gibi görünüyor.
- Sınav metinlerinde `**kalın**` yazım ham görünüyordu.
- Yeni bir konu anlatımına geçince sayfa baştan değil, bir önceki konuda
  kalınan yerden açılabiliyordu.
- **Sayfalara ve ayarlara ilk girişte beyaz parlama** oluyordu.
- Uygulama, açılış ekranı hâlâ ekrandayken arkasında beliriyordu; ikisi
  bir süre aynı anda duruyordu. Artık açılış ekranı kaybolurken geliyor.
- Sürüm notlarında uzun maddeler yarıda kesiliyordu; artık tamamı görünüyor.
- Sürüm notlarındaki başlıklar Türkçede "EKLENDI" yazıyordu, artık "EKLENDİ".

## [0.3.0] — 28 Ağustos 2026

### Eklendi
- Ana ekran artık öğrenme patikalarıyla açılıyor: Python, Veri Bilimi, Makine Öğrenmesi ve SQL, 2x2 dizilmiş dört kart. İçeriği hazır olmayan üçü kilit simgesiyle ve soluk görünüyor; Veri Bilimi ile Makine Öğrenmesi kartlarında önce Python patikasının bitirilmesi öneriliyor. İlerleme çubuğu patika kartının üzerinde duruyor.
- Patikada tek modül varsa modül listesi atlanıyor ve doğrudan konulara gidiliyor; tek kartlık bir ekrana ikinci kez tıklatmanın faydası yoktu. Geri dönüş de aynı yolu izliyor.
- Açılış ekranı: uygulama simgesi ve adı, ana pencere kurulurken görünüyor. Önceden Chromium yüklenene kadar ekranda hiçbir belirti yoktu.
- Öğrenme yolunda henüz yazılmamış bölümler de görünüyor: soluk, tıklanmayan halkalar ve "Yakında" yazısı. Python Temelleri'nin geri kalanı (modüller, hata yakalama, dosya işlemleri, OOP, SQLite, genel tekrar) böyle listelendi.

### Değişti
- Ders notu ekranı yeniden tasarlandı. Soldaki 270 piksellik liste paneli kaldırıldı; bir bölümde en çok üç not olduğu için o panel hem ağır duruyor hem de metni sağa itiyordu. Notlar artık metnin üstünde ince bir sekme sırası ve tek not varsa sıra hiç çizilmiyor.
- Ekran başlıkları yeniden tasarlandı. Şerit sayfa içeriğiyle aynı sütuna hizalandı: başlık pencerenin en solunda, içerik ise ortada duruyordu ve ikisi birbirine bağlı görünmüyordu. Şeridin ayrı zemin rengi kaldırıldı; sayfanın üstünde kopuk bir blok gibi duruyordu, artık aynı zeminde ve yalnızca ince bir çizgiyle ayrılıyor. Başlık büyüdü (17px → 26px), üstüne ekranın bağlamını söyleyen küçük bir satır ve solundaki renkli çubuk geldi; renk sol şeritteki simgeyle aynı. Yazılar şeridin dikeyde tam ortasında.
- Windows başlık çubuğu artık uygulamanın rengini alıyor. Koyu temada pencere koyu, çubuk açık kalıyor ve ekran ikiye bölünmüş gibi duruyordu. Ayarlar ve açılış uyarısı pencereleri de aynı renge uyuyor.

### Düzeltildi
- Ders metninde aşağı inince sayfa aniden başa dönüyordu. Sona ulaşınca "okundu" işaretleniyor, bu da ilerleme kutusunu güncelliyor ve belge baştan yükleniyordu. Aynı şey alıştırma yönergesinde ipucu açılınca da oluyordu. Belge yeniden çizilirken okunan yer artık korunuyor.
- Alıştırmayı doğru çözünce numarasındaki onay işareti hemen belirmiyordu; ancak başka bir alıştırmaya geçince ya da bölüm yeniden açılınca görünüyordu.
- Konu ekranındaki sekmelerin arkasındaki dolu kutu kaldırıldı; şerit sayfayla aynı zemine geçince üstte yamalı duruyordu. Seçili sekme artık altındaki çizgiyle belli oluyor ve sekmeler birbirine yapışmıyor.
- Bölüm başlığındaki süre birimi İngilizcede de "dk" yazıyordu; artık çevirilerden geliyor.
- Karşılama kartındaki sayaç etiketleri artık baş harfleri büyük yazılıyor: "Tamamlanan Bölüm", "Çözülen Alıştırma".
- Büyük harfle yazılan başlıklarda Türkçe `i` harfi yanlış dönüşüyordu: "ÖĞRENME PATIKALARI" çıkıyordu, doğrusu "ÖĞRENME PATİKALARI". Python'un `upper()` metodu `i` harfini `I` yapıyor; artık dile göre dönüştürülüyor.

## [0.2.0] — 27 Ağustos 2026

### Eklendi
- Her bölümde artık **en az üç alıştırma** var; toplam 6'dan 18'e çıktı. Yeni alıştırmalar kolaydan zora sıralı ve yalnızca o bölüme kadar anlatılmış kavramları kullanıyor.
- Uygulama ilk açılışta bilgisayarın arayüz diline göre açılıyor: Windows'u Türkçe olan Türkçe, başka bir dilde olan İngilizce görüyor. Ayarlardan bir dil seçildiği anda bu devreye girmiyor, seçim geçerli oluyor.
- Açılışta kapalı beta uyarısı: uygulamanın kararsız çalışabileceği, hata ve çökme görülebileceği ve geri bildirimin nasıl iletileceği yazıyor. Sürüm başına bir kez çıkıyor.
- Lisans ekranı artık seçili dilde: Türkçede MIT Lisansı'nın Türkçe çevirisi, İngilizcede özgün metin görünüyor. İki dilde de ekranda tek bir lisans metni var.
- **Başlangıç** bölümü: Python nedir, ilk program, uygulamanın nasıl çalıştığı ve kurulum notu.
- **Koşul Durumları** bölümü: if / elif / else, koşul sırası, doğruluk değerleri.
- **Döngüler** bölümü: for, while, range, break ve continue notlarıyla.
- **Sözlükler ve Kümeler** bölümü: anahtar-değer mantığı, `in` ile anahtar sorgulama, ekleme ve güncelleme, `items()` ile döngü, kümelerin tekrar tutmaması ve `{}` tuzağı. Ders notlarında sözlük metotları ile dört veri yapısını karşılaştıran bir seçim rehberi var.
- **Listeler ve Demetler** bölümü: liste oluşturma, sıra numarası, negatif numara, dilimleme, `append`/`remove`/`pop`, `len` ve `in`, demetlerin değiştirilemezliği. Ders notlarında liste metotları ve dilimleme ayrıntısı var; kopya tuzağı da anlatılıyor.
- **Fonksiyonlar** bölümü: `def`, parametreler, `return`, varsayılan değerler. Ders notlarında konumsal/isimli argümanlar ve değişken kapsamı (yerel, global) var. `return` ile `print` farkı hem derste hem sınavda ayrıca ele alınıyor.
- Operatörler bölümüne iki ders notu: aritmetik operatörler, atama ve karşılaştırma.

### Değişti
- Sınav sorularındaki, şıklardaki ve açıklamalardaki kod parçaları artık kod olarak çiziliyor: tek aralıklı yazı ve zemin. Düz metin hâlinde `[20, 30]` ile bir cümleyi ayırt etmek zordu.
- Alıştırma şeridi belirginleşti: sayı kalın yazılıyor ve yanında numara düğmeleri duruyor. Bölümde kaç alıştırma olduğu ve hangilerinin çözüldüğü bakar bakmaz görünüyor; istediğine doğrudan atlanabiliyor. Önceki/Sonraki düğmeleri kaldırıldı.
- Sürüm notlarındaki sayfa numaraları ortalandı; "Sayfa 1 / 2" yazısı kaldırıldı, numaralar zaten aynı bilgiyi veriyordu.
- Sol şerit ikiye ayrıldı: üstte her gün girilen ekranlar (Öğrenme Yolu, Profilim, Ekstra İçerikler), altta ayar simgesinin hemen üstünde ara sıra açılanlar (Sürüm Notları, Bağlantılarım, Lisans).
- Sürüm numaralarının yanında kırmızı **ALPHA** rozeti çıkıyor. 1.0 öncesi her sürüm alpha sayılıyor; 1.0 çıktığında rozet kendiliğinden kalkacak.
- Sürüm notları sayfalara bölündü; bir sayfada en fazla üç sürüm görünüyor, altta sayfa düğmeleri var. Önceden bütün sürümler alt alta dizildiği için ekran uzayıp gidiyordu.
- Python Temelleri modülü yeniden düzenlendi. Sıra artık: Başlangıç, Değişkenler, Operatörler, Koşullar, Döngüler.
- Döngüler operatörlerden ayrılıp kendi bölümü oldu; ikisi tek bölüme sığmıyordu.
- Operatörler bölümünün ders notu PDF yerine metin olarak açılıyor.
- Sınavlardaki açıklamalar artık ders anlatımındaki ipucu kutusuyla aynı görünümde.
- Başlangıç sınavının son sorusu uygulamanın arayüzünü soruyordu; yerine dersin anlattığı bir konu kondu: Python'un yorumlanan bir dil olması ne demek.

### Düzeltildi
- Değişkenler bölümünün ikinci alıştırması fonksiyon yazmayı istiyordu, ama fonksiyonlar o noktada henüz anlatılmamıştı. Alıştırma o dersin gerçekten öğrettiği şeyle değiştirildi: metinden sayıya dönüşüm.
- Sürüm notlarındaki kalın yazı ve kod işaretleri ekranda ham görünüyordu; artık biçimlendirilmiş olarak çiziliyor.
- Paketlenmiş uygulamada Windows görev çubuğunda ve pencere başlığında uygulamanın simgesi yerine genel bir program simgesi çıkıyordu. Simge dosyası paketin içinde duruyordu ama uygulama onu yanlış klasörde arıyordu.
- Ders metnini sonuna kadar okumak "okundu" olarak işaretlenmiyordu. Sayfanın kendisi haber vermeye çalışıyordu ama tarayıcı motoru, kullanıcı tıklaması olmadan uygulamaya haber gönderilmesine izin vermiyor; bu yüzden bildirim sessizce düşüyordu. Artık uygulama sayfaya kendisi soruyor.
- Ders metninin altındaki ileri düğmesi, bölümde ders notu olsa bile doğrudan sınava atlıyordu. Artık sırayla gidiyor: konu anlatımı, ders notu, sınav, alıştırma.
- Ders notlarının sonuncusunda ileri düğmesi yoktu, okuyan kişi sınava geçmek için sekmelere dönmek zorundaydı. Son notun altında artık sınava götüren bir düğme var.
- Yeniden düzenleme sırasında iki alıştırma, içeriği tamamen değişmesine rağmen eski kimliğini korumuştu. Bu yüzden açtığınızda önceki alıştırmada yazdığınız kod karşınıza geliyordu. Kimlikler ayrıştırıldı, alıştırmalar artık boş başlıyor.

## [0.1.2] — 27 Ağustos 2026

### Eklendi
- Bağlantılar ve Projeler bölümü: GitHub, LinkedIn, portfolyo, Medium ve açık kaynak projeler.
- Lisans ekranı: MIT metni ve ders içeriğinin lisansı.
- Alıştırmalarda kademeli ipucu; kullanıcı ihtiyacı kadarını açıyor.
- Hata mesajlarının altında ne anlama geldikleri yazıyor.
- Windows için hazır paket: Python kurmadan çalışan `Odyssey.exe`.
- Uygulamanın kendi adı ve simgesi.

### Değişti
- Alıştırma kodu artık tamamen ASCII. İngilizce klavyede Türkçe karakter olmadığı için önceki alıştırmalar İngilizce kullananlar tarafından çözülemiyordu.
- İlerleme göstergesi gerçek durumu yansıtıyor; bölümü açmak artık "okundu" saymıyor.
- Sol şeritteki simgeler koyu temada daha okunaklı.

### Düzeltildi
- Son ders notundayken "Sonraki not" tıklanamaz hâlde görünüyordu, artık hiç çıkmıyor.
- Sürüm notlarında her başlık ayrı bir kart olarak çiziliyordu.

## [0.1.1] — 26 Ağustos 2026

### Eklendi
- Öğrenme yolu ekranı: modül kartları ve bölüm düğümleri.
- Profil ekranı: ad, soyad ve ilerleme istatistikleri.
- Ders notları PDF yerine metin olarak açılıyor; aranabiliyor ve kopyalanabiliyor.

### Değişti
- Ders metinleri Chromium ile çiziliyor: kod blokları renkli, köşeler yuvarlak, sayfa içi başlık listesi kaydırırken yerinde kalıyor.
- Bölümler kilitli değil; tamamlananlara istenildiğinde dönülebiliyor.

### Düzeltildi
- Ayarlar penceresi açılmıyordu.
- Ders notlarına geçince ikinci bir pencere açılıyordu.

## [0.1.0] — 26 Ağustos 2026

### Eklendi
- İlk çalışan sürüm: Python Temelleri modülü, konu anlatımı, sınav ve kod alıştırmaları.
- Kod çalıştırma motoru: beş kontrol tipi, zaman aşımı, anlaşılır hata mesajları.
- Türkçe ve İngilizce arayüz; yeniden başlatmadan değişiyor.
- İlerleme kalıcı olarak saklanıyor.
