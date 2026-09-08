# SQL Server'ı Kurmak

Bu patikada SQL'i bir Python kütüphanesinin arkasından değil, **gerçek bir
veritabanı sunucusunda** öğreneceksin. Sorguyu yazacaksın, sunucu
çalıştıracak, sonuç tablosu karşına gelecek. Kurumlarda iş tam olarak
böyle yürüyor.

Bu bölüm tek bir şey yapıyor: **düzeneği kuruyor.** Sonunda "Çalıştır"a
basıp sonuç göreceksin, gerisi ondan sonra.

## Neden Microsoft SQL Server?

SQL bir dil, ama tek bir SQL yok. Her veritabanı kendi lehçesini
konuşuyor: PostgreSQL, MySQL, Oracle, SQL Server. Temeli — `SELECT`,
`WHERE`, `JOIN` — hepsinde aynı; farklar kenarlarda.

Microsoft SQL Server'ı seçmemizin sebebi basit: **kurumsal ortamda en sık
karşına çıkacak olan bu.** Bankada, sigortada, kamuda, ERP sistemlerinin
arkasında çoğunlukla o duruyor. Lehçesinin adı **T-SQL**.

Bir başkasını öğrenmen gerektiğinde de kayıp yaşamayacaksın: bildiğinin
%90'ı olduğu gibi geçerli.

Kuracağın sürüm **Express** — Microsoft'un ücret almadan dağıttığı sürüm.
Boyut sınırı var (veritabanı başına 10 GB) ama dilin tamamını
destekliyor; öğrenirken hiçbir eksiği yok.

## Önce karıştırılan şeyleri ayıralım

Kurulum sırasında dört ayrı isim göreceksin. Hangisinin ne olduğu baştan
oturursa kurulum da kolaylaşıyor:

<figure class="fig">
  <div class="anat">
    <div class="anat-row"><span class="anat-label">SQL Server</span><span class="anat-body">Sunucunun kendisi. Bilgisayarında <b>arka planda çalışan bir servis</b>; penceresi yok, simgesi yok. Veriyi tutan ve sorguları çalıştıran şey bu.</span></div>
    <div class="anat-row"><span class="anat-label">Veritabanı</span><span class="anat-body">Sunucunun içindeki bir kutu. Bir sunucuda onlarca veritabanı olabilir; tablolar bunların içinde durur.</span></div>
    <div class="anat-row"><span class="anat-label">T-SQL</span><span class="anat-body">SQL Server'ın konuştuğu lehçe. Yazacağın dil bu.</span></div>
    <div class="anat-row"><span class="anat-label">SSMS</span><span class="anat-body">Sunucuya bağlanan bir <b>arayüz programı</b> (SQL Server Management Studio). Sunucunun kendisi değil, ona bakmanı sağlayan pencere.</span></div>
    <div class="anat-row"><span class="anat-label">ODBC sürücüsü</span><span class="anat-body">Programların sunucuyla konuşurken kullandığı ara katman. Odyssey de bunu kullanıyor.</span></div>
  </div>
  <figcaption>En sık yapılan karışıklık: SSMS'i kurup "SQL Server'ı kurdum" sanmak. SSMS yalnızca bir pencere; arkasında sunucu yoksa boş açılır.</figcaption>
</figure>

## Odyssey nasıl bağlanıyor?

Sen "Çalıştır"a bastığında olan şu:

<figure class="fig">
  <div class="flow">
    <span class="node">Yazdığın sorgu</span>
    <span class="arrow">-&gt;</span>
    <span class="node">Odyssey</span>
    <span class="arrow">-&gt;</span>
    <span class="node">ODBC Driver 18</span>
    <span class="arrow">-&gt;</span>
    <span class="node acc">SQL Server</span>
    <span class="arrow">-&gt;</span>
    <span class="node ok">Sonuç tablosu</span>
  </div>
  <figcaption>Zincirdeki her halka gerekiyor. Bir sonraki adımlarda ilk üçünü kuracağız; sonuncusu kendiliğinden geliyor.</figcaption>
</figure>

Odyssey sunucuyu **kendisi buluyor**; adres yazman gerekmiyor. Sırayla
`.\SQLEXPRESS`, `(localdb)\MSSQLLocalDB`, `.` ve `localhost` adreslerini
deniyor, hangisi cevap verirse onu kullanıyor.

## Adım 1 — SQL Server Express

İndirme sayfası: **<https://go.microsoft.com/fwlink/p/?linkid=2216019>**

Bu adres Microsoft'un **kendi yönlendirme bağlantısı**: yeni bir sürüm
çıktığında Microsoft onu güncelliyor, yani her zaman güncel sürümü
indiriyorsun. Bağlantı çalışmazsa
<https://www.microsoft.com/tr-tr/sql-server/sql-server-downloads>
sayfasından "Express" başlığını bul.

İnen dosyayı çalıştırınca üç seçenek çıkıyor. **Basic**'i seç — diğer
ikisi kurumsal kurulum içindir, senin ihtiyacın yok.

Sonrası kendiliğinden ilerliyor: lisans metnini kabul et, klasörü olduğu
gibi bırak, kurulumun bitmesini bekle. Beş ile on beş dakika sürüyor.

Bitiş ekranında birkaç bilgi görünüyor. **Instance Name** satırında
`SQLEXPRESS` yazdığını gör, sonra pencereyi kapat. Diğer düğmelere
("Connect Now", "Customize", "Install SSMS") basmana gerek yok.

Kurulum bittiğinde sunucu **çalışmaya başlamış oluyor** ve bilgisayarını
her açtığında kendiliğinden açılıyor. Ayrıca bir şey başlatman gerekmiyor.

## Adım 2 — ODBC sürücüsü

Odyssey sunucuya bu sürücüyle bağlanıyor. Genellikle 1. adımla birlikte
kuruluyor, yani muhtemelen zaten var.

Kontrol etmek istersen: Başlat menüsüne **ODBC** yaz, "ODBC Veri
Kaynakları (64 bit)" uygulamasını aç, **Sürücüler** sekmesine geç. Listede
`ODBC Driver 18 for SQL Server` görünmeli.

Yoksa buradan kurulur:
<https://learn.microsoft.com/tr-tr/sql/connect/odbc/download-odbc-driver-for-sql-server>
— sayfadaki **x64** bağlantısını al.

## Adım 3 — SSMS (isteğe bağlı)

**<https://aka.ms/ssmsfullsetup>** — bu adres de her zaman güncel sürümü
veriyor.

SSMS, sunucuya bağlanıp veritabanlarını ağaç hâlinde gezmeni, tabloları
tıklayarak açmanı, sorgu yazmanı sağlayan program. Sahada SQL yazan
herkesin ekranında açık durur.

**Alıştırmalar için gerekmiyor.** Sorguyu Odyssey'in içinde yazıp
çalıştıracaksın. Ama bir noktada işi gerçek bir araçla görmek isteyeceksin
ve SSMS o araç. Şimdi kurmasan da olur, sonra kurarsın.

SSMS'i açtığında bağlantı penceresi çıkıyor. **Server name** kutusuna
`.\SQLEXPRESS`, **Authentication** kutusunda `Windows Authentication`,
**Encryption** kutusunda `Optional` seçip Connect'e bas.

## Adım 4 — Denemek

Kurulum bitti. Şimdi çalıştığını gör: bu bölümün **Alıştırma** sekmesine
geç ve **Çalıştır**'a bas.

Sonuç panelinde bir tablo görüyorsan zincirin tamamı çalışıyor demektir.

## Bir şey olmazsa

Hata mesajı hangisi olursa olsun, sebebi genelde ikisinden biri:

<figure class="fig">
  <div class="anat">
    <div class="anat-row"><span class="anat-label">"ODBC sürücüsü bulunamadı"</span><span class="anat-body">2. adım eksik. Sürücüyü kur, Odyssey'i yeniden başlat.</span></div>
    <div class="anat-row"><span class="anat-label">"SQL Server'a ulaşılamadı"</span><span class="anat-body">Sunucu çalışmıyor olabilir. Başlat menüsüne <code>services.msc</code> yaz, listede <b>SQL Server (SQLEXPRESS)</b> satırını bul; durumu "Çalışıyor" değilse sağ tıklayıp Başlat de.</span></div>
  </div>
</figure>

Kurulumda instance adını değiştirdiysen (`SQLEXPRESS` yerine başka bir şey
yazdıysan) Odyssey onu bulamaz. En kolayı kurulumu tekrarlayıp `Basic`
seçmek.

## Verine bir şey olmuyor

Bu bölümden sonra kendi veritabanlarını da kuracaksın. Odyssey'in
alıştırmalarının onlara dokunmadığını bilmen için iki şey:

- Alıştırmaların veritabanları **`Odyssey_` önekiyle** açılıyor. Senin
  kendi veritabanlarına karışmıyor.
- Bir alıştırmayı her çalıştırdığında yaptığın **her değişiklik geri
  alınıyor.** Yanlışlıkla bir tabloyu silsen bile bir sonraki
  çalıştırmada yerinde duruyor. Bu kasıtlı: denemekten çekinmeni
  istemiyoruz.

## Özet

- **SQL Server** arka planda çalışan sunucu, **SSMS** ona bakan pencere,
  **ODBC sürücüsü** programların bağlanma yolu. Üçü ayrı şey.
- Kurulacak sürüm **Express**, kurulum seçeneği **Basic**, instance adı
  **SQLEXPRESS**.
- Odyssey sunucuyu kendisi buluyor; adres yazman gerekmiyor.
- SSMS alıştırmalar için şart değil, ama sahada kullanılan araç.
- Yazdığın her şey çalıştırma sonunda geri alınıyor; bozmaktan korkma.
