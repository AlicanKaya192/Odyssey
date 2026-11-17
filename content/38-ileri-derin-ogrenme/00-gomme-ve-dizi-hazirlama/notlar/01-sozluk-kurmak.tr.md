Derste sözlüğe metindeki bütün kelimeleri koyduk. Gerçek veride bu iki
sorun çıkarır: sözlük çok büyür (her yazım hatası ayrı kelime olur) ve
eğitimde hiç `<unk>` görülmediği için ağ o vektörü hiç öğrenmez. Yaygın
çözüm: yalnızca en az birkaç kez geçen kelimeleri sözlüğe almak, gerisini
`<unk>` saymak.

```python
from collections import Counter
from dl_data import TEXT

sentences = [s.split() for s in TEXT.split(".") if s.strip()]
counts = Counter(w for s in sentences for w in s)
kept = sorted(w for w, c in counts.items() if c >= 2)
vocab = ["<pad>", "<unk>"] + kept
index = {w: i for i, w in enumerate(vocab)}
print(len(counts), len(kept), len(vocab))

new = "the fox sat on the warm mat".split()
ids = [index.get(w, 1) for w in new]
print(ids)
print(sum(i == 1 for i in ids))
```

```text
24 15 17
[13, 1, 10, 8, 13, 1, 1]
3
```

- 24 farklı kelimenin 15 tanesi en az iki kez
  geçiyor; sözlük özel işaretlerle 17 kelime.
- Yeni cümlede "fox" hiç geçmemişti, "warm" ve "mat" de yalnızca bir kez
  geçtiği için sözlüğe girmedi: üç kelime `<unk>` oldu.

## Kurallar

| Kural | Neden |
|---|---|
| Sözlüğü yalnızca eğitim verisinden kur | Test verisinin kelimeleri sözlüğe sızarsa başarı iyimser ölçülür |
| `<pad>` 0, `<unk>` 1 | `padding_idx=0` ve `index.get(w, 1)` hep aynı kalır |
| Seyrek kelimeleri `<unk>` say | Ağ `<unk>` vektörünü de öğrenir, sözlük küçülür |
| Sözlüğü modelle birlikte kaydet | Başka sırayla kurulan sözlük başka kimlikler verir, model yanlış satırları okur |

Son kural en sık unutulanı: `sorted` yazmasaydık kümenin sırası her
çalıştırmada değişebilirdi ve kaydedilen model yeni sözlükle anlamsız
sonuçlar verirdi.
