Uyarlama takılıyken model yeni görevde iyi, ama eski görevde artık
değil: derste ince ayardan sonra eski görevin verisiyle de bakarsak
doğruluk düşüyor. LoRA'nın asıl kolaylığı burada: taban bir kez saklanır,
her görev için yalnızca küçük `A` ve `B` saklanır ve gerektiğinde takılır.
Aşağıdaki kod dersteki eğitilmiş `net`'i kullanıyor.

```python
print(accuracy(net, xa, ya) < 0.6)
state = net.state_dict()
adapter = {k: state[k].clone() for k in ("0.A", "0.B")}
print(sorted(adapter), sum(v.numel() for v in adapter.values()))
fresh = nn.Sequential(LoRALinear(net[0].base, r=2), *net[1:])
print(accuracy(fresh, xb, yb) > 0.8)
result = fresh.load_state_dict(adapter, strict=False)
print(accuracy(fresh, xb, yb) > 0.8, len(result.missing_keys))
```

```text
True
['0.A', '0.B'] 140
False
True 6
```

- İlk satır: uyarlama takılıyken eski görevde doğruluk 0,6'nın altında.
- Uyarlayıcı yalnızca iki tensör, 140 sayı. Taban modelin tamamını her görev
  için yeniden saklamak yerine bu kadarını saklamak yeter.
- `fresh`: aynı tabanın üstünde **yeni** bir LoRA katmanı; `B` sıfır olduğu
  için davranışı tabanınki, yeni görevde başarısız.
- `load_state_dict(..., strict=False)` yalnızca verilen anahtarları yükler,
  ötekilere dokunmaz; eksik kalan 6 anahtar (taban ağırlıkları) beklenen
  durum. `strict=True` (varsayılan) olsaydı eksik anahtar yüzünden hata
  verirdi.
- Uyarlayıcı yüklenince yeni görevdeki başarı geri geldi.

Böylece tek bir taban modelin yanında onlarca görev için ayrı uyarlayıcı
tutulabilir; istek hangi göreve aitse onun `A`, `B`'si takılır. Taban
dondurulduğu için uyarlayıcılar birbirini bozmaz.
