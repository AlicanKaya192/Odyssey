# LSTM ile Zaman Serisi Tahmini

Zaman Serileri patikası tahmini istatistik yöntemleriyle anlattı: mevsimsel
naif tahmin, üstel düzeltme, ARIMA ve en önemli ders olarak **bir taban
çizgisini yenmeden modele güvenmemek**. Bu bölüm aynı işi bir LSTM ile
yapıyor: geçmiş 28 günü okuyup ertesi günü tahmin eden bir ağ. Yöntem yeni,
kurallar eski: zamana göre bölmek, ölçeklemeyi yalnızca geçmişten öğrenmek
ve sonucu naif tahminlerle karşılaştırmak.

Seri `make_series`'ten: iki yıllık günlük değer; yükselen bir eğilim, haftalık
ve yıllık mevsim, üstüne gürültü.

## Pencereler: diziden örneğe

Bir LSTM'e "seri" verilmez, **pencere** verilir: art arda 28 değer girdi,
hemen sonraki değer hedef. Pencere bir gün kaydırılarak yeni örnek çıkar.

```python
import numpy as np
import torch
from torch import nn
from dl_data import make_series

series = make_series(730)
split = 630
mean, std = series[:split].mean(), series[:split].std()
scaled = (series - mean) / std


def windows(values, size):
    xs = [values[i:i + size] for i in range(len(values) - size)]
    ys = [values[i + size] for i in range(len(values) - size)]
    return torch.tensor(np.array(xs)).unsqueeze(-1), torch.tensor(np.array(ys))


x_train, y_train = windows(scaled[:split], 28)
x_test, y_test = windows(scaled[split - 28:], 28)
print(series.shape, x_train.shape, y_train.shape)
print(x_test.shape, y_test.shape)
```

```text
(730,) torch.Size([602, 28, 1]) torch.Size([602])
torch.Size([100, 28, 1]) torch.Size([100])
```

- **Zamana göre bölme:** ilk 630 gün eğitim, son 100 gün test. Karıştırarak
  bölmek geleceği eğitime sızdırırdı.
- **Ölçekleme yalnızca eğitimden:** ortalama ve standart sapma ilk 630
  günden. Bütün seriden hesaplasaydık test döneminin seviyesi eğitime sızardı
  (eğilim ve yıllık mevsim yüzünden test döneminin seviyesi farklı; ikinci
  not).
- Test pencereleri eğitimin son 28 gününden başlıyor ki test döneminin ilk
  günü de tahmin edilebilsin: 100 test günü, 100 pencere.
- Girdinin son boyutu 1: her adımda tek sayı var. `unsqueeze(-1)` şekli
  `(N, 28)`'den `(N, 28, 1)`'e getiriyor; LSTM `(B, T, D)` ister.

## Model ve eğitim

```python
class Forecaster(nn.Module):
    def __init__(self, hidden=32):
        super().__init__()
        self.lstm = nn.LSTM(1, hidden, batch_first=True)
        self.head = nn.Linear(hidden, 1)

    def forward(self, x):
        out, (h, c) = self.lstm(x)
        return self.head(h[-1]).squeeze(-1)


torch.manual_seed(0)
model = Forecaster()
loader = torch.utils.data.DataLoader(
    torch.utils.data.TensorDataset(x_train, y_train), batch_size=32, shuffle=True,
    generator=torch.Generator().manual_seed(0))
opt = torch.optim.Adam(model.parameters(), lr=0.005)
loss_fn = nn.MSELoss()
for epoch in range(20):
    model.train()
    for xb, yb in loader:
        opt.zero_grad()
        loss = loss_fn(model(xb), yb)
        loss.backward()
        opt.step()
print(model(x_test[:3]).shape)
```

```text
torch.Size([3])
```

- Bu bir **bağlanım** (regression): çıkış tek sayı, kayıp ortalama kare hata
  (`MSELoss`). `squeeze(-1)` `(B, 1)`'i `(B,)` yapar ki hedefle aynı şekilde
  olsun; yoksa yayınlama `(B, B)`'lik yanlış bir fark matrisi kurar ve kayıp
  sessizce yanlış hesaplanır.
- 20 epoch bu bilgisayarda birkaç saniye sürdü.

## Taban çizgileriyle karşılaştırmak

Tahminleri ölçekten geri çevirip asıl birimde **ortalama mutlak hata**
(MAE) ile ölçüyoruz. İki taban çizgisi: dünün değeri (naif) ve geçen haftanın
aynı günü (mevsimsel naif).

```python
model.eval()
with torch.no_grad():
    pred = model(x_test).numpy() * std + mean
actual = series[split:]
mae_lstm = np.abs(pred - actual).mean()
mae_naive = np.abs(series[split - 1:-1] - actual).mean()
mae_week = np.abs(series[split - 7:-7] - actual).mean()
print(round(float(mae_naive), 1), round(float(mae_week), 1))
print(round(float(mae_lstm), 1))
print(mae_lstm < mae_naive, mae_lstm < mae_week)
```

```text
4.8 2.4
1.9
True True
```

- Naif tahmin 4,8, mevsimsel naif 2,4 birim
  hata yapıyor. Haftalık mevsim güçlü olduğu için geçen haftanın aynı günü
  dünden daha iyi bir tahmin.
- LSTM 1,9 ile ikisini de geçiyor: hem haftalık deseni hem
  son günlerin seviyesini birlikte kullanıyor.
- Serideki gürültünün standart sapması 2; böyle bir gürültünün ortalama
  mutlak değeri yaklaşık 1,6. Gürültü tahmin edilemediği için
  hiçbir model bunun altına inemez; LSTM bu sınıra yakın.

## Ne zaman LSTM?

Zaman Serileri patikasının ölçerek gösterdiği şey burada da geçerli: kazanç
çoğu zaman yöntemden değil **bilgiden** gelir (takvim, tatil, kampanya). LSTM
şu durumlarda öne çıkar:

| Durum | LSTM | İstatistik yöntemi |
|---|---|---|
| Tek, kısa seri | Az veriyle zor öğrenir | Çoğu zaman yeter ve daha iyi |
| Birbirine benzeyen yüzlerce seri | Tek modelle hepsini öğrenebilir | Her seri ayrı model |
| Birçok dış değişken, doğrusal olmayan ilişki | Doğal olarak alır | Elle özellik gerekir |
| Belirsizlik aralığı | Ek iş ister | Çoğu yöntemde hazır |

## Özet

- Seri pencerelere bölünür: `(N, T, 1)` girdi, sonraki değer hedef.
- Zamana göre böl; ölçekleme istatistiklerini yalnızca eğitim döneminden
  al.
- Bağlanımda `MSELoss`; çıkışı hedefle aynı şekle getir (`squeeze(-1)`),
  yoksa yayınlama sessizce yanlış kayıp hesaplar.
- Her zaman naif ve mevsimsel naif tahminle karşılaştır; modeli ancak
  ikisini de geçerse kullan.
