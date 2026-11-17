# Modeli Dışa Aktarmak

Derin Öğrenmenin Temelleri modülünde modeli `state_dict` ile kaydettik.
O dosya yalnızca **sayıları** taşır: yüklemek için modelin sınıfını
yazan Python kodu da elinde olmalı. Modeli başka bir programa, sunucuya ya
da telefona göndermek istediğinde bu yetmez. **Dışa aktarma** (export),
modelin hesabını da (hangi işlem hangi sırayla) dosyaya yazar; dosyayı
açan programın senin sınıfını bilmesi gerekmez.

<figure class="fig">
<div class="flow">
<span class="node">nn.Module</span><span class="arrow">→</span>
<span class="node acc">torch.export</span><span class="arrow">→</span>
<span class="node">hesap grafiği</span><span class="arrow">→</span>
<span class="node ok">model.pt2</span>
</div>
<figcaption>Dışa aktarma modeli örnek bir girdiyle bir kez çalıştırır, yaptığı işlemleri kaydeder ve ağırlıklarla birlikte tek bir dosyaya yazar.</figcaption>
</figure>

PyTorch'ta bunun güncel yolu `torch.export`. Eski yol TorchScript'i ve
programlar arası ortak biçim ONNX'i bölümün sonunda anıyoruz.

## `torch.export`

```python
import torch
from torch import nn


class Net(nn.Module):
    def __init__(self):
        super().__init__()
        self.body = nn.Sequential(nn.Linear(8, 16), nn.ReLU(), nn.Linear(16, 2))

    def forward(self, x):
        return self.body(x)


torch.manual_seed(0)
model = Net().eval()
x = torch.randn(4, 8)
ep = torch.export.export(model, (x,))
print(type(ep).__name__, torch.allclose(ep.module()(x), model(x)))
ops = [str(n.target) for n in ep.graph.nodes if n.op == "call_function"]
print([op.removeprefix("aten.") for op in ops])
```

```text
ExportedProgram True
['linear.default', 'relu.default', 'linear.default']
```

- `torch.export.export(model, (x,))` modeli örnek girdi `x` ile izler.
  Sonuç bir `ExportedProgram`: ağırlıklar ve işlemlerin grafiği.
- `ep.module()` grafiği yeniden çağrılabilir bir modüle çevirir; çıktısı
  özgün modelinkiyle aynı.
- Grafikteki işlemler PyTorch'un temel işlemleri (adları `aten.` ile
  başlıyor, kısa olsun diye attık): iki doğrusal
  katman, arada ReLU. `nn.Sequential`, `Net` gibi Python yapıları
  grafikte yok; yalnızca hesap kaldı.

## Grup boyunu serbest bırakmak

İzleme sırasında örnek girdinin şekli de kaydedilir. Başka bir grup boyuyla
çağırınca ne olur?

```python
try:
    ep.module()(torch.randn(7, 8))
except Exception as e:
    print(type(e).__name__, "Guard failed" in str(e))

batch = torch.export.Dim("batch")
ep = torch.export.export(model, (x,), dynamic_shapes={"x": {0: batch}})
print(ep.module()(torch.randn(7, 8)).shape, ep.module()(torch.randn(1, 8)).shape)
```

```text
AssertionError True
torch.Size([7, 2]) torch.Size([1, 2])
```

- İlk dışa aktarma grup boyunu 4'e **sabitledi**; 7 satırlık girdi
  "koruma" (guard) denetiminden geçemedi.
- `torch.export.Dim("batch")` ile 0. boyut serbest: `dynamic_shapes`
  sözlüğünün anahtarı `forward`'ın argüman adı (`x`), değeri hangi boyutun
  serbest olduğu. Artık 7 de 1 de çalışıyor.
- Sunulacak bir modelde grup boyu hemen her zaman serbest bırakılır.

## Kaydetmek ve sınıfsız yüklemek

```python
torch.export.save(ep, "model.pt2")
del Net, model
loaded = torch.export.load("model.pt2").module()
print(type(loaded).__name__, loaded(x).shape)
```

```text
GraphModule torch.Size([4, 2])
```

- `del Net` ile sınıfı bile sildik; yükleme yine çalıştı. Dosyayı açan
  programın elinde yalnızca PyTorch olması yetiyor.
- `.pt2` dosyası bir zip arşivi: ağırlıklar, grafik ve şekil kuralları
  içinde.

## Eski ve ortak biçimler

**TorchScript** (`torch.jit.trace`, `torch.jit.script`) PyTorch'un eski
dışa aktarma yolu. Bu bilgisayardaki sürümde (PyTorch 2.15, Python 3.14)
her ikisi de "Python 3.14 ve sonrasında desteklenmiyor, `torch.export`'a
geçin" uyarısı veriyor (`FutureWarning`). `torch.jit.script` ayrıca
modelin Python kaynak kodunu okumak zorunda; kaynağı olmayan bir ortamda
(yalnızca derlenmiş `.pyc` dosyaları) çalışmaz. Yeni kodda `torch.export`
kullanılır; notlarda `trace`'in sessiz bir tuzağını göreceğiz.

**ONNX** farklı çerçevelerin ve çalıştırıcıların ortak model biçimi:
PyTorch'ta eğitilen model ONNX'e aktarılıp başka bir dilde ya da cihazda
özel bir çalıştırıcıyla kullanılabilir. PyTorch'un ONNX dışa aktarıcısı ek
paketler (`onnx`, `onnxscript`) istiyor; bu programda kurulu olmadıkları
için kodu yalnızca gösteriyoruz:

```
torch.onnx.export(model, (x,), "model.onnx", dynamo=True,
                  dynamic_shapes={"x": {0: torch.export.Dim("batch")}})
```

Görüldüğü gibi ONNX dışa aktarıcısı da arkada `torch.export`'u kullanıyor:
şekil kuralları aynı.

## Özet

- `state_dict` sayıları taşır, sınıf kodu gerekir; dışa aktarma hesabı da
  taşır.
- `torch.export.export(model, (örnek,))` → `ExportedProgram`;
  `.module()` çağrılabilir.
- Grup boyu `Dim` ile serbest bırakılmazsa örnek girdinin boyuna sabitlenir.
- `torch.export.save` / `load`: `.pt2`, sınıf olmadan yüklenir.
- TorchScript eskidi; ONNX ek paket ister ve arkada aynı yolu kullanır.
