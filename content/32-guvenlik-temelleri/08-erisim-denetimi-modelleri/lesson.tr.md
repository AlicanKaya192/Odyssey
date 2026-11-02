# Erişim Denetimi Modelleri

Bir önceki bölümde izinlerin bir matriste durduğunu gördük. Peki o matrisi
**kim doldurur** ve **neye bakarak**? Bu sorunun dört büyük cevabı var; her
birine bir **erişim denetimi modeli** (access control model) denir:

| Model | Kim karar verir? | Neye bakarak? |
|---|---|---|
| **DAC** (isteğe bağlı) | Nesnenin sahibi | Sahibin isteği |
| **MAC** (zorunlu) | Sistem, merkezî kural | Gizlilik etiketleri |
| **RBAC** (rol tabanlı) | Yönetici, rolleri tanımlayarak | Kişinin rolü |
| **ABAC** (öznitelik tabanlı) | Yazılı kurallar | Özne, nesne, eylem ve ortamın özellikleri |

## DAC: sahibi karar verir

**İsteğe bağlı erişim denetimi** (discretionary access control, DAC):
her nesnenin bir **sahibi** (owner) vardır ve kimin erişeceğine sahibi
karar verir. Bilgisayarındaki dosyaları birileriyle paylaşmak, bir belgeyi
"bağlantıya sahip herkes görebilir" yapmak DAC'tir.

```python
files = {"report.txt": {"owner": "ada", "readers": {"ada"}}}


def share(user, name, other):
    entry = files[name]
    if user != entry["owner"]:
        return "denied"
    entry["readers"].add(other)
    return "shared"


print(share("alan", "report.txt", "alan"))
print(share("ada", "report.txt", "alan"))
print(sorted(files["report.txt"]["readers"]))
```

```text
denied
shared
['ada', 'alan']
```

Alan kendine izin veremedi; dosyanın sahibi Ada verdi. DAC esnek ve
kolaydır, ama iki zayıflığı var:

- **Sahip yanılabilir:** gizli bir belgeyi yanlış kişiyle paylaşmak tek bir
  tıklamadır. Kurum bunu engelleyemez; karar kişinindir.
- **Programlar sahibin yetkisiyle çalışır:** Ada'nın açtığı bir program,
  Ada'nın okuyabildiği her şeyi okuyabilir. Ada'nın bilgisayarına giren
  zararlı bir program da öyle. Buna **Truva atı sorunu** (Trojan horse
  problem) denir.

## MAC: kuralı sistem koyar

**Zorunlu erişim denetimi** (mandatory access control, MAC): erişim
kararını kişi değil, sistem genelindeki bir kural verir ve kullanıcılar
bu kuralı değiştiremez. Askeri ve devlet sistemlerinden doğmuştur.

Her nesneye bir **gizlilik derecesi** (classification), her kişiye bir
**yetki düzeyi** (clearance) verilir; ikisi aynı sıralı listeden gelir:
`public` < `internal` < `secret` < `top-secret`.

Gizliliği korumak için en bilinen kural **Bell-LaPadula** modelidir:

- **Yukarı okuma yok** (no read up): kişi yalnızca kendi düzeyindeki ya da
  daha aşağıdaki belgeleri okuyabilir.
- **Aşağı yazma yok** (no write down): kişi yalnızca kendi düzeyine ya da
  daha yukarıya yazabilir.

İkinci kural ilk bakışta tuhaf görünür: neden "secret" düzeyindeki biri
"public" bir belgeye yazamasın? Çünkü yazabilseydi, okuduğu gizli bilgiyi
herkese açık bir belgeye kopyalayabilirdi; yanlışlıkla ya da içindeki bir
Truva atı yüzünden. Kural sızıntının **yolunu** kapatır.

```python
LEVELS = ["public", "internal", "secret", "top-secret"]


def blp(subject, obj, action):
    s, o = LEVELS.index(subject), LEVELS.index(obj)
    return s >= o if action == "read" else s <= o


for obj in LEVELS:
    can_read = blp("secret", obj, "read")
    can_write = blp("secret", obj, "write")
    print(f"{obj:<11}", "read:", can_read, "write:", can_write)
```

```text
public      read: True write: False
internal    read: True write: False
secret      read: True write: True
top-secret  read: False write: True
```

"secret" düzeyindeki biri aşağıyı okuyabiliyor, yukarıyı okuyamıyor;
yukarıya yazabiliyor, aşağıya yazamıyor. Kendi düzeyinde ikisi de serbest.

Bütünlüğü korumak için bunun **tersi** olan **Biba** modeli kullanılır:
**aşağı okuma yok** (düşük güvenilirlikteki veri yüksek güvenilirlikteki
kararı kirletmesin) ve **yukarı yazma yok** (düşük güvenilirlikteki biri
yüksek güvenilirlikteki veriyi değiştiremesin). Kontrol odasının
yazılımı internetten gelen bir dosyayı okuyup ona göre davranmamalı.

MAC çok güçlüdür ama katıdır: her nesneyi etiketlemek ve her kişiye düzey
vermek zahmetlidir, iş akışları zorlanır. Bugün işletim sistemlerinin bir
kısmı, önemli bölümleri korumak için MAC'in bir biçimini DAC'in yanında
kullanır.

## RBAC: rolüne göre

**Rol tabanlı erişim denetimi** (role-based access control, RBAC):
izinler kişilere değil **rollere** verilir; kişilere de rol atanır. Bir
okulda "öğretmen", "öğrenci", "yönetici" rolleri gibi:

```python
role_perms = {
    "teacher": {"grades:read", "grades:write"},
    "student": {"grades:read_own"},
    "admin": {"users:manage"},
}
user_roles = {"ada": {"teacher"}, "alan": {"student"}, "grace": {"teacher", "admin"}}


def permissions(user):
    perms = set()
    for role in user_roles.get(user, set()):
        perms |= role_perms[role]
    return sorted(perms)


for user in ["ada", "alan", "grace"]:
    print(user, permissions(user))
```

```text
ada ['grades:read', 'grades:write']
alan ['grades:read_own']
grace ['grades:read', 'grades:write', 'users:manage']
```

RBAC'in gücü yönetimin kolaylığıdır. Yeni bir öğretmen geldiğinde ona tek
bir rol verilir; bir öğretmen yönetici olunca rolü eklenir; işten
ayrılınca rolleri alınır ve bütün izinleri birlikte gider. Kişi kişi izin
dağıtmak yerine birkaç rol yönetilir.

Roller birbirinden **miras alabilir** (role hierarchy): "baş öğretmen"
rolü "öğretmen" rolünün bütün izinlerini alır, üstüne birkaç tane daha
ekler. Zayıf yanı **rol patlamasıdır** (role explosion): her istisna için
yeni bir rol açılırsa ("yalnızca 9-B'nin notlarını gören öğretmen") roller
yüzlerce olur ve yönetimi zorlaşır.

## ABAC: özelliklere göre

**Öznitelik tabanlı erişim denetimi** (attribute-based access control,
ABAC): karar, bir kurala göre **özelliklerden** (attribute) verilir:

- **Öznenin** özellikleri: rol, bölüm, yetki düzeyi.
- **Nesnenin** özellikleri: sahibi, bölümü, gizlilik derecesi.
- **Eylem:** okumak mı, yazmak mı?
- **Ortam:** saat, konum, kullanılan cihaz.

Bir hastanede "hemşire kendi bölümündeki hastaların kayıtlarını mesai
saatinde okuyabilir" kuralı rolle tek başına yazılamaz; ABAC ile yazılır:

```python
def abac(subject, resource, action, hour):
    same_dept = subject["dept"] == resource["dept"]
    if subject["role"] == "doctor":
        return same_dept
    if subject["role"] == "nurse":
        return same_dept and action == "read" and 7 <= hour < 19
    return False


nurse = {"role": "nurse", "dept": "cardiology"}
record = {"dept": "cardiology"}
for action, hour in [("read", 10), ("read", 23), ("write", 10)]:
    print(action, hour, abac(nurse, record, action, hour))
```

```text
read 10 True
read 23 False
write 10 False
```

ABAC çok esnektir ve rol patlamasını önler. Bedeli karmaşıklıktır: kurallar
çoğaldıkça "kim neye erişebilir?" sorusunu cevaplamak zorlaşır ve kuralları
denetlemek gerekir. Rol de bir öznitelik olduğu için ABAC, RBAC'i içine
alabilir; gerçek sistemlerin çoğu tam da bunu yapar: temel izinler rolle,
ince kurallar özniteliklerle.

## Özet

- **DAC:** sahip karar verir; esnek ama sahip yanılabilir ve programlar
  sahibin bütün yetkisini taşır.
- **MAC:** sistem etiketlere göre karar verir. **Bell-LaPadula**
  gizlilik için (yukarı okuma yok, aşağı yazma yok), **Biba** bütünlük için
  (tersi).
- **RBAC:** izin role, rol kişiye; yönetimi kolay, istisnalar rol
  patlamasına yol açar.
- **ABAC:** özne, nesne, eylem ve ortamın özelliklerine göre kural; en
  esnek, en karmaşık.
- Gerçek sistemler modelleri birlikte kullanır.
