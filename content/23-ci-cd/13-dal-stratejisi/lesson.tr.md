# Dal Stratejisi ve PR Kontrolleri

Şimdiye kadar hattı tek kişi kullanıyor gibi düşündük. Bir ekipte aynı
depoya her gün birçok kişi kod gönderir. `main` dalının **her an
çalışır** durumda kalması, kimsenin testleri geçmeyen kodu oraya
koyamaması gerekir. Bu bölümde dalları nasıl düzenleyeceğimizi, `main`'i
GitHub'ın kurallarıyla nasıl koruyacağımızı ve PR'da çalışan kontrollerin
hangi tuzaklara düştüğünü görüyoruz.

## Dal stratejileri

Dal stratejisi, "kim hangi dalda çalışır, kod `main`'e nasıl girer"
sorusunun ekipçe verilmiş cevabıdır. Yaygın üç tanesi:

| Strateji | Nasıl | Ne zaman uygun |
|---|---|---|
| Gövde tabanlı (trunk-based) | Çok kısa ömürlü dallar (bir-iki gün), sık sık `main`'e birleştirme | Güçlü testleri olan, sık dağıtan ekipler |
| GitHub flow | Her iş için bir dal, PR, inceleme, `main`'e birleştirme; `main` her an dağıtılabilir | Çoğu proje; bu patikanın varsaydığı düzen |
| GitFlow | `main` + `develop` + özellik, sürüm ve acil düzeltme dalları | Seyrek, planlı sürüm çıkaran projeler |

Ortak fikir: dal ne kadar uzun yaşarsa `main`'den o kadar uzaklaşır ve
birleştirmek o kadar zorlaşır. CI'ın "sık birleştir" sözü (sıfırıncı
bölüm) dalları kısa tutmaktan geçer.

## `main`'i korumak

GitHub'da deponun **Settings › Rules** (kural kümeleri, rulesets) ya da
eski adıyla **Branches › Branch protection** sayfasında `main` için
kurallar yazılır:

- **PR zorunlu**: `main`'e doğrudan gönderim yok; her değişiklik bir
  PR'dan geçer.
- **Onay zorunlu**: en az bir kişi PR'ı onaylamadan birleştirilemez.
- **Zorunlu kontroller** (required status checks): listedeki kontroller
  geçmeden birleştirme düğmesi kapalı kalır.
- **Dal güncel olmalı**: PR, `main`'in son hâliyle yeniden sınanmadan
  birleştirilemez.
- **Zorla gönderim ve silme yasak**: `main`'in geçmişi yeniden yazılamaz.

Hattın işi bu kuralların üçüncüsünde başlar: hat, PR'ı geçirecek ya da
durduracak kontrolleri üretir.

## Zorunlu kontrolün adı işin adıdır

Zorunlu kontrol listesine iş akışının adı değil, **işin adı** yazılır:
`lint`, `test`. Matrisli bir işte her kopya ayrı kontroldür ve GitHub
onları `test (3.12)`, `test (3.13)` gibi adlarla gösterir. Birleştirme
kararını küçük bir modelle görelim:

```python
def matrix_names(job, versions):
    return [f"{job} ({version})" for version in versions]


def merge_state(required, reported):
    for name in required:
        if reported.get(name) == "failure":
            return f"blocked: {name} failed"
    for name in required:
        if reported.get(name) != "success":
            return f"waiting: {name}"
    return "ready"


required = ["lint"] + matrix_names("test", ["3.12", "3.13"])
print(required)
runs = {"lint": "success", "test (3.12)": "success",
        "test (3.13)": "success"}
print(merge_state(required, runs))
runs["test (3.13)"] = "failure"
print(merge_state(required, runs))
renamed = {"lint": "success", "tests (3.12)": "success",
           "tests (3.13)": "success"}
print(merge_state(required, renamed))
```

```text
['lint', 'test (3.12)', 'test (3.13)']
ready
blocked: test (3.13) failed
waiting: test (3.12)
```

Son satır en sık yaşanan tuzak: biri iş akışında `test` işinin adını
`tests` yaptı. Bütün kontroller geçiyor, ama zorunlu listede hâlâ `test
(3.12)` yazıyor ve o adla gelen bir sonuç yok. PR **sonsuza kadar
bekler**; GitHub onu "Expected — Waiting for status to be reported"
diye gösterir. İşin adı değişince kural da güncellenir.

## Hiç çalışmayan iş akışı: kapı işi

Aynı tuzağın ikinci yolu dördüncü bölümdeki yol süzgeci. Yalnızca
`README.md`'yi değiştiren bir PR'da `paths: ["src/**"]` süzgeçli iş
akışı **hiç başlamaz**. Başlamayan iş akışı sonuç da bildirmez; zorunlu
kontrol yine bekler. `[skip ci]` yazılmış bir commit de aynı yere düşer.

Fark şurada: iş akışı başlayıp bir iş `if:` ile **atlanırsa** (skipped)
GitHub o işi zorunlu kontrol için başarılı sayar. Yaygın çözüm, bütün
işlere bağlı tek bir **kapı işi** (gate) yazıp zorunlu listeye yalnızca
onu koymaktır:

```yaml
  ci-ok:
    if: always()
    needs: [lint, test]
    runs-on: ubuntu-latest
    steps:
      - run: exit 1
        if: >-
          contains(needs.*.result, 'failure')
          || contains(needs.*.result, 'cancelled')
      - run: echo "lint and test passed or were skipped"
```

- `if: always()`: önceki işler düşse de kapı çalışır; yoksa kendisi de
  atlanır ve atlanan iş başarılı sayıldığı için PR geçerdi.
- `needs.*.result` bağlı işlerin sonuçlarının listesi. İçinde `failure`
  ya da `cancelled` varsa `exit 1` kapıyı düşürür.
- `>-` uzun ifadeyi alt satırlara böler; YAML onu tek satır olarak okur.
- Zorunlu listede tek ad kalır: `ci-ok`. Matrise yeni bir Python sürümü
  eklemek ya da bir işin adını değiştirmek artık kuralı bozmaz.

## Birleştirme kuyruğu

"Dal güncel olmalı" kuralı yoğun bir depoda yorucudur: her birleştirmeden
sonra açık PR'ların hepsi yeniden `main`'le güncellenip sınanır. GitHub'ın
**birleştirme kuyruğu** (merge queue) bunu sıraya koyar: onaylanan PR
kuyruğa girer, GitHub onu önündekilerle birlikte geçici bir dalda sınar,
geçerse birleştirir.

Kuyruktaki sınama ayrı bir olayla başlar: `merge_group`. İş akışı bu
olayı dinlemiyorsa kuyrukta zorunlu kontroller hiç çalışmaz ve PR
kuyrukta takılır:

```yaml
on:
  push:
    branches: [main]
  pull_request:
    branches: [main]
  merge_group:
```

## PR başlığını denetlemek

Birçok ekip PR'ları "squash" ile birleştirir: PR'ın bütün commit'leri tek
commit olur ve o commit'in mesajı **PR'ın başlığı** olur. Onuncu bölümdeki
sürüm artırma commit öneklerine (`feat:`, `fix:`) bakıyordu; o zaman PR
başlığı da bu kurala uymalı. Kuralı bir düzenli ifadeyle (regular
expression) yazalım:

```python
import re

TITLE = re.compile(r"^(feat|fix|docs|test|chore)(\([a-z-]+\))?!?: \S.*$")

for title in ["feat(login): add remember me", "Fix login bug",
              "fix: ", "feat!: drop Python 3.11"]:
    print(f"{title!r:32} {bool(TITLE.match(title))}")
```

```text
'feat(login): add remember me'   True
'Fix login bug'                  False
'fix: '                          False
'feat!: drop Python 3.11'        True
```

- `(\([a-z-]+\))?` isteğe bağlı kapsam: `(login)`.
- `!?` uyumsuz değişiklik işareti.
- `: \S.*` iki noktadan sonra boşluk ve boş olmayan bir özet. `"fix: "`
  bu yüzden geçmiyor.

Hatta denetim PR başlığını bir betiğe verir. Dokuzuncu bölümdeki kural
burada da geçerli: başlık dışarıdan gelen bir metin, `run:` satırına
doğrudan yazılmaz, `env:`'e konur.

```yaml
on:
  pull_request:
    types: [opened, edited, synchronize, reopened]
```

```yaml
  title:
    if: github.event_name == 'pull_request'
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: python scripts/check_title.py "$TITLE"
        env:
          TITLE: ${{ github.event.pull_request.title }}
```

`types` listesindeki `edited` önemli: `pull_request` varsayılan olarak
yalnızca açılınca, yeni commit gelince ve yeniden açılınca çalışır.
Başlığı düzelten kişi `edited` olmadan denetimi yeniden çalıştıramaz.

## `pull_request_target` uyarısı

Bir de `pull_request_target` olayı var: PR'ın kodunda değil **hedef dalın**
kodunda, gizli değerlerle ve yazma izniyle çalışır (fork'tan gelen PR'a
yorum yazmak gibi işler için). Bu olayda PR'ın kodu çekilip
çalıştırılırsa, fork'u açan herkes hattınızın gizli değerleriyle
istediğini çalıştırır. Kural: `pull_request_target` içinde PR'ın kodu
çalıştırılmaz. Test için her zaman `pull_request`.

## Sırada

On dördüncü bölümde bazen geçip bazen düşen **kararsız testlerle**
(flaky tests) ve düşen bir hattın nedenini bulmakla uğraşıyoruz.

## Özet

- Dal stratejisi ekibin anlaşmasıdır; dallar kısa yaşadıkça birleştirme
  kolaylaşır. GitHub flow: dal, PR, inceleme, `main`.
- `main` kurallarla korunur: PR, onay, zorunlu kontroller, güncel dal,
  zorla gönderim yasağı.
- Zorunlu kontrolün adı işin adıdır; matriste `test (3.12)`. Ad değişirse
  ya da iş akışı hiç başlamazsa PR beklemede kalır.
- Atlanan iş başarılı sayılır; `if: always()` + `needs.*.result` ile
  kurulan tek bir kapı işi zorunlu listeyi sadeleştirir.
- Birleştirme kuyruğu kullanılıyorsa iş akışı `merge_group`'u da dinler.
- PR başlığı denetimi `env:` ile; başlık düzeltilince yeniden çalışsın
  diye `types`'a `edited`.
- `pull_request_target` içinde PR'ın kodu çalıştırılmaz.
