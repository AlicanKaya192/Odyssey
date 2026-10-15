# Genel Tekrar

CI/CD ve DevOps modülünün sonuna geldin. "Bende çalışıyordu" sorunuyla
başladık; testleri ve kalite kapılarını hattın içine koyduk, iş akışı
dosyasını parça parça okuduk. Sonra hattı yönettik: ne zaman çalışacağı,
hangi işin hangisini bekleyeceği, matris ve önbellek. Ardından ürüne
geçtik: paket, gizli değerler, sürüm ve dağıtım. En sonda ekiple çalışmayı,
kararsız testleri ve bir projenin bütün hattını gördük. Bu bölüm yolu bir
kez daha yürüyor.

<figure class="fig">
  <div class="flow">
    <span class="node">Test ve kapı</span>
    <span class="arrow">→</span>
    <span class="node">Hattı yönet</span>
    <span class="arrow">→</span>
    <span class="node">Ürün ve güvenlik</span>
    <span class="arrow">→</span>
    <span class="node">Canlı ve ekip</span>
    <span class="arrow">→</span>
    <span class="node acc">Tam hat</span>
  </div>
  <figcaption>Modülün yolu: sına, düzenle, paketle ve koru, yayına çıkar, birleştir.</figcaption>
</figure>

## 1. Temeller (Bölüm 0–3)

- **CI:** sık birleştir, her birleştirmede kod temiz bir makinede kurulup
  sınansın. **Sürekli teslim:** her geçen değişiklik yayına hazır; yayını
  insan başlatır. **Sürekli dağıtım:** yayın da kendiliğinden (0).
- **pytest** `test_` dosya ve fonksiyonlarını bulur; hat kararını çıkış
  kodundan verir: `0` geçti, `1` düştü, `5` test yok (1).
- **Kapı** = ölçüm + eşik. Ucuz kapılar önde: sözdizimi, biçim, lint,
  sonra testler; kapsam test edilmemiş satırı gösterir ama doğruluk
  kanıtı değildir (2).
- **İş akışı dosyası** bir sözlük ve liste ağacı: `on`, `jobs` →
  `runs-on`, `steps`; adım ya `uses` ya `run`. Sürümler tırnakla (`"3.10"`)
  (3).

## 2. Hattı yönetmek (Bölüm 4–7)

- **Tetikleyiciler:** `pull_request` birleşmiş hâli sınar; `branches`
  hedef dal. `*` eğik çizgiye uymaz, `**` uyar. cron UTC (4).
- **İşler** aynı anda, ayrı makinelerde; `needs` sıra koyar. Süreyi
  **kritik yol** belirler. `failure()`, `always()`; değer aktarmak için
  `outputs` (5).
- **Matris:** iş sayısı boyutların çarpımı; `exclude` önce, `include`
  sonra; hatanın yerini görmek için `fail-fast: false` (6).
- **Hız:** önbellek anahtarı içerikten (`hashFiles`), `cache: pip`;
  `concurrency` eski çalışmayı iptal eder; `timeout-minutes` (7).

## 3. Ürün ve güvenlik (Bölüm 8–10)

- **Artifact** ürün içindir, önbellek hız için. **Bir kez derle:** test
  edilen ve yayınlanan aynı dosya (8).
- **Gizli değer** kasada durur, `env:` ile yalnızca isteyen adıma gider;
  fork PR'ında boştur. `permissions:` en az yetki. Dışarıdan gelen metin
  `run:`'a doğrudan yazılmaz (9).
- **Sürüm:** `ANA.YAN.YAMA`, sayı olarak karşılaştırılır; commit önekleri
  artışı söyler; etiket `pyproject.toml` ile tutmalı, yayınlanan etiket
  taşınmaz (10).

## 4. Canlıya çıkmak ve ekip (Bölüm 11–14)

- **Dağıtım:** önce staging, sonra production; ortamlar onay ve ortama
  özel gizli değer taşır. Kademeli, mavi-yeşil, kanarya; sağlık denetimi
  ve `if: failure()` ile geri alma; dağıtımda `cancel-in-progress: false`
  (11).
- **Konteyner:** imajı derle, içinde sına, aynı imajı gönder; dağıtımda
  değişmeyen etiket (SHA), `ghcr.io` için `packages: write`, katman
  önbelleği `type=gha` (12).
- **Ekip:** `main` kurallarla korunur; zorunlu kontrolün adı işin adı; ad
  değişirse ya da iş akışı hiç başlamazsa PR bekler; tek kapı işi `ci-ok`;
  kuyruk için `merge_group` (13).
- **Kararsız test** güveni yok eder: yirmi tanesi hattı üç çalışmanın
  birinde nedensiz kırmızı yapar. Sıra, zaman, küme sırası; yeniden
  çalıştırmak değil düzeltmek ya da sahipli karantina (14).

## 5. Tam hat (Bölüm 15)

- Önce sözleşme, sonra YAML: tetikleyiciler, lint → matrisli testler →
  paket → `ci-ok` → etikette yayın; üstte okuma izni, yazma yalnızca
  yayında; kritik yol 7 dakika (15).

## Hepsi birlikte: bir hattı incelemek

Modülün kurallarını kullanarak bir iş akışı dosyasını okuyup sorunlarını
listeleyen küçük bir inceleyici yazalım. Aşağıdaki dosyada bu modülde
gördüğümüz dört hata var:

```python
import re

import yaml

TEXT = """
name: CI
on: [push, pull_request]
permissions: write-all
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout
      - run: echo "${{ github.event.pull_request.title }}"
      - run: python -m pytest
"""


def review(text):
    data = yaml.safe_load(text)
    problems = []
    if data.get("permissions") in (None, "write-all"):
        problems.append("permissions: read by default")
    for name, job in data["jobs"].items():
        if "timeout-minutes" not in job:
            problems.append(f"{name}: no timeout-minutes")
        for step in job["steps"]:
            uses = step.get("uses", "")
            if uses and "@" not in uses:
                problems.append(f"{name}: {uses} has no version")
            if re.search(r"\$\{\{\s*github\.event\.", step.get("run", "")):
                problems.append(f"{name}: outside text in run")
    return problems


for problem in review(TEXT):
    print(problem)
```

```text
permissions: read by default
test: no timeout-minutes
test: actions/checkout has no version
test: outside text in run
```

Her satır bir bölüme dayanıyor: izin (9), süre sınırı (7), sürümsüz eylem
(3 ve 9), kod enjeksiyonu (9). Gerçek projelerde bu işi yapan hazır
araçlar var; ama neye baktıklarını bilmek, uyarılarını anlamanın tek yolu.

## Sonra

Bu modülde iş akışlarını çalıştırmadan denetledik; testler ve betikler
gerçekten çalıştı. Kendi deponda ilk hattı kurduğunda değişen tek şey,
dosyanın GitHub'ın makinesinde gerçekten koşması olacak. Kurallar aynı:
**küçük başla, hızlı kapıyı öne koy, her parçanın neden orada olduğunu
söyleyebil.**

Bu patikanın ikinci modülü **MLOps ve ML Sistem Tasarımı**: aynı hat bir
modeli eğitmek, ölçmek ve sunmak için kullanılıyor.
