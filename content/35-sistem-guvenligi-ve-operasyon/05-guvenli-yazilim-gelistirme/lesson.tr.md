# Güvenli Yazılım Geliştirme (SDLC)

Şimdiye kadar tek tek açıkları ve onlara karşı önlemleri gördük. Ama
güvenli bir yazılım, yayından bir gün önce yapılan bir "güvenlik
kontrolüyle" ortaya çıkmaz. Güvenlik, yazılımın fikir aşamasından
emekliye ayrılmasına kadar her adımına yayılmış bir **süreçtir**.

Yazılımın baştan sona geçirdiği adımlara **yazılım geliştirme yaşam
döngüsü** (Software Development Life Cycle, SDLC) denir. Bu döngünün her
adımına güvenlik işi eklenmiş hâline de **güvenli SDLC** denir. Bu bölüm
o adımları ve her adımda yapılan işi, küçük Python örnekleriyle anlatıyor.

## Döngünün adımları

<figure class="fig"><div class="flow">
  <span class="node">Gereksinim</span><span class="arrow">→</span>
  <span class="node">Tasarım</span><span class="arrow">→</span>
  <span class="node">Kodlama</span><span class="arrow">→</span>
  <span class="node">Doğrulama</span><span class="arrow">→</span>
  <span class="node ok">Yayın ve bakım</span>
</div><figcaption>Güvenlik her adımda vardır; yalnızca sondaki bir denetimde değil.</figcaption></figure>

| Adım | Güvenlik işi |
|---|---|
| **Gereksinim** | Güvenlik gereksinimlerini yazmak: kim neye erişir, hangi veri gizli, hangi yasa geçerli |
| **Tasarım** | Tehdit modellemek (Tehdit Modelleme ve STRIDE bölümü), güvenli varsayılanları seçmek |
| **Kodlama** | Güvenli kodlama kuralları, girdi doğrulama, kod inceleme |
| **Doğrulama** | Güvenlik testleri, statik analiz, bağımlılık taraması |
| **Yayın ve bakım** | Yayın kapısı, yama, izleme, olaylara müdahale |

Bir hatayı ne kadar erken bulursan düzeltmesi o kadar ucuzdur: tasarımda
fark edilen bir yetki eksikliği bir çizimi değiştirmektir, yayından sonra
fark edilen aynı eksiklik bir olaydır. Güvenlik işini döngünün başına doğru
çekmeye **sola kaydırmak** (shift left) denir.

## İlke 1: Güvenli başarısız ol

Bir denetim beklenmedik bir hatayla karşılaşırsa ne olmalı? İki seçenek
var: **açık başarısızlık** (fail open, hata olunca izin ver) ya da
**kapalı başarısızlık** (fail closed, hata olunca reddet).

```python
def lookup_role(user):
    roles = {"ada": "admin", "bob": "user"}
    return roles[user]


def is_admin_fail_open(user):
    try:
        return lookup_role(user) == "admin"
    except Exception:
        return True


def is_admin_fail_closed(user):
    try:
        return lookup_role(user) == "admin"
    except KeyError:
        return False


print(is_admin_fail_open("mallory"))
print(is_admin_fail_closed("mallory"))
```

```text
True
False
```

Kayıtlı olmayan `mallory` için rol bulunamadı. Açık başarısız olan sürüm
bu hatayı "yönetici" olarak yorumladı; kapalı başarısız olan reddetti.
Güvenlik denetimlerinde kural hep aynıdır: **şüphede reddet**. Ayrıca
`except Exception` her hatayı yuttuğu için başka hataları da gizler; yalnızca
beklenen hata (`KeyError`) yakalanır.

## İlke 2: Güvenli varsayılanlar

Bir programın ayarları verilmediğinde ne olacağı, güvenliğin büyük kısmını
belirler. Çünkü çoğu kurulum varsayılanları hiç değiştirmez. Varsayılanlar
bu yüzden **güvenli** seçilir ve kullanıcının verdiği ayarlar yalnızca
tanınan anahtarlar için uygulanır:

```python
DEFAULTS = {"debug": False, "tls": True, "session_minutes": 30}


def load_config(user_config):
    config = dict(DEFAULTS)
    for key, value in user_config.items():
        if key in DEFAULTS:
            config[key] = value
    return config


print(load_config({}))
print(load_config({"debug": True, "colour": "red"}))
```

```text
{'debug': False, 'tls': True, 'session_minutes': 30}
{'debug': True, 'tls': True, 'session_minutes': 30}
```

Hiç ayar verilmeyince hata ayıklama kapalı, şifreli bağlantı açık geliyor.
Tanınmayan `colour` anahtarı sessizce atlandı. Hata ayıklama kipi gibi
tehlikeli bir ayar ancak **açıkça** istenince açılır: güvenli olmayan şey
bilinçli bir seçim olmalıdır, unutulmuş bir varsayılan değil.

## İlke 3: Girdiyi doğrula

Dışarıdan gelen her veri (form, dosya, istek) güvenilmezdir. Doğrulama
**izin listesiyle** yapılır: neyin geçerli olduğu tarif edilir, geri kalan
her şey reddedilir.

```python
def parse_quantity(text):
    if not text.isdigit():
        return None
    value = int(text)
    if not 1 <= value <= 100:
        return None
    return value


for text in ["3", "0", "250", "-1", "2e3", " 4", ""]:
    print(repr(text), parse_quantity(text))
```

```text
'3' 3
'0' None
'250' None
'-1' None
'2e3' None
' 4' None
'' None
```

Yalnızca `3` geçti. Sıfır ve 250 aralık dışında; eksi işaretli, bilimsel
gösterimli, boşluklu ve boş girdi biçim denetiminde kaldı. "Kötü
karakterleri ayıklamak" (kara liste) yerine "iyi olanı tarif etmek" daha
güvenlidir, çünkü kara listeye bir şey eklemeyi unutmak her zaman
mümkündür. Girdi doğrulamanın ayrıntısı Girdi Doğrulama ve Çıktı Kodlama
bölümündedir.

## Doğrulama: güvenlik testleri

Güvenlik gereksinimleri test olarak yazılırsa, her değişiklikten sonra
kendiliğinden denetlenir. Güvenlik testlerinin en değerlisi **"olmamalı"**
durumlarıdır: yalnızca yazarın silebildiğini değil, yabancının
silemediğini de sınamak.

```python
def can_delete(user, post):
    return user["role"] == "admin" or post["author"] == user["name"]


TESTS = [
    ("author can delete", {"name": "ada", "role": "user"}, {"author": "ada"}, True),
    ("stranger cannot delete", {"name": "bob", "role": "user"}, {"author": "ada"}, False),
    ("admin can delete", {"name": "eve", "role": "admin"}, {"author": "ada"}, True),
]
for name, user, post, expected in TESTS:
    result = "pass" if can_delete(user, post) == expected else "FAIL"
    print(f"{result}: {name}")
```

```text
pass: author can delete
pass: stranger cannot delete
pass: admin can delete
```

Üç test de geçti. Biri ileride `can_delete`'i değiştirip sahiplik
denetimini bozarsa, "stranger cannot delete" testi hemen düşer ve hata
yayına çıkmadan yakalanır.

## Yayın kapısı

Döngünün sonunda bir **yayın kapısı** (release gate) durur: belirli
güvenlik işleri tamamlanmadan sürüm çıkmaz. Kapı bir kontrol listesidir ve
derleme hattında (CI) kendiliğinden denetlenir:

```python
CHECKLIST = {
    "threat_model_reviewed": True,
    "security_tests_pass": True,
    "dependencies_scanned": False,
    "secrets_scan_clean": True,
}
blockers = sorted(item for item, done in CHECKLIST.items() if not done)
print("release blocked" if blockers else "release ok")
print(blockers)
```

```text
release blocked
['dependencies_scanned']
```

Bağımlılık taraması yapılmadığı için sürüm durdu. Kapının değeri,
**istisnasız** uygulanmasındadır: "bu seferlik" geçilen kapı, kapı
olmaktan çıkar.

## Özet

- Güvenlik, **SDLC**'nin her adımına yayılmış bir süreçtir; en sonda
  yapılan tek bir kontrol değildir.
- Hata ne kadar erken bulunursa o kadar ucuzdur: **sola kaydır**.
- **Güvenli başarısız ol:** hata olunca reddet; yalnızca beklenen hatayı
  yakala.
- **Güvenli varsayılanlar:** tehlikeli ayar ancak açıkça istenince açılır.
- **Girdiyi izin listesiyle doğrula:** iyiyi tarif et, kalanı reddet.
- **Güvenlik testleri** "olmamalı" durumlarını da sınar; **yayın kapısı**
  istisnasız uygulanır.
