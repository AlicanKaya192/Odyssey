# Performans ve Profil

Model doğru çalışıyor ama yavaş. İlk kural: **tahmin etme, ölç.** Yavaşlığın
nerede olduğu çoğu zaman sanıldığı yerde değildir; çoğu zaman modelin
kendisi değil, onun çevresindeki Python kodudur. Bu bölümde süre ölçmeyi,
profil çıkarmayı ve PyTorch'un hız ve bellek için sunduğu birkaç aracı
görüyoruz.

Süreler makineden makineye değişir; bu yüzden aşağıdaki çıktılarda süre
yazmıyoruz, yalnızca **karşılaştırma** yazıyoruz. Karşılaştırmalar geniş
paylı: bu bilgisayarda aradaki farklar onlarca kat.

## Döngü değil, toplu iş

```python
import time
import torch
from torch import nn


def timeit(fn, repeat=5):
    best = float("inf")
    for _ in range(repeat):
        start = time.perf_counter()
        fn()
        best = min(best, time.perf_counter() - start)
    return best


torch.manual_seed(0)
model = nn.Sequential(nn.Linear(64, 128), nn.ReLU(), nn.Linear(128, 10)).eval()
x = torch.randn(512, 64)
with torch.no_grad():
    loop = timeit(lambda: [model(row) for row in x])
    batch = timeit(lambda: model(x))
print(batch < loop / 10)
```

```text
True
```

- `time.perf_counter()` duvar saatinin en hassas ölçeri; süre ölçmek için
  `time.time()` değil bu kullanılır.
- `timeit` aynı işi birkaç kez yapıp **en kısasını** alıyor: ilk çağrıdaki
  hazırlık ve arka plandaki başka işler ölçümü şişirmesin.
- 512 satırı tek tek modele vermek, hepsini tek bir `(512, 64)` tensörü
  olarak vermekten on kattan çok yavaş (bu bilgisayarda onlarca
  kat). Her çağrıda Python'un ve PyTorch'un sabit bir maliyeti var; toplu
  iş bu maliyeti bir kez öder, hesabı da optimize edilmiş matris çarpımına
  bırakır.

## `no_grad` ve `inference_mode`

```python
y = model(x)
print(y.requires_grad, y.grad_fn is not None)
with torch.inference_mode():
    z = model(x)
print(z.requires_grad, z.grad_fn is None, z.is_inference())
```

```text
True True
False True True
```

- Normal çağrıda PyTorch geri yayılım için hesap grafiğini kurar ve ara
  sonuçları bellekte tutar (`grad_fn`).
- Tahmin yaparken buna gerek yok. `torch.no_grad()` grafiği kurmaz;
  `torch.inference_mode()` bir adım daha ileri gider ve çıkan tensörleri
  "yalnızca tahmin" diye işaretler, böylece PyTorch bazı iç kayıtları da
  atlar.
- Kazanç her şeyden önce **bellek**. Hız farkı küçük modelde ölçülemeyecek
  kadar az olabilir; büyük modelde ve büyük grupta belirginleşir.

## Bellek: parametreler ve sayı türü

```python
params = sum(p.numel() for p in model.parameters())
print(params, params * 4, params * 2)
with torch.autocast("cpu", dtype=torch.bfloat16):
    print(model(x).dtype)
```

```text
9610 38440 19220
torch.bfloat16
```

- Model 9610 parametre. `float32` bir sayı 4 bayt; `bfloat16` 2 bayt.
  Parametrelerin belleği türle doğrudan yarıya iner.
- `torch.autocast` karışık duyarlık (mixed precision) kipidir: içinde
  matris çarpımı gibi işlemler daha küçük türle yapılır, duyarlığa hassas
  işlemler (toplamlar, kayıplar) `float32`'de kalır. Çıkış `bfloat16`.
  Ekran kartında aynı iş `torch.autocast("cuda", dtype=torch.float16)` ile
  yapılır ve hız kazancı CPU'dakinden çok daha büyüktür.

## Profil: süre nerede?

`torch.profiler` her PyTorch işlemini ve kendi verdiğin etiketli bölümleri
kaydeder. Aşağıda veriyi satır satır normalize eden (yavaş) bir hazırlık
adımı ile modeli ayrı etiketlerle ölçüyoruz.

```python
from torch.profiler import profile, ProfilerActivity, record_function

with profile(activities=[ProfilerActivity.CPU]) as prof:
    with record_function("prepare"):
        rows = torch.stack([(r - r.mean()) / r.std() for r in x])
    with record_function("model"):
        with torch.no_grad():
            model(rows)
events = {e.key: e for e in prof.key_averages()}
print(sorted(k for k in events if k in ("prepare", "model", "aten::linear")))
print(events["prepare"].cpu_time_total > events["model"].cpu_time_total)
```

```text
['aten::linear', 'model', 'prepare']
True
```

- `record_function("ad")` bir bölümü adlandırır; profilde o adla görünür.
  `aten::linear` PyTorch'un doğrusal katman için çağırdığı iç işlem.
- Sonuç tahmin edilenin tersi: **modeli çalıştırmak, veriyi hazırlamaktan
  hızlı**. Satır satır normalize etmek yerine
  `(x - x.mean(1, keepdim=True)) / x.std(1, keepdim=True)` tek satırda,
  toplu yapar.
- Tablonun tamamını görmek için
  `prof.key_averages().table(sort_by="cpu_time_total", row_limit=10)`
  yazdırılır; süre içerdiği için burada göstermiyoruz.

## `torch.compile`

`torch.compile(model)` modeli izleyip işlemleri birleştiren, daha hızlı
kod üreten bir derleyiciden geçirir. Varsayılan arka uç (inductor) makinede
bir C++ derleyicisi ister; Windows'ta Visual Studio'nun derleyicisi kurulu
değilse ilk çağrıda hata verir (bu bilgisayarda `cl is not found`).
`backend="eager"` derleyici istemez: yalnızca izleme kısmını çalıştırır,
hız kazandırmaz ama kodun derlemeye uygun olduğunu sınar.

```python
compiled = torch.compile(model, backend="eager")
with torch.no_grad():
    print(torch.equal(compiled(x), model(x)))
```

```text
True
```

Derleme ilk çağrıda zaman alır ve kazancı modele, donanıma ve grup boyuna
göre değişir: ölçmeden "hızlandı" denmez.

## Özet

- Önce ölç: `time.perf_counter`, birkaç tekrarın en kısası; süre değil oran
  karşılaştır.
- Satır satır değil toplu iş: sabit maliyet bir kez ödenir.
- Tahminde `torch.inference_mode()` (ya da `no_grad`): grafik yok, bellek
  az.
- `bfloat16` / `autocast`: bellek yarıya iner.
- `torch.profiler` + `record_function`: süre nerede, gör.
- `torch.compile` derleyici ister; kazancını ölç.
