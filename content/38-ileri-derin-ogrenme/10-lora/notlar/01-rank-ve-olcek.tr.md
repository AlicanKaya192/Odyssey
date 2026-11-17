LoRA'nın iki ayarı var: rank `r` ve ölçek `alpha`. Büyük modellerde neden
bu kadar sevildiğini sayılar gösteriyor. Bir dil modelinde sık görülen
4096 × 4096'lık bir katman için:

```python
import torch

for r in [1, 4, 16, 64]:
    lora = r * (4096 + 4096)
    print(r, lora, round(100 * lora / (4096 * 4096), 2))
```

```text
1 8192 0.05
4 32768 0.2
16 131072 0.78
64 524288 3.12
```

- Katmanın kendisi 16 777 216 sayı. Rank 16'lık LoRA yüzde birin altında
  kalıyor (sütun: tam katmanın yüzdesi).
- Rank büyüdükçe uyarlama daha çok şey öğrenebilir ama daha çok bellek ve
  veri ister. Çoğu iş için 4–16 arası yetiyor; en iyisi doğrulamayla seçilir.

`B · A` çarpımının rankı en fazla `r`'dir; ne kadar eğitilirse eğitilsin,
uyarlama ağırlığı bu sınırı aşamaz:

```python
gen = torch.Generator().manual_seed(0)
B = torch.randn(64, 4, generator=gen)
A = torch.randn(4, 64, generator=gen)
print((B @ A).shape, torch.linalg.matrix_rank(B @ A).item())
```

```text
torch.Size([64, 64]) 4
```

64 × 64'lük bir matris ama rankı 4. LoRA'nın varsayımı da bu: ince ayarın
yaptığı değişiklik az sayıda "yönde" toplanıyor.

## Ölçek: alpha / r

Derste uyarlamanın katkısı `alpha / r` ile çarpılıyordu. Bunun nedeni, rank
değiştirilince uyarlamanın büyüklüğünün kendiliğinden değişmesini önlemek:
`alpha` sabit kalırsa rank iki katına çıkınca her bileşenin payı yarıya
iner ve öğrenme oranını yeniden ayarlamak gerekmez. Yaygın seçimler
`alpha = 2 · r` ya da rankla birlikte değişmeyen sabit bir `alpha`'dır.

## LoRA nereye konur?

Derste tek bir katmana koyduk. Transformer'larda en yaygın yer dikkat
katmanının sorgu ve değer izdüşümleridir (`q` ve `v` doğrusal katmanları);
daha fazla katmana koymak daha esnek ama daha çok parametre demektir.
Kural aynı: hangi katmanın değişmesi gerektiğini düşünmek, sonra yalnızca
onları sarmak.
