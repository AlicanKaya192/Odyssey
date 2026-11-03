# Yetki Yükseltme

Bir saldırgan bir sisteme çoğu zaman **az yetkiyle** girer: sıradan bir
kullanıcının hesabıyla, kısıtlı bir hizmetin içinden ya da bir web
uygulamasının sıradan bir oturumuyla. Asıl hedefi ise daha fazlasıdır:
başkalarının verisi ya da yönetici yetkisi. Az yetkiden çok yetkiye geçmeye
**yetki yükseltme** (privilege escalation) denir.

Bu bölüm yetki yükseltmeyi **savunan gözüyle** anlatıyor: hangi
yapılandırma hataları buna kapı açar, bu hatalar nasıl bulunur ve nasıl
kapatılır. Kodlar yine oyuncak: sahte tablolar ve sahte kayıt satırları
üzerinde çalışan denetleyiciler.

## İki yön: yatay ve dikey

<figure class="fig"><div class="versus">
  <div><h4>Yatay yükseltme</h4>Aynı düzeydeki <b>başka bir kullanıcının</b> yetkisine ya da verisine ulaşmak. Bir müşterinin başka bir müşterinin faturasını görmesi gibi.</div>
  <div><h4>Dikey yükseltme</h4>Daha <b>yüksek bir düzeye</b> çıkmak. Sıradan kullanıcının yönetici işlemleri yapabilmesi gibi.</div>
</div><figcaption>İkisinde de sebep aynı: bir yerde yetki denetimi eksik ya da yanlış.</figcaption></figure>

## Yatay yükseltme: sahiplik denetimi

Bir uygulama faturayı yalnızca numarasıyla getiriyorsa, giriş yapmış her
kullanıcı numarayı değiştirerek başkasının faturasını görebilir:

```python
INVOICES = {
    101: {"owner": "ada", "total": 120},
    102: {"owner": "bob", "total": 75},
}


def get_invoice_unsafe(user, invoice_id):
    return INVOICES[invoice_id]


def get_invoice(user, invoice_id):
    invoice = INVOICES.get(invoice_id)
    if invoice is None or invoice["owner"] != user:
        return "not found"
    return invoice


print(get_invoice_unsafe("ada", 102))
print(get_invoice("ada", 101))
print(get_invoice("ada", 102))
```

```text
{'owner': 'bob', 'total': 75}
{'owner': 'ada', 'total': 120}
not found
```

İlk fonksiyon `ada`'ya `bob`'un faturasını verdi. Düzeltilmiş hâli her
istekte **sahipliği** denetliyor. Başkasının faturası için "yasak" yerine
"bulunamadı" demesi de bilinçli: böylece hangi numaraların var olduğu da
sızmaz. Kimliği doğrulanmış olmak, her nesneye erişebilmek demek değildir;
Yetkilendirme bölümündeki kural burada da geçerli.

## Dikey yükseltme: istemciye güvenmek

Profil güncelleyen bir uç nokta gelen alanların hepsini kullanıcının
kaydına yazıyorsa, kullanıcı isteğe bir `role` alanı ekleyerek kendini
yönetici yapabilir. Buna **toplu atama** (mass assignment) denir:

```python
def update_unsafe(user, changes):
    user.update(changes)
    return user


ALLOWED = {"email", "display_name"}


def update_safe(user, changes):
    for key, value in changes.items():
        if key in ALLOWED:
            user[key] = value
    return user


request = {"display_name": "Ada", "role": "admin"}
print(update_unsafe({"name": "ada", "role": "user"}, request)["role"])
print(update_safe({"name": "ada", "role": "user"}, request)["role"])
```

```text
admin
user
```

Güvenli sürüm yalnızca **izin listesindeki** alanları yazıyor; `role`
sessizce atlandı. Kural: istemciden gelen veri hangi alanları
değiştirebileceğine kendisi karar veremez. Rol ve yetki gibi alanlar
yalnızca sunucudaki ayrı, denetimli bir işlemle değişir.

## İşletim sisteminde: yanlış yapılandırma

İşletim sistemlerinde yetki yükseltmenin en sık sebebi bir program hatası
değil, **yapılandırma hatasıdır**. Dosya İzinleri bölümünde gördüğümüz gibi,
yönetici adına çalışan bir zamanlanmış görevin betiği başkaları tarafından
değiştirilebiliyorsa, o betiğe eklenen her satır yönetici yetkisiyle
çalışır. Bunu bulan bir denetleyici, yönetici olarak çalışan her görevin
betiğine bakar:

```python
TASKS = [
    {"name": "backup", "runs_as": "root", "owner": "root", "mode": 0o755},
    {"name": "cleanup", "runs_as": "root", "owner": "root", "mode": 0o777},
    {"name": "report", "runs_as": "root", "owner": "bob", "mode": 0o755},
    {"name": "stats", "runs_as": "bob", "owner": "bob", "mode": 0o777},
]
for task in TASKS:
    others_write = task["mode"] & 0o022
    if task["runs_as"] == "root" and (task["owner"] != "root" or others_write):
        print("risky:", task["name"])
```

```text
risky: cleanup
risky: report
```

`cleanup` herkesçe yazılabildiği, `report` ise sıradan bir kullanıcıya ait
olduğu için işaretlendi: iki durumda da yönetici olmayan biri, yöneticinin
çalıştıracağı şeyi değiştirebilir. `stats` yetki yükseltme değil, çünkü
zaten `bob` olarak çalışıyor; ama `777` izni yine de Dosya İzinleri
bölümündeki ayrı bir hatadır.

## setuid envanteri

Dosya İzinleri bölümünde gördüğümüz **setuid** biti, programı çalıştıranın
değil dosya sahibinin yetkisiyle çalıştırır. Sahibi yönetici olan her
setuid program, hatası varsa bir yükseltme kapısıdır. Savunma basittir:
setuid olması **gereken** programların bir izin listesini tut, listede
olmayan her setuid dosyayı raporla.

```python
import stat

FILES = [
    {"path": "/usr/bin/passwd", "mode": 0o4755},
    {"path": "/opt/tools/report-tool", "mode": 0o4755},
    {"path": "/usr/bin/ls", "mode": 0o755},
]
ALLOWED = {"/usr/bin/passwd"}
for f in FILES:
    if f["mode"] & stat.S_ISUID and f["path"] not in ALLOWED:
        print("unexpected setuid:", f["path"])
print(stat.filemode(stat.S_IFREG | 0o4755))
```

```text
unexpected setuid: /opt/tools/report-tool
-rwsr-xr-x
```

setuid bit izin dizesinde sahibin `x` harfinin yerinde `s` olarak görünür.
Parola değiştirme programı listede olduğu için sessiz kaldı; listede
olmayan araç raporlandı. Yeni bir setuid dosyanın **beklenmedik** biçimde
ortaya çıkması da kendi başına bir uyarı işaretidir.

## Tespit: kayıtlarda iz

Önlemek her zaman yetmez; yükseltme **denemeleri** de izlenir. Yetki
isteyen her işlem (Linux'ta `sudo`, Windows'ta yönetici onayı) bir kayıt
bırakır. Aynı kullanıcının kısa sürede art arda reddedilmesi dikkat
edilecek bir işarettir:

```python
from collections import Counter

LOG = [
    "09:58 sudo user=ada result=ok cmd=update",
    "10:01 sudo user=bob result=denied cmd=passwd",
    "10:02 sudo user=bob result=denied cmd=restart",
    "10:02 sudo user=bob result=denied cmd=useradd",
    "10:05 sudo user=eve result=denied cmd=update",
]
denied = Counter()
for line in LOG:
    fields = dict(part.split("=") for part in line.split()[2:])
    if fields["result"] == "denied":
        denied[fields["user"]] += 1
print(dict(denied))
print([user for user, count in denied.items() if count >= 3])
```

```text
{'bob': 3, 'eve': 1}
['bob']
```

`bob` 3 kez reddedildi ve eşiği geçti; `eve`'nin tek
reddi büyük olasılıkla bir yanlışlıktır. Eşik ne kadar düşükse o kadar çok
yanlış alarm, ne kadar yüksekse o kadar çok kaçırılan deneme olur; bu
denge Kayıt ve İzleme ile Saldırı Tespiti bölümlerinin konusudur. Yönetici
grubuna yeni bir üye eklenmesi gibi değişiklikler de aynı şekilde izlenir.

## Önlem listesi

| Sebep | Önlem |
|---|---|
| Nesneye sahiplik denetimi yok | Her istekte sahipliği sunucuda denetle |
| İstemciden gelen alan doğrudan yazılıyor | Değişebilecek alanların izin listesi |
| Yönetici görevi başkasının yazabildiği betiği çalıştırıyor | Betik yönetici hesabına ait, `755` ya da daha dar |
| Gereksiz setuid programlar | İzin listesi; listede olmayanın bitini kaldır |
| Yamalanmamış çekirdek ve hizmetler | Yama yönetimi |
| Herkesin yönetici olduğu sistem | En az yetki; günlük iş standart hesapla |

## Özet

- **Yetki yükseltme**, az yetkiden çok yetkiye geçmektir; **yatay**
  (başka kullanıcı) ya da **dikey** (daha yüksek düzey) olur.
- Yatay yükseltmeye karşı her istekte **sahiplik denetimi**.
- Dikey yükseltmeye karşı istemciden gelen alanlar için **izin listesi**.
- İşletim sisteminde sebep çoğu zaman **yapılandırma**: başkasının
  yazabildiği ayrıcalıklı betikler, gereksiz setuid programlar.
- **Tespit:** art arda reddedilen yetki istekleri ve yönetici grubundaki
  değişiklikler izlenir.
