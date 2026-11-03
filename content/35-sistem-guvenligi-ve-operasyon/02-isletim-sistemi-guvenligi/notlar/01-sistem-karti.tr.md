## Temel kavramlar

| Kavram | Anlamı |
|---|---|
| Çekirdek kipi | Her şeye erişen kip; işletim sisteminin çekirdeği burada |
| Kullanıcı kipi | Kısıtlı kip; uygulamalar burada |
| Sistem çağrısı | Uygulamanın çekirdekten ayrıcalıklı bir iş istemesi |
| Süreç | Çalışan program; kendi bellek alanı vardır |
| Süreç yalıtımı | Bir süreç ötekinin belleğini okuyamaz |
| Kum havuzu (sandbox) | Bir programı daha da kısıtlı bir alanda çalıştırmak |
| Sıkılaştırma | Varsayılan kurulumu daha güvenli hâle getirmek |
| Güvenlik taban çizgisi | Her sistemin uyması gereken yapılandırma listesi |

## Ayrıcalıklı hesaplar

| Sistem | Yönetici hesabı | Yetkiyi geçici istemek |
|---|---|---|
| Linux | `root` | `sudo komut` |
| Windows | Administrator | Kullanıcı Hesabı Denetimi onayı |

Günlük iş standart hesapla yapılır; yönetici yetkisi iş bitince bırakılır.

## Python kalıpları

- Politikada yoksa reddet: `operation in POLICY.get(role, set())`.
- Sürümü sayı demetine çevir: `tuple(int(p) for p in text.split("."))`.
- Demetler sayı sayı karşılaştırılır: `(2, 4, 10) > (2, 4, 9)`.
- Kural listesiyle denetim: `if config.get(key) != wanted: ...`.

## Akılda tutulacak

- `"2.4.10" < "2.4.9"` metin olarak **True** çıkar; sürüm metin olarak
  karşılaştırılmaz.
- Olmayan anahtar da kural ihlalidir: `config.get(key)` `None` döner ve
  istenen değere eşit olmaz.
- Kullanılmayan her hizmet ve hesap, kimsenin izlemediği bir kapıdır.
