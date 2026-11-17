Bu program PyTorch'u CPU'da çalıştırıyor. Gerçek eğitimler çoğu zaman bir
ekran kartında (GPU) yapılır; Mac'lerde de bilgisayarın kendi grafik birimi
(`mps`) kullanılabilir. Kodu baştan **cihazdan bağımsız** yazmak, aynı dosyanın her
yerde çalışmasını sağlar.

```python
import torch
from torch import nn

if torch.cuda.is_available():
    device = torch.device("cuda")
elif torch.backends.mps.is_available():
    device = torch.device("mps")
else:
    device = torch.device("cpu")

model = nn.Linear(8, 2).to(device)
x = torch.randn(4, 8).to(device)
print(model(x).shape)
print(next(model.parameters()).device.type in ("cpu", "cuda", "mps"))
```

```text
torch.Size([4, 2])
True
```

- Model ve veri **aynı cihazda** olmalı; biri CPU'da biri GPU'da ise
  PyTorch hata verir. `.to(device)` ikisini de taşır.
- Hangi cihazın seçildiği makineye bağlı; çıktı yalnızca şekli ve cihazın
  bilinen türlerden biri olduğunu yazıyor.

## GPU'da dikkat edilecekler

- **Taşıma maliyeti:** CPU ile GPU arasında veri kopyalamak yavaştır. Veriyi
  her adımda küçük parçalar hâlinde gidip getirmek yerine grup grup taşı;
  sonuçları her adımda `.item()` ile CPU'ya çekme.
- **`DataLoader(pin_memory=True)`:** veriyi kopyalanmaya hazır bellekte
  tutar; `.to(device, non_blocking=True)` ile birlikte kopyalama hesapla
  üst üste biner.
- **Zamanlama tuzağı:** GPU işleri sıraya koyar ve hemen döner. Süre
  ölçerken `torch.cuda.synchronize()` çağrılmazsa ölçülen şey işin kendisi
  değil, sıraya koyma süresidir.
- **Grup boyu:** GPU büyük gruplarda verimlidir; bellek yettiği kadar büyük
  grup çoğu zaman daha hızlıdır. Bellek yetmiyorsa karışık duyarlık
  (`autocast`) önce denenecek şeydir.
