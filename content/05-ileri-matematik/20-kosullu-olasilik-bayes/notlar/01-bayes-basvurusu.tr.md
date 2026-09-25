Dersteki her şeyin kısa hâli. Bir soruda takıldığında buraya dön.

## Kurallar

| Ad | Formül |
|---|---|
| koşullu olasılık | $P(B \mid A) = \dfrac{P(A \cap B)}{P(A)}$ |
| çarpım kuralı | $P(A \cap B) = P(A) \, P(B \mid A)$ |
| toplam olasılık | $P(B) = \sum_i P(B \mid A_i) \, P(A_i)$ |
| Bayes | $P(A \mid B) = \dfrac{P(B \mid A) \, P(A)}{P(B)}$ |
| oran biçimi | sonsal oran $=$ önsel oran $\times$ olabilirlik oranı |
| koşullu bağımsızlık | $P(A \cap B \mid C) = P(A \mid C) \, P(B \mid C)$ |

## Adlar

| Terim | Anlamı |
|---|---|
| önsel $P(A)$ | kanıttan önceki inanç |
| olabilirlik $P(B \mid A)$ | $A$ doğruysa kanıtı görme olasılığı |
| kanıt $P(B)$ | kanıtın toplam olasılığı |
| sonsal $P(A \mid B)$ | kanıttan sonraki inanç |
| duyarlılık | $P(+ \mid \text{hasta})$ |
| yanlış pozitif oranı | $P(+ \mid \text{sağlıklı})$ |

## Test sorusu için şablon

1. Önseli yaz: $P(H)$.
2. Pozitifliğin iki yolu: $P(+ \mid H) P(H)$ ve $P(+ \mid S) P(S)$.
3. $P(+)$ bu ikisinin toplamı.
4. $P(H \mid +) = \frac{\text{birinci yol}}{P(+)}$.

Ya da $10\,000$ kişilik doğal sıklıklarla aynı dört adım.

## Ardışık güncelleme

Sonsal, bir sonraki bağımsız kanıtın önseli olur. Oran biçiminde her
kanıt oranı olabilirlik oranıyla bir kez daha çarpar.

## Naive Bayes

$$
P(\text{sınıf} \mid x_1, \dots, x_n) \propto P(\text{sınıf}) \prod_i P(x_i \mid \text{sınıf})
$$

En büyük değeri veren sınıf seçilir; olasılık gerekiyorsa toplama bölünür.

## Pratik ipuçları

- Koşulun yönüne bak: "hastaysa pozitif" mi, "pozitifse hasta" mı?
- Nadir olaylarda önsel sonucu belirler.
- Doğal sıklıklar (kişi sayısı) sezgiyi korur.
- Kanıtların bağımsız olup olmadığını sor.
