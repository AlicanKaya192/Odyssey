# Genel Tekrar

Bu modül önce bir paketin ağda nasıl yol aldığına, sonra o yolun üstünde
duran web uygulamalarına baktı: katmanlar ve adresler, ağ saldırıları,
güvenlik duvarı ve bölümleme, DNS, HTTPS, oturumlar, OWASP'ın listelediği
sık açıklar ve bunların savunmaları. Bu bölüm hepsini bir arada görüyor;
sonunda 40 karışık soru ve birden çok bölümü birleştiren beş alıştırma
var.

## Modülün haritası

| Konu | Ana fikir |
|---|---|
| **Ağ katmanları** | Uygulama, taşıma, ağ, bağlantı; kapsülleme; CIDR ve özel aralıklar; açık her port saldırı yüzeyi. |
| **Ağ saldırıları** | Protokoller karşı tarafı doğrulamaz: dinleme, ortadaki adam, ARP, sahte kaynak adresi, SYN seli, yeniden oynatma. |
| **Güvenlik duvarı** | Yukarıdan aşağıya ilk tutan kural, varsayılan ret, durumlu süzme, çıkış süzmesi; WAF ek katman. |
| **VPN ve bölümleme** | VPN yolun bir parçasını korur; bölgeler ve izin listesi yanal hareketi daraltır; sıfır güven. |
| **DNS güvenliği** | Önbellek zehirleme, DNSSEC imzası, şifreli DNS; sahipsiz kayıtlar. |
| **HTTP ve HTTPS** | İsteğin her parçası kullanıcının elinde; 401/403/404; TLS gizlilik, bütünlük, sunucu kimliği; HSTS. |
| **Oturum ve çerez** | `secrets` ile kimlik; Secure, HttpOnly, SameSite; girişte yenileme; süre sınırı; imzalı çerez. |
| **OWASP Top 10** | Erişim denetimi, enjeksiyon, yapılandırma, bileşenler, bütünlük, kayıt; liste bir başlangıç. |
| **SQL enjeksiyonu** | Parametreli sorgu; ad için izin listesi; `LIKE` kaçışı; ikinci derece. |
| **XSS** | Bağlama göre çıktı kodlama; şema denetimi; otomatik kodlayan şablon; CSP. |
| **CSRF** | Oturuma bağlı jeton, SameSite, köken denetimi; `GET` durum değiştirmez. |
| **SSRF** | Ayrıştırılmış adresle izin listesi; iç adresleri IP üzerinde reddetmek; yönlendirmeler. |
| **Kimlik doğrulama hataları** | Aynı mesaj, artan bekleme, tek kullanımlık sıfırlama kodu, uzunluk ve yaygın parola listesi. |
| **Girdi doğrulama ve kodlama** | Önce kanonik biçim, `fullmatch`, izin listesi; yol geçişi; argüman listesi; doğrulama kodlamanın yerini tutmaz. |
| **Güvenli API** | Her nesnede sahiplik; girişte ve çıkışta alan izin listesi; kova sınırı; anahtar özeti; HMAC imzası. |
| **CORS ve başlıklar** | Köken = şema + ad + port; izin listesiyle CORS ve `Vary: Origin`; ön kontrol; CSP, HSTS, `nosniff`, çerçeve engeli. |

## Bir isteğin yolu

Bir web isteği sunucuya ulaştığında, modülün savunmalarının çoğu sırayla
devreye girer:

<figure class="fig"><div class="flow">
  <span class="node">Oturum</span><span class="arrow">→</span>
  <span class="node acc">Köken + CSRF</span><span class="arrow">→</span>
  <span class="node acc">Sahiplik</span><span class="arrow">→</span>
  <span class="node">Parametreli sorgu</span><span class="arrow">→</span>
  <span class="node ok">Kodlanmış cevap</span>
</div><figcaption>Kim olduğu, isteğin nereden geldiği, nesnenin kimin olduğu, verinin kod olmaması ve çıktının bağlamına göre kodlanması.</figcaption></figure>

Aşağıdaki küçük not uygulaması bunu baştan sona yapıyor. Veritabanı
bellekte, istekler sözlük; hiçbir ağ bağlantısı yok:

```python
import hmac
import html
import sqlite3

db = sqlite3.connect(":memory:")
db.execute("CREATE TABLE notes (id INTEGER, owner TEXT, body TEXT)")
db.executemany(
    "INSERT INTO notes VALUES (?, ?, ?)",
    [(1, "ada", "<b>hi</b>"), (2, "bob", "secret")],
)
SESSIONS = {"s-ada": {"user": "ada", "csrf": "t-123"}}
ALLOWED_ORIGINS = {"https://notes.example"}


def handle(method, note_id, headers, form=None):
    session = SESSIONS.get(headers.get("cookie", ""))
    if session is None:
        return 401, "login required"
    if method == "POST":
        if headers.get("origin") not in ALLOWED_ORIGINS:
            return 403, "bad origin"
        if not hmac.compare_digest(form.get("csrf", ""), session["csrf"]):
            return 403, "bad csrf token"
    row = db.execute(
        "SELECT body FROM notes WHERE id = ? AND owner = ?",
        (note_id, session["user"]),
    ).fetchone()
    if row is None:
        return 404, "not found"
    return 200, "<p>" + html.escape(row[0]) + "</p>"


ada = {"cookie": "s-ada", "origin": "https://notes.example"}
print(handle("GET", 1, ada))
print(handle("GET", 2, ada))
print(handle("GET", 1, {}))
print(handle("POST", 1, {"cookie": "s-ada", "origin": "https://other.example"}, {}))
print(handle("POST", 1, ada, {"csrf": "guess"}))
print(handle("POST", 1, ada, {"csrf": "t-123"}))
```

```text
(200, '<p>&lt;b&gt;hi&lt;/b&gt;</p>')
(404, 'not found')
(401, 'login required')
(403, 'bad origin')
(403, 'bad csrf token')
(200, '<p>&lt;b&gt;hi&lt;/b&gt;</p>')
```

Satır satır: notun içindeki `<b>` kodlandı ve sayfada yazı olarak
görünecek (XSS). `bob`'un notu `ada`'ya `404` ile döndü; not var ama onun
değil (nesne düzeyinde yetkilendirme, varlığı ele vermeyen cevap). Çerezi
olmayan istek `401` aldı. Başka kökenden gelen `POST` jetona bakılmadan
geri çevrildi (köken denetimi), doğru kökenden ama yanlış jetonla gelen de
(CSRF jetonu, sabit süreli karşılaştırma). Yalnızca son istek bütün
kapılardan geçti. Sahiplik denetimi sorgunun içinde ve parametreyle
yapılıyor: `note_id` ne olursa olsun veri olarak kalır (SQL enjeksiyonu).

Gerçek bir uygulamada oturum kimliği ve jeton `secrets` ile üretilir,
çerez `Secure; HttpOnly; SameSite=Lax` ile gönderilir ve cevaba güvenlik
başlıkları eklenir; burada okunabilsin diye kısa, sabit değerler var.

## Sık karışan çiftler

| Çift | Fark |
|---|---|
| Kimlik doğrulama / yetkilendirme | "Kimsin?" / "Bu nesne senin mi, bu işe iznin var mı?" |
| `401` / `403` / `404` | Kimlik yok / yetki yok / yok (ya da varlığı gizleniyor) |
| Doğrulama / kodlama | Veri beklenen biçimde mi / veri yazıldığı yerde kod olmasın |
| XSS / CSRF | Sayfada başkasının kodu çalışır / başka site kullanıcı adına istek gönderir |
| CSRF / SSRF | Tarayıcı kandırılır / sunucu kandırılır |
| Aynı köken politikası / CORS | Okumayı engeller / okumaya sunucunun izin vermesi |
| DNSSEC / şifreli DNS | Cevap değişmedi mi / sorguyu kim görüyor |
| VPN / HTTPS | Yolun bir parçasını korur / tarayıcı ile site arasını uçtan uca korur |
| İzin listesi / kara liste | Geçerli olanı tarif eder / bilinen kötüyü sayar, hep bir şey unutur |
| Durumsuz / durumlu güvenlik duvarı | Her paketi ayrı değerlendirir / bağlantıları hatırlar |
| Güvenlik başlığı / uygulama düzeltmesi | İkinci katman / asıl çözüm |

## Ortak çizgiler

Bölümler farklı konulara bakıyor ama aynı birkaç fikir hep geri geldi:

- **Kullanıcıdan gelen her şey girdidir:** adres, başlık, çerez, gövde,
  dosya adı, başka bir API'nin cevabı.
- **İzin listesi, varsayılan ret:** güvenlik duvarı kuralları, kökenler,
  alanlar, şemalar, ana bilgisayarlar, dosya türleri.
- **Ayrıştır, sonra karar ver:** adresi metinle değil `urlsplit` ile,
  yolu `normpath` ile, IP'yi `ipaddress` ile.
- **Veri ile kodu ayır:** parametreli sorgu, bağlama göre kodlama, argüman
  listesi.
- **Sırlar `secrets` ile üretilir, `compare_digest` ile karşılaştırılır.**
- **Derinlemesine savunma:** her katman (bölümleme, WAF, CSP, SameSite)
  bir öncekinin kaçırdığını yakalamak için var; hiçbiri asıl düzeltmenin
  yerini tutmuyor.

## Özet

- Ağ katmanlıdır; protokollerin çoğu karşı tarafı doğrulamadığı için
  şifreleme ve kimlik doğrulama birlikte gerekir.
- Ağ katmanında güvenlik duvarı, bölümleme ve sıfır güven; ad katmanında
  DNSSEC ve şifreli DNS; taşımada TLS ve HSTS.
- Web uygulamasında her istek için: oturum, köken ve CSRF jetonu,
  nesnenin sahipliği, parametreli sorgu, bağlama göre kodlanmış çıktı.
- Sunucunun dışarıya attığı istekler (SSRF) ve API'lerin sınırları da
  aynı izin listesi düşüncesiyle korunur.
- Başlıklar ve tarayıcı politikaları ikinci katmandır; asıl savunma
  uygulamanın kendi kodundadır.
