# Aşırı Öğrenme ve Düzenlileştirme

Eğitim Döngüsü bölümünde doğrulama kaybının bir noktadan sonra yükseldiğini
gördük: model eğitim verisini **ezberlemeye** başlamıştı. Buna **aşırı
öğrenme** (overfitting) denir. Sinir ağları çok parametreli olduğu için az
veride kolayca ezberler. Bu bölümde aşırı öğrenmeyi bilerek büyütüp ona
karşı dört aracı deneyeceğiz: **Dropout**, **ağırlık çürümesi** (weight
decay), **erken durdurma** (early stopping) ve daha küçük model. Makine
öğrenmesi patikasındaki düzenlileştirme fikrinin (L2 cezası, ağaç budama)
derin öğrenmedeki karşılıkları bunlar.

## Aşırı öğrenmeyi büyütmek

Eğitim için yalnızca 80 örnek, doğrulama için 320 örnek ayıralım ve 80
örneğe göre çok büyük bir ağ kuralım (iki gizli katman, 128'er nöron):

```python
import torch
from torch import nn
from dl_data import make_table

x_np, y_np = make_table(400, seed=11)
x, y = torch.from_numpy(x_np), torch.from_numpy(y_np)
x_tr, y_tr, x_val, y_val = x[:80], y[:80], x[80:], y[80:]
loss_fn = nn.CrossEntropyLoss()


def fit(model, epochs=200, weight_decay=0.0):
    optimizer = torch.optim.AdamW(model.parameters(), lr=0.01, weight_decay=weight_decay)
    for _ in range(epochs):
        model.train()
        optimizer.zero_grad()
        loss_fn(model(x_tr), y_tr).backward()
        optimizer.step()
    model.eval()
    with torch.no_grad():
        train_acc = (model(x_tr).argmax(dim=1) == y_tr).float().mean().item()
        val_loss = loss_fn(model(x_val), y_val).item()
    return round(train_acc, 2), round(val_loss, 1)


def big_net(p=0.0):
    torch.manual_seed(0)
    return nn.Sequential(nn.Linear(6, 128), nn.ReLU(), nn.Dropout(p),
                         nn.Linear(128, 128), nn.ReLU(), nn.Dropout(p),
                         nn.Linear(128, 3))


print("big", fit(big_net()))
```

```text
big (1.0, 2.4)
```

Eğitim doğruluğu **%100**: model 80 örneğin hepsini ezberledi. Ama
doğrulama kaybı 2,4: görmediği örneklerde çok emin ve sık sık
yanlış. Ezber, öğrenme değil.

## Dropout

**Dropout** eğitim sırasında her adımda nöronların rastgele bir kısmını
(ör. yarısını) sıfırlar. Ağ tek bir nörona güvenemez; bilgiyi birçok yola
yaymak zorunda kalır. Değerlendirmede (`model.eval()`) Dropout kapanır:

```python
drop = nn.Dropout(p=0.5)
ones = torch.ones(10)
torch.manual_seed(0)
print(drop(ones).tolist())
drop.eval()
print(drop(ones).tolist())
```

```text
[0.0, 0.0, 2.0, 0.0, 0.0, 0.0, 2.0, 2.0, 0.0, 2.0]
[1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0]
```

- Eğitim kipinde elemanların bir kısmı 0, kalanlar **2,0**: Dropout kalan
  değerleri `1 / (1 − p)` ile büyütüyor ki çıktının ortalaması değişmesin.
- `eval()` kipinde hiçbir şey değişmiyor. nn.Module bölümünde
  `model.eval()`'in neden önemli olduğunu söylemiştik: unutulursa tahminler
  her çalıştırmada rastgele değişir.

## Ağırlık çürümesi ve küçük model

**Ağırlık çürümesi** (weight decay) her adımda ağırlıkları biraz sıfıra
doğru çeker: büyük ağırlıklar cezalandırılır, model daha "yumuşak" kalır.
`AdamW`'de `weight_decay` parametresi. Bir de en basit çare var: daha
küçük bir model.

```python
print("dropout", fit(big_net(p=0.5)))
print("decay", fit(big_net(), weight_decay=1.0))
torch.manual_seed(0)
print("small", fit(nn.Sequential(nn.Linear(6, 8), nn.ReLU(), nn.Linear(8, 3))))
```

```text
dropout (1.0, 1.6)
decay (1.0, 1.2)
small (0.95, 0.8)
```

Dropout ve ağırlık çürümesinde eğitim doğruluğu yine %100 (80 örneği
ezberlemek kolay), küçük modelde %95; üçünde de doğrulama kaybı düştü. Hiçbiri sihirli değil; her biri ezberlemeyi
zorlaştırıp modeli genel kurallara itiyor.

## Erken durdurma

En güçlü ve en ucuz çare, doğrulama kaybını izleyip **iyileşmeyi bıraktığı
anda durmak**. Belli bir sayıda tur (sabır, patience) boyunca iyileşme
olmazsa eğitim kesilir ve en iyi duruma dönülür:

```python
def early_stopping_fit(model, patience=10, max_epochs=200):
    optimizer = torch.optim.AdamW(model.parameters(), lr=0.01)
    best, best_epoch, waited = float("inf"), 0, 0
    for epoch in range(1, max_epochs + 1):
        model.train()
        optimizer.zero_grad()
        loss_fn(model(x_tr), y_tr).backward()
        optimizer.step()
        model.eval()
        with torch.no_grad():
            val_loss = loss_fn(model(x_val), y_val).item()
        if val_loss < best:
            best, best_epoch, waited = val_loss, epoch, 0
        else:
            waited += 1
            if waited == patience:
                break
    return best_epoch, epoch, round(best, 2)


print(early_stopping_fit(big_net()))
```

```text
(4, 14, 0.36)
```

En iyi doğrulama kaybı 4. turda geldi; 10 tur iyileşme
olmayınca eğitim 14. turda durdu. Doğrulama kaybı
(0,36) öteki çarelerin hepsinden düşük ve eğitim çok daha
kısa. (Burada en iyi durumu saklamadık; gerçek kodda Eğitim Döngüsü
bölümündeki gibi `copy.deepcopy(model.state_dict())` ile saklanır.)

## Daha çok veri

Aşırı öğrenmenin kökü, modelin gücüne göre az veri. Aynı büyük ağı 80
yerine 800 örnekle 200 tur eğitelim:

```python
x2_np, y2_np = make_table(1120, seed=11)
x_tr = torch.from_numpy(x2_np[:800])
y_tr = torch.from_numpy(y2_np[:800])
x_val, y_val = torch.from_numpy(x2_np[800:]), torch.from_numpy(y2_np[800:])
print("big + 800", fit(big_net()))
```

```text
big + 800 (1.0, 1.6)
```

200 turda bu büyük ağ 800 örneğin de hepsini ezberledi (eğitim doğruluğu
yine %100), ama doğrulama kaybı 2,4 değerinden
1,6 değerine indi: daha çok veri ezberi zorlaştırıyor. Yine de
bu ağ için 800 örnek de az; erken durdurma burada hâlâ en etkili çare.

Çareler birbirinin yerine değil, birlikte kullanılır: elde edilebilen her
veri, makul büyüklükte bir model, biraz Dropout ya da ağırlık çürümesi ve
her zaman erken durdurma.

## Özet

- Aşırı öğrenme: eğitimde mükemmel, görülmemiş veride kötü. Az veri, çok
  parametre.
- Dropout eğitimde nöronları rastgele kapatır, `eval()`'de kapanır.
- Ağırlık çürümesi (`AdamW(weight_decay=...)`) ağırlıkları küçük tutar.
- Erken durdurma doğrulama kaybı iyileşmeyi bırakınca durur.
- Daha çok veri ezberi zorlaştırır. Çareler birlikte kullanılır; erken
  durdurma her zaman.
