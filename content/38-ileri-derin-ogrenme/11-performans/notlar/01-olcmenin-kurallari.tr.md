Yanlış ölçüm, hiç ölçmemekten kötüdür: yanlış yeri "düzeltip" asıl
darboğazı bırakırsın. Birkaç kural ölçümü güvenilir yapar.

## Kurallar

- **Isınma:** ilk çağrı hep yavaştır (bellek ayırma, önbellek, derleme).
  Ölçmeden önce bir kez çalıştır ya da birkaç tekrarın en kısasını al.
- **Tekrar:** tek ölçüm gürültüdür. Arka planda çalışan başka bir program
  bir ölçümü iki katına çıkarabilir; en kısası işin gerçek maliyetine en
  yakın olanıdır.
- **Aynı koşul:** karşılaştırdığın iki yol aynı veriyle, aynı grup boyuyla,
  aynı iş parçacığı sayısıyla ölçülür. PyTorch CPU'da birden çok iş parçacığı
  kullanır (`torch.get_num_threads()`); başka bir makinede bu sayı
  farklıdır ve süreler de farklı çıkar.
- **Oranla düşün:** "0,3 sn" bir şey söylemez; "toplu iş on kattan hızlı"
  her makinede anlamlıdır.

## Python döngüsü mü, tensör işlemi mi?

En sık görülen yavaşlık, tensörün elemanlarını Python'da tek tek gezmektir.

```python
import time
import torch


def timeit(fn, repeat=3):
    best = float("inf")
    for _ in range(repeat):
        start = time.perf_counter()
        fn()
        best = min(best, time.perf_counter() - start)
    return best


t = torch.randn(100_000, generator=torch.Generator().manual_seed(0))
slow = timeit(lambda: sum(v for v in t.tolist()))
fast = timeit(lambda: t.sum())
print(fast < slow / 10)
print(abs(sum(t.tolist()) - t.sum().item()) < 1e-2)
```

```text
True
True
```

- Aynı toplam: Python her sayıyı ayrı bir nesne olarak toplar; `t.sum()`
  bütün diziyi C kodunda, tek çağrıda toplar. Bu bilgisayarda fark onlarca
  kat.
- İkinci satır: iki sonuç birebir aynı değil (kayan noktada toplama sırası
  son basamakları değiştirir) ama aynı sayı.

Aynı kural her yerde geçerli: `for` ile satır gezen bir ön işleme,
`.item()` çağrılarıyla dolu bir döngü ya da her adımda `print` eden bir
eğitim döngüsü, modelin kendisinden çok zaman yiyebilir.
