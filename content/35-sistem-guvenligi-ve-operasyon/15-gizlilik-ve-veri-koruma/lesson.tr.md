# Gizlilik ve Veri Koruma (KVKK, GDPR)

Güvenlik veriyi **yetkisiz** kişilerden korur. **Gizlilik** (privacy) bir
adım öteye bakar: verinin **yetkili** ellerde bile nasıl kullanıldığına.
Bir şirket müşterisinin verisini kusursuz bir güvenlikle saklayabilir ama
o veriyi müşterinin hiç onaylamadığı bir iş için kullanıyorsa gizliliği
ihlal etmiş olur.

Kişisel verinin korunması birçok ülkede yasayla düzenlenir. Türkiye'de
**KVKK** (Kişisel Verilerin Korunması Kanunu), Avrupa Birliği'nde **GDPR**
(Genel Veri Koruma Tüzüğü) bu alanın temel düzenlemeleridir. İkisi de aynı
temel fikirlere dayanır. Bu bölüm o fikirleri ve onları koda dökmenin
yollarını anlatıyor; hukuki tavsiye değildir. Bütün kişiler ve kayıtlar
uydurmadır.

## Kişisel veri nedir?

**Kişisel veri**, kimliği belirli ya da **belirlenebilir** bir gerçek kişiyle
ilgili her bilgidir: ad, e-posta, telefon, adres, bir cihaz kimliği, hatta
başka bilgilerle birleşince kişiyi gösteren bir yaş ve posta kodu. Bazı
veriler **özel nitelikli** (hassas) sayılır ve daha sıkı korunur: sağlık,
biyometrik ve genetik veri, din, siyasi görüş gibi.

| Rol | Kim? |
|---|---|
| **İlgili kişi** (data subject) | Verisi işlenen kişi |
| **Veri sorumlusu** (controller) | Verinin neden ve nasıl işleneceğine karar veren |
| **Veri işleyen** (processor) | Veri sorumlusu adına veriyi işleyen (ör. bir bulut hizmeti) |

## Temel ilkeler

| İlke | Kısaca |
|---|---|
| Hukuka uygunluk ve şeffaflık | Bir hukuki dayanakla ve kişiye açıkça anlatılarak işlemek |
| Amaçla sınırlılık | Belirli bir amaç için toplanan veriyi başka işe kullanmamak |
| Veri en aza indirme | Amaç için gereken kadar veri toplamak |
| Doğruluk | Veriyi doğru ve güncel tutmak |
| Saklama sınırlaması | Gerekenden uzun saklamamak |
| Güvenlik | Veriyi uygun teknik ve idari önlemlerle korumak |

Bu ilkelerin çoğu doğrudan koda dönüşebilir.

## Veri en aza indirme

Toplanmayan veri sızdırılamaz. Bir formun her alanı, "bu amaç için gerçekten
gerekli mi?" sorusundan geçer:

```python
FORM = {
    "name": "Ada",
    "email": "ada@example.org",
    "phone": "555-0100",
    "birth_date": "1990-05-01",
    "favourite_colour": "green",
}
NEEDED = {"newsletter": {"email"}, "delivery": {"name", "phone", "email"}}
for purpose, fields in NEEDED.items():
    kept = sorted(k for k in FORM if k in fields)
    dropped = sorted(set(FORM) - fields)
    print(purpose, "keeps", kept)
    print("  drops", dropped)
```

```text
newsletter keeps ['email']
  drops ['birth_date', 'favourite_colour', 'name', 'phone']
delivery keeps ['email', 'name', 'phone']
  drops ['birth_date', 'favourite_colour']
```

Bülten için yalnızca e-posta gerekiyor; teslimat için ad, telefon ve
e-posta. Doğum tarihi ve sevilen renk hiçbir amaç için gerekmiyor:
toplanmamalı. Veri en aza indirme hem yasal bir ilke hem de en ucuz
güvenlik önlemidir.

## Takma ad: anahtarlı özet

Analiz için kişinin kim olduğu değil, aynı kişinin kayıtlarının
birleştirilebilmesi gerekebilir. **Takma ad** (pseudonymisation),
doğrudan tanıtıcıyı (e-posta gibi) başka bir değerle değiştirir. Düz bir
özet bunun için yetmez: olası e-postalar tek tek özetlenip karşılaştırılarak
geri bulunabilir. Bu yüzden **gizli anahtarlı** bir özet (HMAC, Mesaj
Doğrulama: HMAC bölümü) kullanılır:

```python
import hashlib
import hmac

KEY = b"kept-in-the-vault"


def pseudonym(value):
    return hmac.new(KEY, value.encode(), hashlib.sha256).hexdigest()[:12]


print(pseudonym("ada@example.org"))
print(pseudonym("ada@example.org") == pseudonym("ada@example.org"))
print(pseudonym("bob@example.org"))
```

```text
1a790762043a
True
586be60649d3
```

Aynı e-posta her zaman aynı takma adı veriyor, böylece kayıtlar
birleştirilebiliyor; farklı kişiler farklı takma ad alıyor. Anahtarı
bilmeyen, takma addan e-postaya dönemez. Ama anahtar elinde olan
dönebildiği için takma adlı veri **hâlâ kişisel veridir**; yalnızca
riski azaltır. Kimseyi, hiçbir ek bilgiyle bir daha belirleyemeyen veriye
**anonim** veri denir ve bunu sağlamak sanıldığından zordur.

## Anonim sanılan veri: k-anonimlik

Adları silmek veriyi anonim yapmaz. Yaş ve posta kodu gibi **dolaylı
tanıtıcılar** birleşince bir kişiyi tek başına gösterebilir. **k-anonimlik**,
dolaylı tanıtıcıları aynı olan her grubun en az **k** kişiden oluşmasını
ister. Yaşları on yıllık aralıklara, posta kodlarını ilk üç haneye
genelleştirip ölçelim:

```python
from collections import Counter

ROWS = [
    {"age": 34, "zip": "34710", "illness": "flu"},
    {"age": 36, "zip": "34712", "illness": "asthma"},
    {"age": 35, "zip": "34718", "illness": "flu"},
    {"age": 52, "zip": "06420", "illness": "diabetes"},
    {"age": 58, "zip": "06425", "illness": "flu"},
    {"age": 41, "zip": "35210", "illness": "asthma"},
]


def generalise(row):
    decade = row["age"] // 10 * 10
    return (f"{decade}-{decade + 9}", row["zip"][:3] + "**")


groups = Counter(generalise(r) for r in ROWS)
for key, size in groups.items():
    print(key, size)
print("k =", min(groups.values()))
```

```text
('30-39', '347**') 3
('50-59', '064**') 2
('40-49', '352**') 1
k = 1
```

İki grupta birden çok kişi var ama `40-49` yaşında ve `352**` bölgesinde
oturan tek bir kişi kaldı: k = 1. Bu kişiyi tanıyan biri, adı
silinmiş olsa da onun hastalığını öğrenebilir. Sağlık verisi özel nitelikli
olduğu için bu ciddi bir ihlaldir. Çözüm daha fazla genelleştirme ya da
küçük grupları yayından çıkarmaktır.

## Saklama sınırlaması

Her verinin bir amacı, her amacın bir saklama süresi vardır. Süresi dolan
veri silinir ya da anonimleştirilir. Aşağıdaki süreler yalnızca örnektir,
yasal süre değildir:

```python
from datetime import date

TODAY = date(2026, 11, 1)
RETENTION = {"marketing": 365, "invoice": 3650, "support": 730}
RECORDS = [
    ("r1", "marketing", date(2025, 6, 1)),
    ("r2", "invoice", date(2019, 2, 1)),
    ("r3", "support", date(2025, 1, 10)),
    ("r4", "marketing", date(2026, 3, 3)),
]
for rid, purpose, created in RECORDS:
    age = (TODAY - created).days
    print(rid, purpose, age, "delete" if age > RETENTION[purpose] else "keep")
```

```text
r1 marketing 518 delete
r2 invoice 2830 keep
r3 support 660 keep
r4 marketing 243 keep
```

Aynı türden iki kayıt farklı sonuç aldı, çünkü yaşları farklı. Pazarlama
için bir yıldan eski kayıt silinmeli; fatura gibi yasal olarak saklanması
gereken kayıt daha uzun kalır.

## İlgili kişinin hakları

Yasalar kişiye kendi verisi üzerinde haklar tanır: verisinin işlenip
işlenmediğini ve hangi verisinin tutulduğunu **öğrenme**, yanlışsa
**düzeltme**, koşullar varsa **silinmesini isteme**, işlemeye **itiraz
etme**. Bir kişinin "bende hangi verim var?" sorusunu cevaplamak, verinin
nerede durduğunu bilmeyi gerektirir:

```python
TABLES = {
    "customers": [{"email": "ada@example.org"}, {"email": "bob@example.org"}],
    "orders": [{"email": "ada@example.org"}, {"email": "ada@example.org"}],
    "newsletter": [{"email": "bob@example.org"}],
}
person = "ada@example.org"
for table, rows in sorted(TABLES.items()):
    found = sum(1 for row in rows if row["email"] == person)
    if found:
        print(table, found)
```

```text
customers 1
orders 2
```

Verinin hangi tablolarda, hangi sistemlerde ve hangi yedeklerde durduğunu
gösteren bir **veri envanteri** olmadan bu soru güvenle cevaplanamaz.

## İhlal olunca

Kişisel veri sızdığında veri sorumlusu, yasaların belirlediği kısa süre
içinde yetkili kuruma, gerekirse ilgili kişilere bildirim yapar. Bunun
nasıl yapılacağı Olay Müdahalesi bölümündeki iletişim planının bir
parçasıdır.

## Özet

- **Gizlilik**, verinin yetkili ellerde nasıl kullanıldığıyla ilgilidir;
  KVKK ve GDPR aynı temel ilkelere dayanır.
- **Kişisel veri**, belirlenebilir bir kişiye dair her bilgidir; sağlık gibi
  veriler özel niteliklidir.
- İlkeler: amaçla sınırlılık, **veri en aza indirme**, doğruluk,
  **saklama sınırlaması**, güvenlik.
- **Takma ad** riski azaltır ama veri kişisel kalır; düz özet değil
  anahtarlı özet kullanılır.
- Adı silmek anonimleştirmek değildir: **k-anonimlik** dolaylı
  tanıtıcıları ölçer.
- İlgili kişinin hakları için **veri envanteri** gerekir.
