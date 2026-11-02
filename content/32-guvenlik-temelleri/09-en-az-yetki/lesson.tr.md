# En Az Yetki ve Görev Ayrılığı

Güvenlik İlkeleri bölümünde iki ilkeyi kısaca gördük: **en az yetki**
(least privilege) ve **görev ayrılığı** (separation of duties). İkisi de
basit cümlelerdir ama gerçek bir kurumda uygulamak sürekli emek ister.
Çünkü yetkiler zamanla kendiliğinden **büyür**: kimse bir yetkiyi geri
almayı hatırlamaz. Bu bölüm bu büyümeyi ölçmeyi ve durdurmayı anlatıyor.

## En az yetki nerelerde uygulanır?

- **Kişi hesapları:** herkes işine yetecek kadar. Muhasebe stajyeri bütün
  bordroları görmez.
- **Yönetici hesapları:** yönetici yetkisi olan biri, günlük işlerini
  (e-posta, web) **ayrı ve sıradan** bir hesapla yapar. Yönetici hesabı
  yalnızca gerektiğinde kullanılır; oltalama e-postasını açan hesap
  yönetici değilse zarar küçük kalır.
- **Programlar ve hizmetler:** bir web uygulaması veritabanına, yalnızca
  ihtiyaç duyduğu tablolarda okuma ve yazma izni olan bir kullanıcıyla
  bağlanır; tablo silme izni olan yönetici kullanıcıyla değil.
- **Veri:** **bilmesi gereken kadar** (need to know). Yetki düzeyi yeterli
  olsa bile iş gerektirmiyorsa bilgi verilmez.

## Yetki birikmesi

Bir çalışan önce destek ekibinde, sonra satışta, sonra finansta çalışıyor.
Her ekip değişikliğinde yeni rolün yetkileri veriliyor ama eskiler
alınmıyor. Buna **yetki birikmesi** (privilege creep) denir:

```python
role_perms = {
    "support": {"tickets:read", "tickets:reply"},
    "sales": {"crm:read", "crm:write"},
    "finance": {"invoices:read", "payments:approve"},
}
history = ["support", "sales", "finance"]
held = set()
for role in history:
    held |= role_perms[role]
needed = role_perms[history[-1]]
print("held:", len(held), "needed:", len(needed))
print("extra:", sorted(held - needed))
```

```text
held: 6 needed: 2
extra: ['crm:read', 'crm:write', 'tickets:read', 'tickets:reply']
```

Bu kişinin elindeki altı yetkiden dördü bugünkü işi için gereksiz. Hesabı
ele geçirilirse saldırgan hem müşteri kayıtlarına hem destek taleplerine
hem ödemelere ulaşır. Birikme sessizdir: hiçbir şey bozulmaz, kimse
şikâyet etmez, risk yalnızca büyür.

## Gözden geçirme ve kullanılmayan yetkiler

Birikmeye karşı en etkili önlem düzenli **erişim gözden geçirmesidir**
(access review): her yetkinin sahibine ya da yöneticisine "bu hâlâ gerekli
mi?" diye sorulur. Cevabı kolaylaştıran bir veri var: kayıtlar. Bir yetki
aylardır hiç kullanılmamışsa büyük ihtimalle gereksizdir.

```python
granted = {"crm:read", "crm:write", "invoices:read", "payments:approve"}
used_last_90_days = {"invoices:read", "payments:approve", "crm:read"}
print(sorted(granted - used_last_90_days))
```

```text
['crm:write']
```

Küme farkı (`-`) verilen ama kullanılmayanları bulur. Bu liste bir
öneridir, otomatik silme listesi değil: yılda bir kez kullanılan bir
yetki (yıl sonu kapanışı) 90 günlük kayıtta görünmeyebilir.

## Süreli yetki

Bazı yetkiler yalnızca kısa bir süre için gerekir: bir sorunu çözmek için
canlı veritabanına bakmak, bir taşıma işi için yedeklere erişmek. Bunları
kalıcı vermek yerine **bitiş tarihiyle** vermek birikmeyi baştan önler.
Bu fikrin uç hâline **tam zamanında erişim** (just-in-time access) denir:
yetki istenir, onaylanır, birkaç saat sonra kendiliğinden düşer.

```python
from datetime import date

grants = [("ada", "prod-db", "2026-10-01"), ("alan", "prod-db", "2026-11-30"),
          ("grace", "backups", "2026-11-02")]
today = date(2026, 11, 2)
for user, resource, until in grants:
    status = "active" if date.fromisoformat(until) >= today else "expired"
    print(user, resource, status)
```

```text
ada prod-db expired
alan prod-db active
grace backups active
```

Süresi dolan yetkinin gerçekten **kaldırılması** gerekir; "süresi doldu"
yazan ama hâlâ çalışan bir yetki işe yaramaz. Bitiş günü dahil sayıldı
(`>=`): Grace'in yetkisi bugün son gününde.

## Görev ayrılığı

**Görev ayrılığı**, bir işin kötüye kullanılabilecek adımlarını farklı
kişilere vermektir. Tek bir kişi hem yeni bir tedarikçi kaydedip hem ona
ödeme onaylayabilirse, kendi kurduğu sahte şirkete para gönderebilir. İki
adım iki ayrı kişide olursa dolandırıcılık için iki kişinin anlaşması
gerekir.

Kurumlar **çakışan görev** (conflicting duties) çiftlerini önceden yazar
ve kimsenin bir çiftin iki yarısına birden sahip olmadığını denetler:

```python
conflicts = [("vendor:create", "payment:approve"), ("code:write", "deploy:alone")]
user_perms = {
    "ada": {"vendor:create", "payment:approve", "crm:read"},
    "alan": {"vendor:create"},
    "grace": {"code:write", "deploy:alone"},
}
for user, perms in user_perms.items():
    found = [pair for pair in conflicts if set(pair) <= perms]
    print(user, found)
```

```text
ada [('vendor:create', 'payment:approve')]
alan []
grace [('code:write', 'deploy:alone')]
```

`set(pair) <= perms` "çiftin iki yarısı da kişinin yetkilerinde mi?"
demek (`<=` kümelerde "alt kümesi mi" sorusudur). Ada ve Grace birer
çakışma taşıyor.

Görev ayrılığının akrabaları:

- **Dört göz ilkesi** (two-person rule): önemli bir işlem için iki kişinin
  onayı. Büyük ödemeler, canlı sisteme kod gönderme, şifreleme anahtarına
  erişim.
- **Zorunlu izin ve görev değişimi** (mandatory vacation, job rotation):
  bir kişinin işini bir süre başkası yapar; gizli bir düzen varsa ortaya
  çıkar.

## Acil durum hesabı

Her şey kilitliyken bir gün acil bir durum olur ve normal onay yolu
beklenemez. Bunun için **acil durum hesabı** (break-glass account)
tutulur: parolası kasada durur, kullanıldığı an alarm çalar ve sonradan
her işlemi incelenir. En az yetki ilkesinin istisnası da bu yüzden açık,
kayıtlı ve izlenir.

## Özet

- En az yetki kişilere, yöneticilere, programlara ve veriye uygulanır;
  günlük iş yönetici olmayan hesapla yapılır.
- Yetkiler kendiliğinden **birikir**; düzenli **gözden geçirme** ve
  kullanılmayan yetkilerin kaldırılması bunu durdurur.
- Kısa süreli ihtiyaç için yetki **bitiş tarihiyle** verilir.
- **Görev ayrılığı** kötüye kullanılabilecek adımları farklı kişilere
  verir; çakışan görev çiftleri önceden yazılıp denetlenir.
- İstisnalar (acil durum hesabı) açık, kayıtlı ve izlenir.
