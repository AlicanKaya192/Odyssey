Derste aynı anlamı taşıyan aday BLEU'dan 0,001 almıştı, çünkü tek bir
referans vardı. Bir cümle birçok doğru biçimde söylenebildiği için BLEU
baştan **birden çok referansla** tasarlandı: her kelime grubu, referanslardan
birinde en çok kaç kez geçiyorsa o kadar sayılır; kısalık cezası boyca en
yakın referansa göre hesaplanır.

```python
def bleu_multi(candidate, references, max_n=4):
    c = candidate.split()
    refs = [r.split() for r in references]
    logs = []
    for n in range(1, max_n + 1):
        cand = ngrams(c, n)
        best = Counter()
        for r in refs:
            best |= ngrams(r, n)
        clipped = sum(min(k, best[g]) for g, k in cand.items())
        logs.append(math.log(max(clipped, 1e-9) / max(sum(cand.values()), 1)))
    closest = min((abs(len(r) - len(c)), len(r)) for r in refs)[1]
    brevity = min(1.0, math.exp(1 - closest / len(c)))
    return round(brevity * math.exp(sum(logs) / max_n), 3)


second = ("the package is coming on monday and you will get "
          "a tracking number by email")
for cand in candidates[1:3]:
    print(bleu(cand, reference), bleu_multi(cand, [reference, second]))
```

```text
0.702 0.717
0.001 0.714
```

- İkinci bir referans eklenince eş anlamlı aday 0,001'den 0,714'e çıkıyor;
  ilk aday neredeyse yerinde kalıyor (0,702 → 0,717).
- `Counter`'ların `|` işlemi her grubun en büyük sayısını alır: bir grup
  birinci referansta 1, ikincide 2 kez geçiyorsa 2'ye kadar sayılır.
- Çeviri sınav kümeleri bu yüzden çoğu zaman cümle başına 2–4 insan
  çevirisiyle hazırlanır. Ama referans yazmak pahalıdır ve hiçbir referans
  kümesi bütün doğru cevapları kapsamaz.
