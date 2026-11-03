# Bağımlılıklar ve Tedarik Zinciri

Bugün yazılan programların çoğu, kodun büyük kısmını kendisi yazmaz:
paketler (kütüphaneler) kullanır. Bir web uygulaması bir web çatısını, o
çatı bir şablon kütüphanesini, o kütüphane de başka paketleri kullanır.
Senin yazdığın birkaç yüz satırın arkasında başkalarının yazdığı on
binlerce satır çalışır.

Bu paketlerin her biri programın bir parçasıdır ve **açıkları da senin
açığındır**. Bir paketin geliştiricisinden senin bilgisayarına kadar
uzanan yolun tamamına **yazılım tedarik zinciri** (software supply chain)
denir. Bu bölüm o zinciri nasıl koruyacağımızı anlatıyor: sürüm
sabitleme, dolaylı bağımlılıklar, bilinen açıklarla karşılaştırma, benzer
adlı paketler ve özet doğrulama. Örnekler yine oyuncak: gerçek bir paket
indirilmiyor, adlar ve sürümler sözlüklerde duruyor.

## Doğrudan ve dolaylı bağımlılık

Senin açıkça kurduğun pakete **doğrudan bağımlılık**, onun kendi
kullandıklarına **dolaylı bağımlılık** (transitive dependency) denir.
Dolaylı bağımlılıklar çoğu zaman görülmez, ama aynı ölçüde çalışır:

```python
GRAPH = {
    "app": ["web", "db"],
    "web": ["templates", "http"],
    "db": ["http", "pool"],
    "templates": ["escape"],
    "http": [],
    "pool": [],
    "escape": [],
}


def all_deps(graph, root):
    seen = set()
    stack = list(graph[root])
    while stack:
        name = stack.pop()
        if name not in seen:
            seen.add(name)
            stack.extend(graph.get(name, []))
    return seen


print("direct:", len(GRAPH["app"]))
print("all:", len(all_deps(GRAPH, "app")), sorted(all_deps(GRAPH, "app")))
```

```text
direct: 2
all: 6 ['db', 'escape', 'http', 'pool', 'templates', 'web']
```

Uygulama yalnızca 2 paket istedi ama 6 paketle
çalışıyor. `escape` paketini hiç seçmedik, yine de içinde bir açık olsa
bizim uygulamamızda da olurdu. `seen` kümesi aynı paketi (`http` iki yerden
geliyor) bir kez saymayı ve döngülü grafikte sonsuza kadar dönmemeyi
sağlıyor. Kullanılan bütün paketlerin bu listesine **yazılım malzeme
listesi** (Software Bill of Materials, SBOM) denir.

## Sürümü sabitlemek

`requirements.txt` gibi bir dosyada paket sürümü yazılmazsa ya da yalnızca
alt sınır yazılırsa, her kurulum o günün en yeni sürümünü alır. Bugün
çalışan kurulum yarın farklı bir kodla kurulabilir; o yeni sürüm bozuk ya
da kötü niyetli olabilir. Bu yüzden sürümler **sabitlenir** (pinning):

```python
REQUIREMENTS = """numpy==2.1.3
pandas>=2.0
flask
# test tools
pytest==8.3.4
"""
for line in REQUIREMENTS.splitlines():
    line = line.strip()
    if not line or line.startswith("#"):
        continue
    status = "pinned" if "==" in line else "NOT pinned"
    print(f"{line:<14} {status}")
```

```text
numpy==2.1.3   pinned
pandas>=2.0    NOT pinned
flask          NOT pinned
pytest==8.3.4  pinned
```

`pandas>=2.0` ve `flask` sabit değil: her kurulumda başka bir sürüm
gelebilir. Sabitleme, kurulumu **tekrarlanabilir** yapar. Bunun bedeli,
güncellemelerin artık kendiliğinden gelmemesidir; sabitlenmiş sürümler
bilinçli ve düzenli olarak güncellenir (sonraki adım).

## Bilinen açıklarla karşılaştırmak

Paketlerin açıkları, hangi sürümlerin etkilendiğini söyleyen **güvenlik
duyurularıyla** (advisory) yayımlanır: açık hangi sürümde ortaya çıktı,
hangi sürümde düzeltildi. Kurulu sürüm bu aralıktaysa paket etkilenir.
Sürümler, İşletim Sistemi Güvenliği bölümünde gördüğümüz gibi sayı demeti
olarak karşılaştırılır:

```python
def version(text):
    return tuple(int(p) for p in text.split("."))


INSTALLED = {"web": "2.3.1", "http": "1.9.0", "pool": "0.4.2"}
ADVISORIES = [
    ("web", "2.0.0", "2.3.2", "ADV-1"),
    ("http", "1.0.0", "1.8.0", "ADV-2"),
    ("pool", "0.1.0", "0.5.0", "ADV-3"),
]
for name, introduced, fixed, adv in ADVISORIES:
    v = version(INSTALLED[name])
    if version(introduced) <= v < version(fixed):
        print(f"{name} {INSTALLED[name]} affected by {adv}, fix: {fixed}")
```

```text
web 2.3.1 affected by ADV-1, fix: 2.3.2
pool 0.4.2 affected by ADV-3, fix: 0.5.0
```

`web` ve `pool` etkilenen aralıkta; `http` ise zaten düzeltilmiş bir
sürümde. Bunu her gün elle yapmak mümkün değil; **bağımlılık tarama**
araçları (SCA) kurulu paket listesini duyuru veritabanlarıyla
kendiliğinden karşılaştırır ve derleme hattında çalışır.

## Benzer adlı paketler

Tedarik zincirine yapılan saldırıların bir kısmı açık bulmaya bile
uğraşmaz: popüler bir pakete **çok benzeyen adla** zararlı bir paket
yayımlanır ve bir harfi yanlış yazan geliştiricinin onu kurması beklenir.
Buna **yazım hatası avcılığı** (typosquatting) denir. Savunan taraf, yeni
eklenen bir paket adını bilinen popüler adlarla karşılaştırabilir:

```python
import difflib

POPULAR = ["numpy", "pandas", "django", "flask", "pytest"]
for name in ["numpi", "pandas", "flaskk", "djang0", "leftpad"]:
    if name in POPULAR:
        print(name, "ok")
        continue
    close = difflib.get_close_matches(name, POPULAR, n=1, cutoff=0.8)
    print(name, "-> looks like " + close[0] if close else "unknown")
```

```text
numpi -> looks like numpy
pandas ok
flaskk -> looks like flask
djang0 -> looks like django
leftpad unknown
```

`numpi`, `flaskk` ve `djang0` popüler adlara çok yakın: kurulmadan önce
bir insanın bakması gerekir. `leftpad` hiçbirine benzemiyor; benzememek
güvenli olduğu anlamına gelmez, yalnızca bu denetimin konusu değildir.
`difflib`'in benzerlik oranı 0 ile 1 arasındadır; `cutoff` eşiği, Yetki
Yükseltme bölümündeki eşik gibi, yanlış alarm ile kaçırma arasındaki
dengeyi belirler.

İlgili bir saldırı da **bağımlılık karışıklığıdır** (dependency
confusion): bir kurumun iç paketiyle aynı adda bir paket herkese açık
depoya yayımlanır ve yanlış yapılandırılmış kurulum araçları açık depodaki
sürümü seçer. Savunması, iç paketlerin hangi depodan geleceğini açıkça
yazmaktır.

## Özet doğrulama ve kilit dosyası

Sürümü sabitlemek, **hangi** sürümün kurulacağını söyler; ama indirilen
dosyanın gerçekten o sürüm olduğunu kanıtlamaz. **Kilit dosyası** (lock
file) her paketin sürümünün yanında dosyasının **SHA-256 özetini** de
tutar. Kurulumda indirilen dosyanın özeti hesaplanır ve karşılaştırılır
(Özet Fonksiyonları bölümü):

```python
import hashlib


def digest(data):
    return hashlib.sha256(data).hexdigest()


LOCK = {"web-2.3.2.zip": digest(b"web package v2.3.2")}
print(digest(b"web package v2.3.2") == LOCK["web-2.3.2.zip"])
print(digest(b"web package v2.3.2 + extra") == LOCK["web-2.3.2.zip"])
```

```text
True
False
```

Dosyaya tek bir şey eklenince özet tutmadı ve kurulum durdurulur. pip'te
bu `--require-hashes` seçeneğiyle yapılır: özeti olmayan ya da tutmayan
hiçbir paket kurulmaz.

## Önlem listesi

| Tehdit | Önlem |
|---|---|
| Bilinen açıklı sürüm | Bağımlılık taraması, düzenli güncelleme |
| Kurulumdan kuruluma değişen sürüm | Sürüm sabitleme, kilit dosyası |
| Yolda ya da depoda değiştirilmiş dosya | Kilit dosyasında özet doğrulama |
| Benzer adlı zararlı paket | Yeni bağımlılığı insan inceler, ad benzerliği denetimi |
| İç paket adının açık depoda taklidi | İç paketlerin deposunu açıkça yaz |
| Gereksiz paket | Az bağımlılık: her paket bir risk |

## Özet

- Programın **tedarik zinciri**, kullandığı bütün paketlerdir;
  **dolaylı** bağımlılıklar da dahil.
- **SBOM:** kullanılan bütün paketlerin listesi.
- Sürümleri **sabitle**; sabitlenmiş sürümleri bilinçli ve düzenli
  güncelle.
- **Güvenlik duyurularıyla** karşılaştır: kurulu sürüm, açığın ortaya
  çıktığı sürümle düzeltildiği sürüm arasındaysa paket etkilenir.
- **Typosquatting** ve **bağımlılık karışıklığı** adları hedef alır; yeni
  paketi insan inceler.
- **Kilit dosyasındaki özet**, indirilen dosyanın değişmediğini kanıtlar.
