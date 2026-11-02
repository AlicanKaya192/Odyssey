# Saldırı Yüzeyi

Bir evin ne kadar çok kapısı ve penceresi varsa, hırsızın deneyebileceği
o kadar çok yer vardır. Bir sistemin **saldırı yüzeyi** (attack surface),
bir saldırganın sisteme veri gönderebildiği, ona ulaşabildiği ya da onu
etkileyebildiği bütün noktaların toplamıdır. Her noktaya **giriş noktası**
(entry point) denir. Yüzey ne kadar büyükse savunulacak yer o kadar çok,
gözden kaçan bir kapının kalma ihtimali o kadar yüksektir.

## Yüzeyin üç türü

| Tür | Giriş noktası örnekleri |
|---|---|
| **Dijital** (digital) | Web sayfaları ve formlar, API uç noktaları, dosya yükleme, açık ağ hizmetleri, yönetim paneli, güncelleme mekanizması, kullanılan dış kütüphaneler |
| **Fiziksel** (physical) | USB girişleri, kilitlenmemiş sunucu odası, kaybolabilecek dizüstü bilgisayarlar, yazıcıda unutulan kâğıtlar |
| **İnsan** (human, social) | E-posta ve telefonla ulaşılabilen çalışanlar, yardım masası, tedarikçiler |

Bu bölüm dijital yüzeye odaklanıyor; insan yüzeyi Sosyal Mühendislik
bölümünün konusu.

## Önce envanter

Bilmediğin bir kapıyı kilitleyemezsin. Saldırı yüzeyini küçültmenin ilk
adımı **envanter** (inventory) çıkarmaktır: hangi sunucular, hangi uç
noktalar, hangi hizmetler var, kim kullanıyor? Bir ekibin kimseye
sormadan açtığı bir test sunucusu ya da unutulmuş eski bir sayfa
(**gölge BT**, shadow IT) en sık rastlanan gözden kaçan kapılardır.

## Her giriş noktası aynı değil

İki soru bir giriş noktasının ne kadar açık olduğunu büyük ölçüde belirler:

- **Kimler ulaşabiliyor?** İnternetteki herkes mi, yalnızca iç ağdakiler
  mi, yalnızca o makinenin başındaki kişi mi?
- **Kimlik doğrulama gerekiyor mu?** Giriş yapmadan kullanılabiliyorsa
  dünyadaki herkes onu deneyebilir.

Bu iki soruyla oyuncak bir puan verelim: internet 3, iç ağ 2, yalnızca
yerel 1; kimlik doğrulama yoksa puan iki katı. Gerçek ölçüm yöntemleri
daha ayrıntılıdır, ama fikir aynıdır.

```python
WEIGHT = {"internet": 3, "internal": 2, "local": 1}
entry_points = [
    ("login page", "internet", True),
    ("search api", "internet", False),
    ("admin panel", "internet", True),
    ("report export", "internal", True),
    ("debug console", "local", False),
]
total = 0
for name, exposure, needs_auth in entry_points:
    score = WEIGHT[exposure] * (1 if needs_auth else 2)
    total += score
    print(f"{name:<14} {exposure:<9} auth={needs_auth!s:<5} score={score}")
print("total:", total)
```

```text
login page     internet  auth=True  score=3
search api     internet  auth=False score=6
admin panel    internet  auth=True  score=3
report export  internal  auth=True  score=2
debug console  local     auth=False score=2
total: 16
```

Bu tablo iki şeyi hemen gösteriyor: giriş gerektirmeyen arama API'si en
açık kapı, ve yönetim paneli internetten ulaşılabiliyor. Yönetim panelinin
herkese açık olması için bir neden yoksa kapatılabilecek ilk yer orası.

## Yüzeyi küçültmek

Saldırı yüzeyini küçültmenin yolları çoğu zaman basittir:

- **Kullanılmayanı kaldır:** eski sayfalar, denenip bırakılmış özellikler,
  hiç çağrılmayan uç noktalar, kurulu ama kullanılmayan paketler.
- **Ulaşılabilirliği daralt:** yönetim paneli yalnızca iç ağdan ya da
  VPN'den; veritabanı internete hiç açık değil.
- **Varsayılanı kapalı yap:** bir özellik gerekiyorsa açılır, gerekmedikçe
  kapalı durur (Güvenlik İlkeleri'ndeki "varsayılan olarak güvenli").
- **Hata ayıklama araçlarını canlı sistemden çıkar:** geliştirme sırasında
  işe yarayan konsollar canlı sistemde bir kapıdır.

Örnekteki sistemde yönetim panelini iç ağa alıp hata ayıklama konsolunu
kaldıralım:

```python
after = [("login page", "internet", True), ("search api", "internet", False),
         ("admin panel", "internal", True), ("report export", "internal", True)]
after_total = sum(WEIGHT[e] * (1 if a else 2) for _, e, a in after)
print("before:", total, "after:", after_total)
print(f"reduced by {(total - after_total) / total:.0%}")
```

```text
before: 16 after: 13
reduced by 19%
```

İki küçük değişiklik yüzeyin puanını %19 küçülttü. Asıl kazanç
puanda değil: internetten ulaşılabilen bir yönetim paneli artık yok.

## Kullanılmayanı bulmak

Hangi uç noktaların gerçekten kullanıldığını kayıtlar (log) söyler. Son
üç ayda hiç istek almamış bir uç nokta büyük ihtimalle unutulmuştur ve
kaldırılmaya adaydır:

```python
hits = {"/login": 5120, "/search": 830, "/grades": 2210,
        "/admin": 4, "/legacy-upload": 0}
print([path for path, count in hits.items() if count == 0])
```

```text
['/legacy-upload']
```

Unutulmuş uç noktalar iki kat tehlikelidir: kimse onları güncellemez ve
kimse onlara saldırı olup olmadığına bakmaz. Eski bir dosya yükleme sayfası,
yeni sayfadaki bütün denetimleri atlatmanın yolu olabilir.

## Yüzey her sürümde değişir

Her yeni özellik yeni bir giriş noktası olabilir. Bu yüzden bir sürümü
yayınlamadan önce yüzeyin **nasıl değiştiğine** bakmak iyi bir alışkanlıktır:
yeni eklenen her uç nokta kod incelemesinde ve tehdit modelinde ayrıca
ele alınır.

```python
v1 = {"/login", "/search", "/grades", "/admin"}
v2 = {"/login", "/search", "/grades", "/admin", "/export", "/debug"}
print("new:", sorted(v2 - v1))
print("removed:", sorted(v1 - v2))
```

```text
new: ['/debug', '/export']
removed: []
```

Yeni sürümde iki uç nokta var. `/export` bilinçli eklenmiş bir özellik
olabilir; `/debug` ise büyük ihtimalle yanlışlıkla canlıya gidiyor. Bu fark
listesi, "bu sürümde neyi incelemeliyiz?" sorusunun cevabıdır.

## Küçük yüzey, gizli yüzey değildir

Saldırı yüzeyini küçültmek, kapıları **kaldırmak** ya da **kilitlemektir**.
Bir kapıyı saklamak (yönetim panelini tahmin edilmesi zor bir adrese
koymak) yüzeyi küçültmez; yalnızca gizlilik yoluyla güvenliktir (Güvenlik
İlkeleri). Adres bir gün sızar, kapı yine oradadır.

## Özet

- **Saldırı yüzeyi**, saldırganın sisteme ulaşabildiği bütün **giriş
  noktalarının** toplamıdır: dijital, fiziksel ve insan.
- İlk adım **envanter**: bilinmeyen kapı kilitlenemez; gölge BT en sık
  gözden kaçandır.
- Bir giriş noktasının açıklığını **kimlerin ulaşabildiği** ve **kimlik
  doğrulama gerekip gerekmediği** belirler.
- Küçültmek için kullanılmayanı kaldır, ulaşılabilirliği daralt,
  varsayılanı kapalı yap.
- Her sürümde yüzeyin farkına bak; saklamak küçültmek değildir.
