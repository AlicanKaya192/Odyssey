# Güvenli API

Şimdiye kadarki web bölümleri çoğunlukla tarayıcının gösterdiği sayfalara
baktı. Bugünkü uygulamaların büyük kısmı ise bir **API** üzerinden konuşur:
telefon uygulaması, tarayıcıdaki betik ya da başka bir sunucu, adrese JSON
gönderir ve JSON alır. Sayfa yoktur; ama sayfada gördüğümüz sorunların
çoğu API'de de vardır, üstelik bazıları daha kolay görünür hâle gelir,
çünkü saldırgan isteği doğrudan kendisi yazar. Bu bölüm API'ye özgü
hataları ve savunmalarını küçük, bellekte çalışan Python fonksiyonlarıyla
gösteriyor; hiçbir ağ bağlantısı kurulmuyor.

OWASP'ın web uygulamaları için olan Top 10 listesinin yanında, API'ler
için ayrı bir listesi de var (**API Security Top 10**). O listenin ilk
sırasındaki hatayla başlıyoruz.

## Nesne düzeyinde yetkilendirme

API'de kaynaklar çoğunlukla bir kimlikle istenir: `GET /orders/2`. Kimliği
istek yazan kişi seçer. Sunucu yalnızca "bu kişi giriş yapmış mı?" diye
bakıp "bu sipariş bu kişinin mi?" diye bakmazsa, herkes başkasının
siparişini sayıyı değiştirerek okuyabilir:

```python
ORDERS = {
    1: {"owner": "ada", "total": 40},
    2: {"owner": "bob", "total": 75},
}


def get_order_leaky(user, order_id):
    return ORDERS.get(order_id)


def get_order(user, order_id):
    order = ORDERS.get(order_id)
    if order is None or order["owner"] != user:
        return 404, None
    return 200, order


print(get_order_leaky("ada", 2))
print(get_order("ada", 2))
print(get_order("ada", 1))
```

```text
{'owner': 'bob', 'total': 75}
(404, None)
(200, {'owner': 'ada', 'total': 40})
```

İlk fonksiyon `ada`'ya `bob`'un siparişini verdi. Bu hataya **nesne
düzeyinde bozuk yetkilendirme** (Broken Object Level Authorization, BOLA)
denir; web listesindeki adı **IDOR**'dur (Insecure Direct Object
Reference). OWASP Top 10 bölümündeki "bozuk erişim denetimi"nin API'deki en
sık hâlidir.

Savunma, nesneyi getiren **her** uç noktada sahipliği denetlemektir. İki
ayrıntı önemli:

- Başkasının siparişi için `403` (yasak) yerine `404` (yok) dönmek,
  siparişin var olup olmadığını da ele vermez.
- Sırayla artan sayılar kimliği tahmin etmeyi kolaylaştırır; rastgele
  kimlikler (`secrets.token_hex`) işi zorlaştırır ama **denetimin yerini
  tutmaz**. Tahmin edilemeyen kimlik de bir gün bir günlükte ya da
  paylaşılan bir bağlantıda görünür.

<figure class="fig">
<div class="flow">
<span class="node">istek: GET /orders/2</span>
<span class="arrow">→</span>
<span class="node">kim? (kimlik doğrulama)</span>
<span class="arrow">→</span>
<span class="node acc">bu nesne onun mu?</span>
<span class="arrow">→</span>
<span class="node ok">cevap</span>
</div>
<figcaption>Kimlik doğrulama "kim" sorusunu cevaplar; yetkilendirme her nesne için ayrıca sorulur.</figcaption>
</figure>

## Fazladan alan atamak

Bir profil güncelleme uç noktası gelen JSON'u olduğu gibi kayda yazarsa,
istek yazan kişi formda hiç olmayan alanları da gönderebilir:

```python
def update_leaky(user, body):
    user.update(body)
    return user


ALLOWED = {"name", "email"}


def update_safe(user, body):
    rejected = sorted(set(body) - ALLOWED)
    for key in ALLOWED & set(body):
        user[key] = body[key]
    return user, rejected


body = {"name": "Ada L", "role": "admin"}
print(update_leaky({"name": "Ada", "role": "user"}, body))
print(update_safe({"name": "Ada", "role": "user"}, body))
```

```text
{'name': 'Ada L', 'role': 'admin'}
({'name': 'Ada L', 'role': 'user'}, ['role'])
```

`update_leaky` kullanıcıyı kendi isteğiyle yönetici yaptı. Bu hataya
**toplu atama** (mass assignment) denir. Savunma bir **izin listesidir**:
yalnızca değiştirilebilecek alanlar kopyalanır. Reddedilen alanları
saklamak yerine `422` ile geri çevirmek de bir seçenektir; istemci hatasını
görür.

## Fazla veri göndermek

Aynı sorunun ters yönü de var: sunucu kaydın tamamını gönderip "istemci
gerekeni gösterir" diye düşünür. Ama JSON'un tamamı istemcinin elindedir:

```python
user = {
    "id": 7,
    "name": "Ada",
    "email": "ada@example.com",
    "password_hash": "pbkdf2$...",
    "is_admin": False,
}
PUBLIC = ["id", "name"]


def public_view(record):
    return {key: record[key] for key in PUBLIC}


print(sorted(user))
print(public_view(user))
```

```text
['email', 'id', 'is_admin', 'name', 'password_hash']
{'id': 7, 'name': 'Ada'}
```

Kaydın beş alanından yalnızca ikisinin başkalarına gösterilmesi gerekiyor.
Cevap her zaman **açıkça seçilmiş** alanlardan kurulur; kayıt nesnesi
olduğu gibi JSON'a çevrilmez. API Security Top 10'da bu iki hata (fazla
atamak, fazla göstermek) tek başlıkta toplanır: **nesne özelliği düzeyinde
bozuk yetkilendirme**.

<figure class="fig">
<div class="versus">
<div class="no">
<h4>Kaydı olduğu gibi</h4>
<p>Gelen JSON kayda yazılır, kayıt JSON'a çevrilip gönderilir. Bir alan
eklenince kimse fark etmeden dışarı açılır.</p>
</div>
<div class="ok">
<h4>İzin listesiyle</h4>
<p>Girişte yalnızca değiştirilebilir alanlar, çıkışta yalnızca
gösterilebilir alanlar. Yeni alan varsayılan olarak kapalıdır.</p>
</div>
</div>
<figcaption>İki yönde de izin listesi: yeni bir alan kendiliğinden dışarı açılmaz.</figcaption>
</figure>

## İstek sınırı

Sınırsız bir API'ye tek bir istemci saniyede binlerce istek gönderebilir:
parola dener, veri kazır ya da sunucuyu yorar. **Kova algoritması** (token
bucket) sık kullanılan bir sınırdır: kovada en fazla `capacity` jeton
vardır, her istek bir jeton harcar, kova her saniye `rate` jetonla dolar:

```python
def make_bucket(capacity, rate):
    state = {"tokens": capacity, "last": 0}

    def allow(now):
        elapsed = now - state["last"]
        state["tokens"] = min(capacity, state["tokens"] + elapsed * rate)
        state["last"] = now
        if state["tokens"] >= 1:
            state["tokens"] -= 1
            return True
        return False

    return allow


allow = make_bucket(capacity=3, rate=1)
times = [0, 0, 0, 0, 0, 1, 1, 3, 3, 3, 3]
print("".join("+" if allow(t) else "-" for t in times))
```

```text
+++--+-++--
```

`+` geçen, `-` geri çevrilen istek. 0. saniyedeki beş isteğin ilk üçü
kovadaki üç jetonu harcadı; 1. saniyede bir jeton gelmişti, ikinci istek
yine geri çevrildi; 3. saniyede iki saniyelik birikimle iki istek geçti.
Kova kısa patlamalara izin verir ama uzun sürede ortalama hızı `rate`'te
tutar. Geri çevrilen isteğe `429 Too Many Requests` döner, istersen
`Retry-After` başlığıyla.

Sınır yalnızca istek sayısı için değil: gövdenin boyutu, bir sayfada
dönecek kayıt sayısı (`?limit=100000`) ve tek bir isteğin çalıştıracağı iş
de sınırlanır. API Security Top 10'da bu başlığın adı **sınırsız kaynak
tüketimi**dir.

## API anahtarı

Sunucudan sunucuya konuşan API'lerde istemci çoğunlukla bir **API
anahtarıyla** tanınır. Anahtar bir paroladır ve parola gibi korunur:
sunucu anahtarın kendisini değil özetini saklar, karşılaştırmayı sabit
sürede yapar:

```python
import hashlib
import hmac

stored = hashlib.sha256(b"k_demo_7f3a").hexdigest()


def check_key(given):
    digest = hashlib.sha256(given.encode()).hexdigest()
    return hmac.compare_digest(digest, stored)


print(stored[:16])
print(check_key("k_demo_7f3a"), check_key("k_demo_0000"))
```

```text
87afbccd80d0a41c
True False
```

Örnekteki anahtar okunabilsin diye kısa; gerçek anahtar
`secrets.token_urlsafe(32)` gibi uzun ve rastgele üretilir. Uzun rastgele
bir anahtar tahmin edilemediği için parolanın aksine yavaş özete
(`pbkdf2`) gerek yoktur; tek bir SHA-256 yeter. `hmac.compare_digest`
karşılaştırmanın süresinin, kaçıncı karakterde ayrıştığına bağlı olmasını
engeller.

Anahtar adresin içinde değil başlıkta gönderilir (`Authorization`):
adresler sunucu günlüklerine, tarayıcı geçmişine ve vekil sunuculara
düşer.

## İsteği imzalamak

Anahtar yalnızca "kim" sorusunu cevaplar. İsteğin yolda **değişmediğini**
ve **yeniden oynatılmadığını** göstermek için istek, iki tarafın bildiği
bir sırla imzalanır (Kriptografi modülündeki HMAC). İmzaya zaman da girer;
sunucu eski isteği kabul etmez:

```python
import hashlib
import hmac

SECRET = b"shared-demo-secret"


def sign(ts, method, path, body):
    message = f"{ts}\n{method}\n{path}\n{body}".encode()
    return hmac.new(SECRET, message, hashlib.sha256).hexdigest()


def verify(ts, now, method, path, body, signature):
    if abs(now - ts) > 300:
        return "expired"
    expected = sign(ts, method, path, body)
    if not hmac.compare_digest(expected, signature):
        return "bad signature"
    return "ok"


sig = sign(1000, "POST", "/transfer", '{"amount": 10}')
print(verify(1000, 1030, "POST", "/transfer", '{"amount": 10}', sig))
print(verify(1000, 1030, "POST", "/transfer", '{"amount": 99}', sig))
print(verify(1000, 2000, "POST", "/transfer", '{"amount": 10}', sig))
```

```text
ok
bad signature
expired
```

Gövdedeki tutar değişince imza tutmadı; aynı istek 1000 saniye sonra
gönderilince süresi geçmiş sayıldı. 300 saniyelik pencere iki makinenin
saatleri arasındaki küçük farka pay bırakır. Pencerenin içinde aynı
isteğin ikinci kez gelmesini de engellemek için istekte bir kez
kullanılacak rastgele bir değer (**nonce**) bulunur ve sunucu gördüklerini
pencere boyunca hatırlar.

## Hata cevapları

Bir API hatayı istemciye anlatmalı ama iç ayrıntıyı vermemeli. Yığın
dökümü, veritabanı hata metni ya da dosya yolu saldırgana sistemin içini
gösterir. İstemciye kısa bir kod ve mesaj (`{"error": "not_found"}`),
günlüğe ayrıntı gider; ikisini birbirine bağlamak için cevaba bir istek
kimliği eklenebilir.

## Özet

- Kimlik doğrulama "kim", yetkilendirme "bu nesne onun mu" sorusunu
  cevaplar; ikincisi **her** uç noktada, her nesne için sorulur.
- Girişte ve çıkışta alanlar **izin listesiyle** seçilir.
- İstek sayısı, gövde boyutu ve sayfa büyüklüğü sınırlanır; kova
  algoritması patlamaya izin verip ortalamayı tutar.
- API anahtarı uzun ve rastgele üretilir, özeti saklanır, başlıkta
  gönderilir, sabit sürede karşılaştırılır.
- İmza (HMAC + zaman + nonce) değiştirilmiş ve yeniden oynatılmış isteği
  yakalar.
