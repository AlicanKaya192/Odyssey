Dersteki her şeyin kısa hâli. Bir soruda takıldığında buraya dön.

## Kavramlar

| Kavram | Anlamı | Zar örneği |
|---|---|---|
| örnek uzay $S$ | bütün sonuçlar | $\{1, \dots, 6\}$ |
| olay | $S$'nin alt kümesi | çift: $\{2, 4, 6\}$ |
| tümleyen $A'$ | $A$ değil | tek: $\{1, 3, 5\}$ |
| ayrık | birlikte olamaz, $A \cap B = \varnothing$ | "1" ve "6" |
| bağımsız | biri ötekini etkilemez | iki ayrı zar |

## Kurallar

| Kural | Formül |
|---|---|
| eşit olasılıklı sonuçlar | $P(A) = \dfrac{s(A)}{s(S)}$ |
| sınırlar | $0 \leq P(A) \leq 1$, $P(S) = 1$ |
| tümleyen | $P(A') = 1 - P(A)$ |
| birleşim | $P(A \cup B) = P(A) + P(B) - P(A \cap B)$ |
| ayrık birleşim | $P(A \cup B) = P(A) + P(B)$ |
| bağımsız kesişim | $P(A \cap B) = P(A) \, P(B)$ |
| koşullu | $P(B \mid A) = \dfrac{P(A \cap B)}{P(A)}$ |

## Ağaç

- Dala o adımın olasılığı yazılır; ikinci dallar koşullu olasılık.
- Yol boyunca **çarp**, olaya uyan yolları **topla**.
- Bütün yolların toplamı $1$.
- İadesiz çekişte ikinci adımın olasılıkları değişir; iadeli çekişte
  değişmez.

## Pratik ipuçları

- "En az bir" gördüğünde tümleyene bak: $1 - P(\text{hiç})$.
- "Ya da" için birleşim, "ve" için kesişim.
- Çarpmadan önce bağımsızlığı sor.
- $P(B \mid A)$ ile $P(A \mid B)$ farklı: payda hangi grubu sayıyor?
- Sonuçların gerçekten eşit olasılıklı olduğundan emin ol.
