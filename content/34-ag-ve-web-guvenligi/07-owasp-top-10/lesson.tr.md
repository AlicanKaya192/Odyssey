# OWASP Top 10

Modülün buraya kadarki kısmı yolu anlattı: ağ, DNS, HTTP, oturum. Bundan
sonrası uygulamanın kendisine, yani web sitesinin kodundaki açıklara
bakıyor. Bu alanda en çok başvurulan kaynak **OWASP Top 10**'dur. Bu bölüm
listeyi bir harita olarak tanıtıyor; her başlığı küçük, kendi içinde
çalışan bir örnekle ve hemen ardından savunmasıyla gösteriyor. Ayrıntıları
sonraki bölümler (SQL Enjeksiyonu, XSS, CSRF, SSRF, Kimlik Doğrulama
Hataları) işleyecek.

## OWASP ve Top 10 nedir?

**OWASP** (Open Worldwide Application Security Project), uygulama
güvenliği üzerine açık ve ücretsiz kaynaklar üreten, kâr amacı gütmeyen
bir topluluktur. **Top 10** onun en bilinen belgesidir: birçok kurumdan
toplanan verilere ve uzman görüşüne dayanarak web uygulamalarında en
önemli görülen on **risk kategorisini** sıralar. Bir kontrol listesi ya da
standart değil, **farkındalık** belgesidir: "en sık nerede hata
yapılıyor?" sorusunun cevabı.

Liste birkaç yılda bir güncellenir; kategorilerin sırası ve adları
sürümden sürüme değişebilir, güncel sürüm OWASP'ın kendi yayınından
kontrol edilir. Aşağıda **2025 sürümünü** kullanıyoruz.

<figure class="fig anat">
  <div class="anat-row"><span><b>A01</b> Bozuk erişim denetimi</span><span>Kişi yetkisi olmayan veriye ya da işleme ulaşabiliyor (CSRF ve SSRF de burada).</span></div>
  <div class="anat-row"><span><b>A02</b> Güvenlik yapılandırma hataları</span><span>Hata ayıklama açık, varsayılan parola, gereksiz özellik.</span></div>
  <div class="anat-row"><span><b>A03</b> Yazılım tedarik zinciri hataları</span><span>Açıklı ya da kötü niyetli kütüphane, derleme ve dağıtım hattında bozulma.</span></div>
  <div class="anat-row"><span><b>A04</b> Kriptografik hatalar</span><span>Hassas veri şifresiz, zayıf algoritmayla ya da yanlış kullanılmış kriptoyla korunuyor.</span></div>
  <div class="anat-row"><span><b>A05</b> Enjeksiyon</span><span>Kullanıcı verisi kod gibi yorumlanıyor (SQL, komut, betik; XSS de burada).</span></div>
  <div class="anat-row"><span><b>A06</b> Güvensiz tasarım</span><span>Açık kodda değil tasarımda: gereken denetim hiç düşünülmemiş.</span></div>
  <div class="anat-row"><span><b>A07</b> Kimlik doğrulama hataları</span><span>Zayıf parola kuralı, kaba kuvvete açık giriş, kötü oturum yönetimi.</span></div>
  <div class="anat-row"><span><b>A08</b> Yazılım ya da veri bütünlüğü hataları</span><span>Doğrulanmadan kullanılan güncelleme, eklenti ya da veri.</span></div>
  <div class="anat-row"><span><b>A09</b> Güvenlik kaydı ve uyarı hataları</span><span>Saldırı kaydedilmiyor, kimseye haber verilmiyor ya da kayıtlar sır sızdırıyor.</span></div>
  <div class="anat-row"><span><b>A10</b> Olağandışı durumların yanlış ele alınması</span><span>Hata çıkınca program kapıyı açık bırakıyor ya da tutarsız bir durumda kalıyor.</span></div>
  <figcaption>OWASP Top 10, 2025 sürümü. Sıra, risk değerlendirmesine göredir.</figcaption>
</figure>

Eski kaynaklarda 2021 sürümüyle karşılaşırsınız; numaralar farklıdır
(orada enjeksiyon A03, yapılandırma A05). 2025'te iki kategori yeni:
**tedarik zinciri** (2021'deki "açıklı ve eski bileşenler" kategorisinin
genişlemiş hâli) ve **olağandışı durumlar**. 2021'de ayrı bir kategori olan
**SSRF**, bozuk erişim denetiminin içine alındı. Kategorilerin anlattığı
fikirler ise büyük ölçüde aynı kaldı.

## A01 Bozuk erişim denetimi

Listenin başındaki kategori en sık görülen hatayı anlatır: uygulama
**kimin** istediğine bakıyor ama **neyi** istediğine yetkisi olup
olmadığına bakmıyor. En tipik biçimi adresteki numarayı değiştirerek
başkasının kaydına ulaşmaktır (`/invoices/102`). Buna **güvensiz doğrudan
nesne başvurusu** (IDOR) denir.

```python
INVOICES = {101: {"owner": "ada", "amount": 250},
            102: {"owner": "bob", "amount": 990}}


def get_invoice_bad(user, invoice_id):
    return INVOICES.get(invoice_id)


def get_invoice(user, invoice_id):
    invoice = INVOICES.get(invoice_id)
    if invoice is None or invoice["owner"] != user:
        return None
    return invoice


print(get_invoice_bad("ada", 102))
print(get_invoice("ada", 102))
print(get_invoice("ada", 101))
```

```text
{'owner': 'bob', 'amount': 990}
None
{'owner': 'ada', 'amount': 250}
```

İlk fonksiyon Ada'ya Bob'un faturasını verdi. Doğrusu **her istekte**
kaydın sahibini denetlemek (Güvenlik İlkeleri bölümündeki tam aracılık).
Yok ile yetkisiz aynı cevabı (`None`, HTTP'de 404) veriyor; HTTP ve HTTPS
bölümünde gördüğümüz gibi böylece başkasının faturasının var olduğu da
ele verilmiyor.

Bu kategori iki tanıdık açığı da kapsıyor. **CSRF**'te kişinin tarayıcısı,
**SSRF**'te sunucu, kendi yetkisiyle başkasının istediği bir işi yapıyor.
İkisinde de sorun aynı: isteğin yetkisi denetlenmeden işleniyor. CSRF ve
SSRF bölümleri bunları ayrıca işleyecek.

## A02 Güvenlik yapılandırma hataları

Kod doğru olsa da ayarlar açık bırakabilir: hata ayıklama kipinin açık
kalması (hata sayfası kodu ve ayarları gösterir), varsayılan yönetici
parolası, klasör listeleme, düz HTTP'ye izin. Bunlar otomatik
denetlenebilir:

```python
config = {"debug": True, "admin_password": "admin",
          "dir_listing": False, "https_only": False}

problems = []
if config["debug"]:
    problems.append("debug mode is on")
if config["admin_password"] in {"admin", "password", "1234"}:
    problems.append("default admin password")
if config["dir_listing"]:
    problems.append("directory listing is on")
if not config["https_only"]:
    problems.append("plain HTTP allowed")
for problem in problems:
    print("-", problem)
```

```text
- debug mode is on
- default admin password
- plain HTTP allowed
```

Yayına çıkmadan önce böyle bir denetim çalıştırmak, ayar hatalarının
çoğunu yakalar. Varsayılanlar güvenli seçilir: Güvenlik İlkeleri
bölümündeki "güvenli varsayılan".

## A03 Yazılım tedarik zinciri hataları

Uygulamalar yüzlerce kütüphaneye dayanır; onları derleyen ve dağıtan
araçlara da. Bu zincirin herhangi bir halkası bozulursa uygulama da
bozulur: bilinen açığı olan bir kütüphane, ele geçirilmiş bir paket,
değiştirilmiş bir derleme aracı. En sık görüleni en basitidir: bir
kütüphanede açık yayımlandığında güncellemeyen herkes açıktadır. Hangi
sürümün güncel olduğunu denetlemek bile tuzaklıdır, çünkü sürüm numaraları
metin olarak karşılaştırılamaz:

```python
def parse(version):
    return tuple(int(p) for p in version.split("."))


print("1.10.0" < "1.9.0")
print(parse("1.10.0") < parse("1.9.0"))

installed = {"pagekit": "2.4.1", "imagelib": "1.10.0", "parser": "0.9.3"}
minimum = {"pagekit": "2.4.1", "imagelib": "1.9.2", "parser": "1.0.0"}
for name, version in installed.items():
    ok = parse(version) >= parse(minimum[name])
    print(f"{name:<9} {version:<7} {'ok' if ok else 'UPDATE'}")
```

```text
True
False
pagekit   2.4.1   ok
imagelib  1.10.0  ok
parser    0.9.3   UPDATE
```

Metin olarak `"1.10.0"` daha küçük görünüyor (`1` < `9`), sayı olarak
daha büyük. Savunma: bileşenlerin listesini tutmak, açık bildirimlerini
izlemek, düzenli güncellemek, kullanılmayan bileşeni kaldırmak, sürümleri
sabitlemek ve paketleri yalnızca güvenilir kaynaktan almak (Sistem
Güvenliği modülünün Bağımlılıklar ve Tedarik Zinciri bölümü).

## A04 Kriptografik hatalar

Kriptografi modülünün konusu: parolanın düz metin ya da hızlı bir özetle
saklanması, HTTPS'siz taşınan veri, kod içine yazılmış anahtar, tahmin
edilebilir rastgelelik. Savunma o modülün kurallarıdır: parola için
yavaş, tuzlu özet (Parolaları Saklamak bölümü), taşımada TLS, rastgelelik
için `secrets`, kendi kriptonu yazmamak.

## A05 Enjeksiyon

Enjeksiyonun özü tek cümledir: **kullanıcının verisi, kodun bir parçası
gibi yorumlanıyor.** En bilinen örneği SQL'dir. Sorguyu metin
birleştirerek kurmak, veriyi sorgunun içine yapıştırır. Kötü niyet bile
gerekmiyor; adında kesme işareti olan biri yeter:

```python
import sqlite3

conn = sqlite3.connect(":memory:")
conn.execute("CREATE TABLE users (name TEXT, city TEXT)")
conn.executemany("INSERT INTO users VALUES (?, ?)",
                 [("Ada", "Istanbul"), ("O'Brien", "Izmir")])

name = "O'Brien"
try:
    query = "SELECT city FROM users WHERE name = '" + name + "'"
    print(conn.execute(query).fetchall())
except sqlite3.OperationalError as error:
    print("error:", error)

print(conn.execute("SELECT city FROM users WHERE name = ?", (name,)).fetchall())
```

```text
error: near "Brien": syntax error
[('Izmir',)]
```

Birleştirilen sorguda adın içindeki `'` işareti metni erken kapattı ve
geri kalanı SQL sözdizimi olarak okundu: sorgu bozuldu. Kazara olan bu
bozulmayı bilerek yapan biri sorgunun anlamını değiştirebilir. Doğrusu
**parametreli sorgudur** (ikinci satır): sorgu ile veri ayrı gönderilir,
veritabanı `?` yerine geleni her zaman **veri** olarak ele alır. SQL
Enjeksiyonu bölümü bunu ayrıntılı işleyecek; aynı fikir komut satırı
(komutu metinle kurmamak) ve HTML (XSS bölümünde çıktıyı kodlamak) için de
geçerli.

## A06 Güvensiz tasarım

Bazı açıklar kodun bir satırında değil, **tasarımda** durur. Parola
sıfırlama bağlantısı istemenin hiçbir sınırı yoksa, dört haneli bir
sıfırlama kodu 10000 denemede bulunur; kod ne kadar temiz yazılmış olursa
olsun. Savunma tasarım aşamasındadır: tehdit modelleme (Tehdit Modelleme ve
STRIDE bölümü), hız sınırı, kötüye kullanım senaryolarını baştan düşünmek.

## A07 Kimlik doğrulama hataları

Kaba kuvvete açık giriş formu, zayıf ya da varsayılan parola, çok
aşamalı doğrulamanın (MFA) olmaması, tahmin edilebilir ya da girişte
yenilenmeyen oturum kimliği. Oturum ve Çerez bölümü bunun oturum tarafını
işledi; Kimlik Doğrulama Hataları bölümü giriş tarafını işleyecek.

## A08 Yazılım ya da veri bütünlüğü hataları

Uygulama bir güncellemeyi, bir eklentiyi ya da dışarıdan gelen bir veriyi
**doğrulamadan** kullanırsa, onu yolda ya da kaynağında değiştiren biri
uygulamanın içine girer. Tedarik zinciri kategorisinden farkı ölçeğidir:
orada bütün zincir, burada tek bir paket ya da veri parçası. En basit
denetim, güvenilir bir kanaldan alınan özetle karşılaştırmaktır (Özet
Fonksiyonları bölümü):

```python
import hashlib

update = b"toy update package v2"
published = hashlib.sha256(update).hexdigest()


def safe_to_install(data, expected):
    return hashlib.sha256(data).hexdigest() == expected


print(safe_to_install(update, published))
print(safe_to_install(update + b" + extra", published))
```

```text
True
False
```

Sonuna birkaç bayt eklenmiş paket reddedildi. Özet yalnızca **güvenilir bir
kanaldan** geldiyse işe yarar; paketle aynı yerden gelen özeti
değiştiren biri ikisini birlikte değiştirir. Bu yüzden güncellemeler
dijital imzayla imzalanır (Dijital İmza bölümü).

## A09 Güvenlik kaydı ve uyarı hataları

Bir saldırı kaydedilmezse fark edilmez; kaydedilip de kimseye haber
verilmezse yine durdurulmaz. 2025 sürümü bu yüzden kategorinin adında
**uyarıyı** öne çıkarıyor: kayıt tek başına yetmez, önemli olay birine
ulaşmalıdır. Kayıtlar da dikkat ister: **parola, jeton, oturum kimliği
kayda yazılmaz**, yoksa kayıtları okuyabilen herkes hesapları ele geçirir.
Kayda yazmadan önce bu değerler maskelenir:

```python
import re


def mask(line):
    return re.sub(r"(password|token)=[^&\s]+", r"\1=***", line)


print(mask("login user=ada&password=s3cret&next=/home"))
print(mask("api call token=abc123 status=200"))
```

```text
login user=ada&password=***&next=/home
api call token=*** status=200
```

Düzenli ifade `password=` ya da `token=` ile başlayıp `&` ya da boşluğa
kadar süren değeri `***` ile değiştirdi; adı korudu, böylece kayıt
okunabilir kaldı. İyi kayıt ne olduğunu (kim, ne zaman, ne yaptı, sonuç)
yazar, sırrı yazmaz (Sistem Güvenliği modülünün Kayıt ve İzleme bölümü).

## A10 Olağandışı durumların yanlış ele alınması

Programlar yalnızca her şey yolundayken değil, bir şey ters gidince de
güvenli kalmalıdır: dosya yoksa, veri bozuksa, beklenmeyen bir kullanıcı
gelirse. En tehlikeli hata **açık kalarak başarısız olmaktır** (fail open):
denetim sırasında bir istisna çıkınca programın "izin ver" demesi.

```python
PERMISSIONS = {"ada": {"read", "delete"}}


def can_delete_bad(user):
    try:
        return "delete" in PERMISSIONS[user]
    except Exception:
        return True


def can_delete(user):
    try:
        return "delete" in PERMISSIONS[user]
    except KeyError:
        return False


print(can_delete_bad("bob"))
print(can_delete("bob"))
print(can_delete("ada"))
```

```text
True
False
True
```

Listede olmayan Bob için `PERMISSIONS["bob"]` bir `KeyError` verdi; ilk
fonksiyon her hatayı yakalayıp **izin verdi**. Doğrusu **kapalı kalarak
başarısız olmaktır** (fail closed): beklenen hata açıkça yakalanır ve
cevap "hayır" olur. Her hatayı susturan geniş bir `except Exception` hem
bu açığa yol açar hem de gerçek hatayı gizler (Güvenlik İlkeleri
bölümündeki "güvenli varsayılan").

## Listeyi nasıl kullanmalı?

<figure class="fig"><div class="versus">
  <div class="ok"><h4>İyi kullanım</h4>Ekibin ortak dili olarak, eğitimde ve kod incelemesinde "bu değişiklik hangi kategoriye dokunuyor?" sorusunu sormak için.</div>
  <div class="no"><h4>Kötü kullanım</h4>"On maddeyi kapattık, uygulama güvenli" demek. Liste en sık olanı anlatır, hepsini değil; uygulamanın kendine özgü riskleri tehdit modellemeyle bulunur.</div>
</div><figcaption>Top 10 bir başlangıç noktasıdır, bitiş çizgisi değil.</figcaption></figure>

## Özet

- **OWASP Top 10**, web uygulamalarındaki en önemli on risk kategorisini
  sıralayan bir farkındalık belgesidir; birkaç yılda bir güncellenir.
  Burada 2025 sürümü kullanıldı.
- **A01 Bozuk erişim denetimi:** her istekte kaydın sahibi denetlenir;
  yok ile yetkisiz aynı cevabı verir. CSRF ve SSRF de bu kategoride.
- **A02 Yapılandırma:** hata ayıklama kapalı, varsayılan parola yok;
  yayın öncesi otomatik denetim.
- **A03 Tedarik zinciri:** sürümler sayı olarak karşılaştırılır; düzenli
  güncelleme, güvenilir kaynak.
- **A05 Enjeksiyon:** veri kod gibi yorumlanmamalı; **parametreli sorgu**.
- **A08 Bütünlük:** dışarıdan gelen paket özet ya da imzayla doğrulanmadan
  kullanılmaz.
- **A09 Kayıt ve uyarı:** saldırı kaydedilir ve birine haber verilir, sır
  kaydedilmez (maskeleme).
- **A10 Olağandışı durumlar:** hata çıkınca kapalı kalınır; geniş
  `except` ile hata susturulmaz.
- Liste bir başlangıçtır; uygulamaya özgü riskler tehdit modellemeyle
  bulunur.
