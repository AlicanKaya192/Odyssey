Derste `argmax` kullandık: arıza olasılığı 0,5'i geçerse arıza. Ama iki hata
türünün bedeli eşit değil. Arızayı kaçırmak (yanlış negatif) makinenin
bozulmasına, gereksiz alarm (yanlış pozitif) bir teknisyenin boşuna bakmasına
yol açar. Bedeller farklıysa eşik de 0,5 olmak zorunda değil: **bedeli en
küçük eşik** seçilir.

Aşağıda on pencere için elle yazılmış arıza olasılıkları ve gerçek etiketler
var; kaçırılan arızanın bedeli 10, gereksiz alarmınki 1:

```python
import torch

probs = torch.tensor([0.05, 0.1, 0.2, 0.35, 0.4, 0.55, 0.6, 0.8, 0.9, 0.95])
labels = torch.tensor([0, 0, 0, 1, 0, 0, 1, 1, 1, 1])


def costs(threshold, fn_cost=10, fp_cost=1):
    pred = (probs >= threshold).long()
    fn = ((pred == 0) & (labels == 1)).sum().item()
    fp = ((pred == 1) & (labels == 0)).sum().item()
    return fn, fp, fn * fn_cost + fp * fp_cost


for t in [0.5, 0.3]:
    print(t, costs(t))
print(min([0.1, 0.2, 0.3, 0.4, 0.5, 0.6], key=lambda t: costs(t)[2]))
```

```text
0.5 (1, 1, 11)
0.3 (0, 2, 2)
0.3
```

- Eşik 0,5: bir arıza kaçtı (0,35 olasılıklı), bir gereksiz alarm var;
  bedel 11.
- Eşik 0,3: hiç arıza kaçmadı, iki gereksiz alarm; bedel 2. Daha çok alarm
  ama çok daha ucuz.
- Aday eşikler içinde en ucuzu 0,3.

Eşik düştükçe duyarlılık artar ya da aynı kalır, kesinlik genellikle düşer:
ikisi birbirine karşı çeker. Gerçek projede bu hesap modelin **doğrulama**
verisindeki olasılıklarıyla yapılır
(`torch.softmax(model(x[val]), dim=1)[:, 1]`), seçilen eşik teslim paketinin
açıklamasına yazılır ve testte bir kez ölçülür. Bedeller bir mühendislik
kararıdır; modelden değil işin kendisinden gelir.
