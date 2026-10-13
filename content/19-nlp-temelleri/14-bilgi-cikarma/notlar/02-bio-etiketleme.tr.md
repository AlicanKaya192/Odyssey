Kurallar yetmediğinde bilgi çıkarma bir **sıra etiketleme** (sequence
labelling) problemine çevrilir: her token'a bir etiket verilir ve model
etiketleri öğrenir. En yaygın etiket biçimi **BIO**:

| Etiket | Anlamı |
|---|---|
| `B-TÜR` | Bir varlığın ilk token'ı (begin) |
| `I-TÜR` | Aynı varlığın devamı (inside) |
| `O` | Hiçbir varlığın parçası değil (outside) |

Kuralla bulduğumuz parçaları BIO etiketlerine çevirelim. Böyle etiketlenmiş
metinler, bir modeli eğitmek için veri olur:

```python
import re

PATTERNS = {"AMOUNT": r"\$\d+\.\d{2}", "ORDER": r"\bORD-\d{5}\b",
            "DATE": r"\b\d{1,2} [A-Z][a-z]+ \d{4}\b"}


def bio(text):
    tokens = list(re.finditer(r"\S+", text))
    tags = ["O"] * len(tokens)
    for kind, pattern in PATTERNS.items():
        for match in re.finditer(pattern, text):
            inside = [i for i, t in enumerate(tokens)
                      if t.start() < match.end() and t.end() > match.start()]
            for n, i in enumerate(inside):
                tags[i] = ("B-" if n == 0 else "I-") + kind
    return [(t.group(), tag) for t, tag in zip(tokens, tags)]


for token, tag in bio("Refund $12.49 for ORD-12345 sent on 13 October 2026."):
    print(f"{token:<10} {tag}")
```

```text
Refund     O
$12.49     B-AMOUNT
for        O
ORD-12345  B-ORDER
sent       O
on         O
13         B-DATE
October    I-DATE
2026.      I-DATE
```

- Bir token bir eşleşmeyle **örtüşüyorsa** o varlığa ait: "2026." sonundaki
  noktayla birlikte tek token, ama tarihin parçası.
- Üç token'lık tarih `B-DATE I-DATE I-DATE`. `I-` olmadan, art arda gelen iki
  ayrı varlığı tek bir uzun varlıktan ayırmak mümkün olmazdı.
- Bir model bu etiketleri öğrenirken her token'ın kendisine ve
  **komşularına** bakar ("$" ile başlıyor mu, önceki token "refund" mu,
  önceki etiket `B-` mi). Etiketler birbirine bağlı olduğu için tek tek
  sınıflandırma yerine bütün sırayı birlikte çözen yöntemler kullanılır.
  Gömmeler ve Dil Modelleri modülünde HMM ve Viterbi algoritmasıyla tam
  bunu yapacağız.
