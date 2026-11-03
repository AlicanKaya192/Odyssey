# Bulut Güvenliği

Bugün birçok sistem kurumun kendi odasındaki sunucularda değil, bir **bulut
sağlayıcısının** veri merkezlerinde çalışır. Sunucuyu, depolamayı ya da
hazır bir uygulamayı kiralamak hızlıdır ve bakım yükünü azaltır. Ama
güvenlik sorumluluğu ortadan kalkmaz; **paylaşılır**. Bulutta yaşanan
olayların büyük kısmı sağlayıcının bir açığından değil, müşterinin bir
**yapılandırma hatasından** doğar: herkese açık bırakılmış bir depolama
alanı, gereğinden geniş bir yetki, internete açılmış bir yönetim portu.

Bu bölüm paylaşılan sorumluluğu ve en sık yapılandırma hatalarını
denetleyen küçük araçları anlatıyor. Bütün yapılandırmalar sahte sözlükler;
hiçbir bulut hizmetine bağlanılmıyor.

## Paylaşılan sorumluluk

Bulut hizmetleri, sağlayıcının ne kadarını üstlendiğine göre üç modelde
toplanır:

| Model | Kiralanan | Örnek |
|---|---|---|
| **IaaS** (altyapı) | Sanal sunucu, ağ, depolama | Kendi işletim sistemini kurduğun sanal makine |
| **PaaS** (platform) | Uygulamanın çalıştığı ortam | Kodunu yüklediğin uygulama platformu |
| **SaaS** (yazılım) | Hazır uygulama | E-posta ya da belge hizmeti |

Sağlayıcı ne kadar çok üstlenirse müşteriye o kadar az kalır, ama **veri ve
kimlikler** her modelde müşterinindir:

```python
LAYERS = ["data", "identities", "application", "operating system", "network", "physical"]
for model, provider_from in [("IaaS", 4), ("PaaS", 3), ("SaaS", 2)]:
    print(f"{model}: you = {', '.join(LAYERS[:provider_from])}")
```

```text
IaaS: you = data, identities, application, operating system
PaaS: you = data, identities, application
SaaS: you = data, identities
```

SaaS kullanırken bile kimin hangi belgeye erişebildiği, hangi hesabın çok
faktörlü doğrulama kullandığı ve hangi verinin oraya konduğu müşterinin
sorumluluğundadır. "Bulutta, sağlayıcı korur" düşüncesi en yaygın
yanılgıdır.

## Depolama alanları

Bulutta dosyalar genellikle **nesne depolama** alanlarında (bucket)
tutulur. Bir alanın yanlışlıkla **herkese açık** bırakılması, bulutta veri
sızıntılarının en bilinen sebebidir. Denetim, her alanın kimlere açık
olduğuna, ne tür veri tuttuğuna ve şifrelenip şifrelenmediğine bakar:

```python
BUCKETS = [
    {"name": "web-assets", "public": True, "encrypted": True, "data": "public"},
    {"name": "customer-exports", "public": True, "encrypted": False, "data": "personal"},
    {"name": "logs", "public": False, "encrypted": True, "data": "internal"},
]
for b in BUCKETS:
    problems = []
    if b["public"] and b["data"] != "public":
        problems.append("public but holds " + b["data"] + " data")
    if not b["encrypted"]:
        problems.append("not encrypted")
    print(f"{b['name']}: {'; '.join(problems) or 'ok'}")
```

```text
web-assets: ok
customer-exports: public but holds personal data; not encrypted
logs: ok
```

Web sitesinin resimlerinin herkese açık olması doğaldır. Müşteri dışa
aktarımlarının herkese açık ve şifresiz durması ise bir olaydır.
Sağlayıcıların çoğu "herkese açık erişimi engelle" gibi hesap düzeyinde bir
ayar sunar; güvenli varsayılan (Güvenli Yazılım Geliştirme bölümü) bu
ayarın açık olmasıdır.

## Kimlik ve erişim politikaları

Bulutta neyin yapılabileceğini **kimlik ve erişim yönetimi** (IAM)
politikaları belirler. Politika, izin veren (`allow`) ve yasaklayan (`deny`)
ifadelerden oluşur; işlem adlarında `*` joker karakteri kullanılabilir.
Yaygın kurallar: açıkça izin verilmeyen her şey yasaktır ve **yasak her
zaman kazanır**:

```python
from fnmatch import fnmatchcase

POLICY = [
    {"effect": "allow", "action": "storage:Get*"},
    {"effect": "allow", "action": "storage:List*"},
    {"effect": "deny", "action": "storage:GetSecret*"},
]


def allowed(policy, action):
    matches = [s["effect"] for s in policy if fnmatchcase(action, s["action"])]
    if "deny" in matches:
        return False
    return "allow" in matches


for action in ["storage:GetObject", "storage:GetSecretValue", "storage:DeleteObject"]:
    print(action, allowed(POLICY, action))
```

```text
storage:GetObject True
storage:GetSecretValue False
storage:DeleteObject False
```

Nesne okumaya izin var. Sır okuma da `Get*` kalıbına uyuyor ama ayrı bir
yasak ifadesi onu kapattı: yasak kazandı. Silme için hiçbir ifade yok;
varsayılan olarak reddedildi. Joker karakter rahattır ama tehlikelidir:
`storage:*` ya da yalnızca `*` gibi bir izin, En Az Yetki ve Görev Ayrılığı
bölümündeki ilkenin tam tersidir ve incelemede ilk işaretlenen şeydir.

## Ağ kuralları

Bulut sunucularına gelen trafiği **güvenlik grupları** ya da benzeri ağ
kuralları sınırlar (Güvenlik Duvarı bölümü). En sık hata, yönetim
portlarının (uzak bağlantı, veritabanı) bütün internete
(`0.0.0.0/0`) açılmasıdır:

```python
RULES = [
    {"port": 443, "source": "0.0.0.0/0"},
    {"port": 22, "source": "0.0.0.0/0"},
    {"port": 5432, "source": "10.0.0.0/16"},
    {"port": 3389, "source": "0.0.0.0/0"},
]
ADMIN_PORTS = {22, 3389, 5432}
for r in RULES:
    if r["port"] in ADMIN_PORTS and r["source"] == "0.0.0.0/0":
        print("open to the internet:", r["port"])
```

```text
open to the internet: 22
open to the internet: 3389
```

Web portu `443`'ün herkese açık olması amaçtır. Uzak bağlantı portları
`22` ve `3389` ise bütün internete açık: dünyanın her yerinden parola
denemelerine hedef olurlar. Veritabanı yalnızca iç ağdan erişilebilir;
doğrusu budur. Yönetim erişimi VPN ya da benzeri bir ara katmanla ve
belirli adreslerle sınırlanır.

## Kod olarak altyapı

Bulut kaynakları elle tıklanarak değil, bir yapılandırma dosyasıyla
(**kod olarak altyapı**, infrastructure as code) kurulduğunda bütün bu
denetimler kurulumdan **önce** yapılabilir: dosya Kod İnceleme ve Statik
Analiz bölümündeki gibi taranır, herkese açık alan ya da `0.0.0.0/0` gibi
bulgular değişikliği durdurur. Yanlış yapılandırma buluta hiç ulaşmaz.

## Özet

- Bulutta güvenlik **paylaşılır**: sağlayıcı altyapıyı korur, **veri ve
  kimlikler** her modelde müşterinindir.
- Olayların çoğu sağlayıcının açığından değil **yapılandırma hatasından**
  doğar.
- Depolama alanları varsayılan olarak **kapalı** ve şifreli olur.
- IAM'de açıkça izin verilmeyen yasaktır, **yasak kazanır**; geniş joker
  izinlerden kaçınılır.
- Yönetim portları bütün internete açılmaz.
- **Kod olarak altyapı** denetimi kurulumdan önceye taşır.
