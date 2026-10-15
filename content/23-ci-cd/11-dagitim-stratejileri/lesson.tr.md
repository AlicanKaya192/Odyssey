# Dağıtım Stratejileri

Onuncu bölümde bir paketi yayınladık: kullanıcı onu kendisi indirip
kuruyor. Bir web uygulamasında ya da bir model servisinde durum farklı:
kodu **biz** bir sunucuda çalıştırıyoruz ve kullanıcılar ona o anda
bağlı. Yeni sürümü oraya koymaya **dağıtım** (deployment) denir. Bu
bölümde dağıtımı hatta nasıl bağlayacağımızı, yeni sürüme geçerken
kullanıcıları nasıl korumayı seçebileceğimizi ve bir şey ters gidince
nasıl geri döneceğimizi görüyoruz.

## Ortamlar: önce provada, sonra sahnede

Kod doğrudan gerçek kullanıcılara gitmez. Arada en az bir **ortam**
(environment) olur:

<figure class="fig flow">
  <span class="node">Test</span>
  <span class="arrow">→</span>
  <span class="node">staging</span>
  <span class="arrow">→</span>
  <span class="node acc">production</span>
</figure>

- **staging** (hazırlık): gerçeğe olabildiğince benzeyen ama kullanıcısı
  olmayan ortam. Yeni sürüm önce buraya gider, burada denenir.
- **production** (canlı): gerçek kullanıcıların kullandığı ortam.

GitHub'da her ortam deponun **Settings › Environments** sayfasında
tanımlanır ve kendi kurallarını taşır:

- **Onaylayıcılar** (required reviewers): iş, listedeki biri "onayla"
  diyene kadar bekler. Canlıya geçişi bir insan başlatır.
- **Ortama özel gizli değerler**: canlının veritabanı şifresi yalnızca
  `production` ortamına bağlı işlerde görünür.
- **Hangi dallar**: örneğin canlıya yalnızca `main`'den ya da `v*`
  etiketlerinden dağıtılabilir.

İş akışında bir iş ortama `environment:` ile bağlanır:

```yaml
  deploy-staging:
    needs: build
    if: github.ref == 'refs/heads/main'
    runs-on: ubuntu-latest
    environment: staging
    steps:
      - uses: actions/download-artifact@v4
        with:
          name: dist
          path: dist
      - run: python scripts/deploy.py staging
```

## Yeni sürüme geçmenin dört yolu

Sunucuda eski sürüm çalışıyor, kullanıcılar bağlı. Yeni sürüme nasıl
geçilir?

| Strateji | Nasıl | Kesinti | Geri dönmek |
|---|---|---|---|
| Yeniden kur (recreate) | Eskiyi durdur, yeniyi başlat | Var | Eskiyi yeniden kur |
| Kademeli (rolling) | Sunucuları birkaç birkaç değiştir | Yok, ama kapasite düşer | Kademeli geri al |
| Mavi-yeşil (blue-green) | Yeniyi ayrı bir kopyada hazırla, trafiği bir anda çevir | Yok | Trafiği geri çevir (anında) |
| Kanarya (canary) | Trafiğin küçük bir kısmını yeniye ver, ölç, sonra artır | Yok | Kanaryayı kapat |

Kademeli dağıtımı küçük bir modelle görelim. Beş sunucu var, her adımda
ikisi yenileniyor; yenilenen sunucu o adım boyunca hizmet vermiyor:

```python
servers = ["web1", "web2", "web3", "web4", "web5"]
batch = 2
updated = []
for start in range(0, len(servers), batch):
    group = servers[start:start + batch]
    serving = len(servers) - len(group)
    print(f"updating {', '.join(group):<11} serving {serving}/5")
    updated += group
    old = len(servers) - len(updated)
    print(f"  after: new {len(updated)}, old {old}")
```

```text
updating web1, web2  serving 3/5
  after: new 2, old 3
updating web3, web4  serving 3/5
  after: new 4, old 1
updating web5        serving 4/5
  after: new 5, old 0
```

İki şey görünüyor: güncelleme boyunca kapasite 5 yerine 3'e düşüyor ve
bir süre **iki sürüm aynı anda** çalışıyor. Yani yeni sürüm, eskisiyle
yan yana çalışabilmeli; veritabanını eski sürümün anlamayacağı biçimde
değiştirmemeli.

## Kanarya: önce küçük bir grup

Madenciler ocağa kanarya götürürdü: zehirli gaz varsa önce kuş
etkilenirdi. Kanarya dağıtımında da yeni sürüm önce trafiğin küçük bir
kısmını (örneğin %5) alır; hata oranı eski sürümünkinden belirgin
yüksekse geri çekilir, değilse pay artırılır.

Karar sayılara dayanır, ama az istekle verilen karar yanıltır. Aşağıdaki
iki durumda yeni sürümün hata oranı aynı (%2), ama birinde yalnızca 50
istek görülmüş:

```python
def error_rate(errors, requests):
    return errors / requests


def decide(old, new, max_increase=0.01, min_requests=500):
    if new[1] < min_requests:
        return "wait"
    if error_rate(*new) > error_rate(*old) + max_increase:
        return "rollback"
    return "promote"


old = (40, 10000)
print(decide(old, (1, 50)))
print(decide(old, (20, 1000)))
print(decide(old, (5, 1000)))
```

```text
wait
rollback
promote
```

- Eski sürüm %0,4 hata veriyor. 50 istekte 1 hata da %2 eder, ama bu kadar
  az istekle karar verilmez: `wait`.
- 1000 istekte 20 hata (%2), eskisinden 1 puandan fazla yüksek:
  `rollback`.
- 1000 istekte 5 hata (%0,5), sınırın içinde: `promote`, pay artırılır.

## Dağıtımdan sonra: sağlık denetimi

Dağıtım komutunun başarıyla bitmesi uygulamanın çalıştığı anlamına
gelmez. Dağıtımdan sonra uygulamanın bir **sağlık adresine** (`/health`)
istek atılır. Yeni başlayan uygulama birkaç saniye hazır olmayabilir;
denetim birkaç kez, aralarında bekleyerek denenir. Hiç başarılı olmazsa
iş düşer ve hat **geri alma** adımına geçer:

```yaml
      - run: python scripts/deploy.py staging
      - run: python scripts/check_health.py "$APP_URL"
        env:
          APP_URL: ${{ vars.STAGING_URL }}
      - run: python scripts/deploy.py staging --rollback
        if: failure()
```

Beşinci bölümdeki `failure()` burada adım düzeyinde: önceki bir adım
düştüyse çalışır. Uygulamanın adresi gizli olmadığı için `vars` ile
okunuyor (dokuzuncu bölüm).

## Geri almak

Geri almanın en güvenli yolu, **önceki sürümün aynı paketini** yeniden
dağıtmaktır; kodu geri alıp yeniden derlemek değil. Bu yüzden sekizinci
bölümdeki "bir kez derle" kuralı burada da işe yarar: her sürümün paketi
sürüm numarasıyla saklanır ve geri almak, eski numarayı yeniden dağıtmak
olur.

Dikkat isteyen tek yer veritabanı. Yeni sürüm bir sütunu silen bir
değişiklik (migration) yaptıysa eski sürüme dönmek onu geri getirmez.
Yaygın yol iki adımdır: önce **ekle** (yeni sütun gelir, eski kod onu
görmezden gelir), her şey yerleşince sonraki bir sürümde **eskiyi kaldır**
(expand / contract). Böylece her an bir önceki sürüme dönülebilir.

## Canlıya geçiş

```yaml
name: Deploy

on:
  push:
    branches: [main]
    tags: ["v*"]

permissions:
  contents: read

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.13"
      - run: python -m pip install build
      - run: python -m build
      - uses: actions/upload-artifact@v4
        with:
          name: dist
          path: dist/
  deploy-staging:
    needs: build
    runs-on: ubuntu-latest
    environment: staging
    steps:
      - uses: actions/checkout@v4
      - uses: actions/download-artifact@v4
        with:
          name: dist
          path: dist
      - run: python scripts/deploy.py staging
  deploy-production:
    needs: deploy-staging
    if: startsWith(github.ref, 'refs/tags/v')
    runs-on: ubuntu-latest
    environment:
      name: production
      url: https://app.example.com
    concurrency:
      group: deploy-production
      cancel-in-progress: false
    steps:
      - uses: actions/checkout@v4
      - uses: actions/download-artifact@v4
        with:
          name: dist
          path: dist
      - run: python scripts/deploy.py production
```

- `main`'e her gönderim staging'e gider; canlıya yalnızca `v` etiketi ve
  staging başarılıysa.
- `production` ortamında onaylayıcı tanımlıysa iş, onay gelene kadar
  bekler.
- `environment` bir sözlük olabilir: `url` çalışma sayfasında canlı
  adresin bağlantısı olarak görünür.
- `concurrency` aynı anda iki canlı dağıtımı engeller. Yedinci bölümde
  `cancel-in-progress: true` testleri iptal ediyordu; dağıtımda **iptal
  edilmez** (`false`): yarıda kesilen dağıtım sunucuyu iki sürümün
  arasında bırakır. Yeni gelen, öncekinin bitmesini bekler.
- Dağıtım işleri `scripts/deploy.py`'yi kullandığı için kodu çekiyor;
  dağıttıkları paket ise yine `build`'in ürettiği aynı dosya.

## Sırada

Burada dağıtılan bir Python paketiydi. On ikinci bölümde paketi bir
**konteyner imajına** koyup hatta derliyor, sınıyor ve bir imaj deposuna
gönderiyoruz.

## Özet

- Kod önce staging'e, sonra production'a gider. GitHub ortamları
  onaylayıcı, ortama özel gizli değer ve dal kuralı taşır; iş
  `environment:` ile bağlanır.
- Yeniden kur kesinti yaratır; kademeli dağıtımda kapasite düşer ve iki
  sürüm yan yana çalışır; mavi-yeşil trafiği bir anda çevirir; kanarya
  önce küçük bir payla ölçer.
- Kanarya kararı yeterli istekle verilir; az istekle beklenir.
- Dağıtımdan sonra sağlık denetimi; düşerse `if: failure()` ile geri
  alma.
- Geri almak, önceki sürümün aynı paketini yeniden dağıtmaktır.
  Veritabanı değişiklikleri önce ekle, sonra kaldır.
- Canlı dağıtımında `concurrency` ve `cancel-in-progress: false`.
