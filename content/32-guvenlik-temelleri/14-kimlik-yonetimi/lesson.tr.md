# Kimlik Yönetimi ve Tek Oturum

Kimlik Doğrulama bölümü tek bir girişi anlattı: "bu kişi gerçekten Ada
mı?". Bir kurumda ise yüzlerce kişi, onlarca sistem ve her gün değişen
görevler var. **Kimlik ve erişim yönetimi** (IAM, identity and access
management) bu kalabalığı düzenler: kime hesap açılacak, hangi yetki
verilecek, görev değişince ne olacak, ayrılınca hangi kapılar kapanacak.
Bu bölümün ikinci yarısı da her sisteme ayrı ayrı giriş yapmak yerine tek
bir yerden girmeyi, yani **tek oturum açmayı** (SSO) anlatıyor.

## Hesabın yaşam döngüsü

Bir hesabın ömrü üç olayla anlatılır; İngilizce baş harfleriyle **JML**:

| Olay | Ne olur? | Sık yapılan hata |
|---|---|---|
| **Katılan** (joiner) | Yeni çalışana rolüne göre hesaplar açılır. | "Ne lazım olur bilmiyoruz" diye fazla yetki vermek. |
| **Değişen** (mover) | Görev değişir; yeni rolün yetkileri eklenir, **eskileri kaldırılır**. | Yalnızca eklemek: kişi yıllar içinde her rolün yetkisini biriktirir (En Az Yetki bölümündeki yetki birikmesi). |
| **Ayrılan** (leaver) | Bütün hesaplar kapatılır, bildiği ortak sırlar değiştirilir, cihazları geri alınır. | Bir sistemi unutmak. |

Ayrılan bir çalışanın unutulan hesabına **öksüz hesap** (orphaned account)
denir. Kimse onu kullanmadığı için parolası değişmez, kimse ona bakmaz ve
saldırgan için sessiz bir kapıdır. Öksüz hesapları bulmanın yolu basittir:
insan kaynaklarındaki **etkin çalışan listesi** ile her sistemdeki hesap
listesini karşılaştırmak.

```python
active = {"ada", "bora", "ceren"}
accounts = {
    "mail": ["ada", "bora", "ceren", "deniz"],
    "wiki": ["ada", "deniz"],
    "payroll": ["ceren", "emre"],
}
for system, users in accounts.items():
    for user in users:
        if user not in active:
            print(f"{system:<8} {user:<6} orphaned")
```

```text
mail     deniz  orphaned
wiki     deniz  orphaned
payroll  emre   orphaned
```

`deniz` iki sistemde, `emre` bordro sisteminde unutulmuş. Bu karşılaştırma
düzenli olarak (örneğin ayda bir) yapılır; buna **erişim gözden geçirmesi**
(access review) denir. Her yöneticiye ekibinin yetkileri gösterilir ve
"bu hâlâ gerekli mi?" diye sorulur.

İnsana bağlı olmayan hesaplar da var: bir programın veritabanına bağlanmak
için kullandığı **hizmet hesabı** (service account). Bunların da bir
sahibi olmalı; sahibi ayrılan hizmet hesabı öksüz hesabın en tehlikeli
türüdür, çünkü çoğu zaman geniş yetkilidir ve parolası yıllarca değişmez.

## Merkezî kimlik

Her sistemin kendi kullanıcı listesi olursa JML her sistemde ayrı ayrı
yapılır ve bir tanesi mutlaka unutulur. Çözüm, kimlikleri **tek bir
yerde** tutmaktır: bir **dizin** (directory). Kişiler, gruplar ve roller
oradadır; sistemler kişiyi oradan sorar. Ayrılan çalışanın dizindeki
kaydı kapatılınca ona bağlı her sistemin kapısı birden kapanır. Dizinlere
erişmek için yaygın standart **LDAP**'tir.

## Tek oturum açma (SSO)

**Tek oturum açma** (single sign-on, SSO), kişinin bir kez giriş yapıp
birçok uygulamayı yeniden parola girmeden kullanmasıdır. İki taraf var:

- **Kimlik sağlayıcı** (IdP, identity provider): kişinin gerçekten giriş
  yaptığı yer. Parolayı ve çok faktörlü doğrulamayı yalnızca o görür.
- **Hizmet sağlayıcı** (SP, service provider): kişinin kullanmak istediği
  uygulama. Parolayı hiç görmez; IdP'nin "bu Ada'dır" diyen **imzalı**
  belgesine güvenir.

<figure class="fig"><div class="flow">
  <span class="node">Uygulama (SP)</span><span class="arrow">→</span>
  <span class="node acc">IdP: parola + ikinci faktör</span><span class="arrow">→</span>
  <span class="node">İmzalı jeton</span><span class="arrow">→</span>
  <span class="node">SP imzayı denetler</span><span class="arrow">→</span>
  <span class="node ok">İçeride</span>
</div>
<figcaption>Tek oturum açmada parola yalnızca kimlik sağlayıcıya gider; uygulama imzalı jetona güvenir.</figcaption>
</figure>

Farklı kurumların birbirinin kimliğine güvenmesine **federasyon**
(federation) denir: bir üniversitenin öğrencisinin başka bir kurumun
kütüphane sistemine kendi okul hesabıyla girmesi gibi.

**Faydaları:** kişi tek bir güçlü parola hatırlar (parola tekrarı azalır);
çok faktörlü doğrulama tek yerde zorunlu tutulur; ayrılan çalışanın erişimi
tek yerden kapanır; bütün girişler tek yerde kayda geçer.

**Riski:** bütün yumurtalar tek sepettedir. IdP'yi ele geçiren her
uygulamaya girer, IdP çökerse kimse hiçbir yere giremez. Bu yüzden IdP
hesapları güçlü çok faktörlü doğrulamayla korunur ve IdP'nin kendisi en
sıkı izlenen sistemlerdendir.

## Standartlar

| Standart | Ne için? | Belge |
|---|---|---|
| **SAML 2.0** | Kurumsal tek oturum açma (çoğunlukla web) | XML biçiminde imzalı **onay** (assertion) |
| **OAuth 2.0** | **Yetki devri**: bir uygulamaya, şifreni vermeden, senin adına sınırlı bir iş yapma izni | **Erişim jetonu** (access token) |
| **OpenID Connect** (OIDC) | OAuth 2.0'ın üstüne **kimlik** katmanı: "giren kim?" | **Kimlik jetonu** (ID token), JWT biçiminde |

<figure class="fig"><div class="versus">
  <div><h4>OAuth 2.0</h4>"Bu uygulama takvimimi <b>okuyabilir</b>." Bir <b>izin</b> verir. Erişim jetonu kimin girdiğini söylemek için tasarlanmamıştır; tek başına giriş için kullanılması yaygın bir hatadır.</div>
  <div><h4>OpenID Connect</h4>"Giren kişi <b>Ada</b>, şu kimlik sağlayıcı doğruladı." Bir <b>kimlik</b> bildirir. Kimlik jetonu kimin, kimin için, ne zamana kadar sorularını cevaplar.</div>
</div><figcaption>OAuth yetki devridir, OpenID Connect kimlik doğrulamadır; "OAuth ile giriş" denince çoğu zaman OIDC kastedilir.</figcaption></figure>

## İmzalı jeton

IdP'nin verdiği jeton, içinde bilgi taşıyan ve **imzalanmış** bir metindir.
Yaygın biçim **JWT**'dir (JSON Web Token): üç parça, aralarında nokta:
`başlık.gövde.imza`. Gövde base64 ile kodlanmış bir JSON'dur. Burada aynı
fikri iki parçalı küçük bir **oyuncak** jetonla görüyoruz: gövde ve
HMAC imzası (Parola Saklama bölümündeki anahtarlı özet). Gerçek
uygulamada jeton bir kütüphaneyle üretilip denetlenir; elle yazılmaz.

```python
import base64
import hashlib
import hmac
import json

KEY = b"toy-shared-key-for-the-lesson"


def sign(text):
    return hmac.new(KEY, text.encode(), hashlib.sha256).hexdigest()


def make_token(claims):
    body = base64.urlsafe_b64encode(json.dumps(claims).encode()).decode()
    return body + "." + sign(body)


def read_token(token):
    body, signature = token.split(".")
    if not hmac.compare_digest(signature, sign(body)):
        return "bad signature"
    return json.loads(base64.urlsafe_b64decode(body))


token = make_token({"sub": "ada", "role": "user"})
print(read_token(token))
body, signature = token.split(".")
print(base64.urlsafe_b64decode(body))

fake = json.dumps({"sub": "ada", "role": "admin"}).encode()
forged = base64.urlsafe_b64encode(fake).decode() + "." + signature
print(read_token(forged))
```

```text
{'sub': 'ada', 'role': 'user'}
b'{"sub": "ada", "role": "user"}'
bad signature
```

İki şey görünüyor:

1. **İmza gizlemez.** İkinci satırda gövdeyi anahtarsız çözdük; jetonu
   gören herkes içini okuyabilir. Jetona parola ya da gizli bilgi konmaz.
2. **İmza değişikliği yakalar.** Gövdede `user`'ı `admin` yapıp eski imzayı
   ekleyen jeton reddedildi: anahtarı bilmeyen yeni imza üretemez.

Bu yüzden sıra önemlidir: **önce imza, sonra içerik.** İmzası
denetlenmemiş bir jetonun içindeki `role` alanına güvenmek, kişinin kendi
yazdığı yetkiye güvenmektir. Gerçek JWT'de bir tuzak daha var: başlıkta
algoritma yazar ve bazı eski kütüphaneler "algoritma yok" (`none`) diyen
imzasız jetonu kabul ediyordu. Sunucu **hangi algoritmayı beklediğini
kendisi belirler**, jetonun söylediğine bakmaz.

## İmza doğru, jeton geçerli mi?

İmzanın doğru olması yetmez. Jetonun gövdesindeki **iddialar** (claims)
da denetlenir:

| İddia | Anlamı | Denetim |
|---|---|---|
| `iss` (issuer) | Jetonu kim verdi? | Güvendiğimiz IdP mi? |
| `aud` (audience) | Jeton kimin için? | Bizim uygulamamız için mi? |
| `sub` (subject) | Jeton kimi anlatıyor? | Kişinin kimliği |
| `exp` (expiration) | Ne zamana kadar geçerli? | Süresi dolmuş mu? |
| `nbf` (not before) | Ne zamandan beri geçerli? | Henüz erken mi? |

`aud` denetimi sık unutulur: aynı IdP'nin **kütüphane uygulaması** için
verdiği jeton, **not sistemi** tarafından kabul edilirse, kütüphanede
jetonu gören biri not sistemine de girer.

```python
def check(claims, now):
    if claims.get("iss") != "https://id.school.example":
        return "wrong issuer"
    if claims.get("aud") != "grades-app":
        return "wrong audience"
    if now >= claims.get("exp", 0):
        return "expired"
    return "ok"


claims = {
    "iss": "https://id.school.example",
    "aud": "grades-app",
    "sub": "ada",
    "exp": 1000,
}
print(check(claims, 900))
print(check(claims, 1000))
print(check({**claims, "aud": "library-app"}, 900))
```

```text
ok
expired
wrong audience
```

Burada zaman küçük bir sayı; gerçekte `exp` 1970'ten beri geçen saniyedir.
Jetonların ömrü kısa tutulur (dakikalar): çalınan jeton kısa süre işe
yarasın. Uzun süren oturum için ayrı bir **yenileme jetonu** (refresh
token) kullanılır ve o da iptal edilebilir.

## Oturumu kapatmak

Tek oturum açmanın bir eşi de **tek oturum kapatma**dır (single logout):
IdP'den çıkınca bağlı uygulamalardaki oturumlar da kapanmalıdır. Ayrılan
çalışanın IdP hesabı kapatıldığında elinde hâlâ geçerli bir jeton varsa,
jetonun süresi dolana kadar içeride kalabilir; kısa jeton ömrünün bir
nedeni de budur.

## Özet

- Hesap yaşam döngüsü **JML**: katılan, değişen, ayrılan. Değişende eski
  yetkiler kaldırılır, ayrılanda hiçbir sistem unutulmaz.
- **Öksüz hesaplar** etkin çalışan listesiyle karşılaştırarak bulunur;
  erişim düzenli olarak gözden geçirilir.
- **SSO**'da parola yalnızca **IdP**'ye gider, **SP** imzalı jetona güvenir.
  Fayda: tek güçlü giriş, tek yerden kapatma; risk: IdP tek hedef.
- **SAML** kurumsal SSO, **OAuth 2.0** yetki devri, **OpenID Connect**
  kimlik.
- Jetonda önce **imza**, sonra **iddialar**: `iss`, `aud`, `exp`, `nbf`.
  İmza içeriği gizlemez.
