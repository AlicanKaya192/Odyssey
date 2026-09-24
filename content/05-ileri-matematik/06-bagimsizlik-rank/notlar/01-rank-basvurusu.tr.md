Dersteki her şeyin kısa hâli. Bir soruda takıldığında buraya dön.

## Kavramlar

| Kavram | Anlamı |
|---|---|
| Doğrusal kombinasyon | $c_1\mathbf{v}_1 + \cdots + c_k\mathbf{v}_k$ |
| Germe (span) | Bütün doğrusal kombinasyonların kümesi |
| Bağımlı | Biri ötekilerin kombinasyonu; $\sum c_i \mathbf{v}_i = \mathbf{0}$'ın sıfır olmayan çözümü var |
| Bağımsız | $\sum c_i \mathbf{v}_i = \mathbf{0}$'ın tek çözümü $\mathbf{c} = \mathbf{0}$ |
| Taban | Uzayı geren bağımsız grup |
| Boyut | Bir tabandaki vektör sayısı |
| Koordinat | Bir tabana göre katsayılar (tek türlü) |
| Sütun uzayı | $A$'nın sütunlarının germesi = $A\mathbf{x}$'in bütün değerleri |
| Çekirdek | $A\mathbf{x} = \mathbf{0}$'ın çözümleri |
| Rank | Bağımsız sütun sayısı = pivot sayısı = bağımsız satır sayısı |

## Bağımsızlık sınamaları

| Durum | Sınama |
|---|---|
| İki vektör | Biri ötekinin katı mı? Katıysa bağımlı |
| $n$ boyutta $n$ vektör | $\det \ne 0$ ise bağımsız |
| Genel | Sütun yap, ele; her sütunda pivot varsa bağımsız |
| $n$ boyutta $n$'den fazla vektör | her zaman bağımlı |
| Sıfır vektörü içeren grup | her zaman bağımlı |

## Rank

- $\operatorname{rank} A \le \min(m, n)$; eşitse **tam ranklı**.
- $\operatorname{rank} A = \operatorname{rank} A^\mathsf{T}$.
- Satır işlemleri rankı değiştirmez.

**Rank–sıfırlık:** $\operatorname{rank} A + \dim(\text{çekirdek}) = n$ (sütun sayısı).

## Sistemler ve rank

| Durum | Koşul |
|---|---|
| Çözüm var | $\operatorname{rank} A = \operatorname{rank}\,[A \mid \mathbf{b}]$ |
| Tek çözüm | ayrıca $\operatorname{rank} A = n$ |
| Sonsuz çözüm | ayrıca $\operatorname{rank} A < n$; çözümler = bir çözüm + çekirdek |

## Tersinir matris teoremi (n × n)

Hepsi denk: $A$ tersinir $\iff$ $\det A \ne 0$ $\iff$ $\operatorname{rank} A = n$ $\iff$ sütunlar bağımsız $\iff$ çekirdek $= \{\mathbf{0}\}$ $\iff$ her $\mathbf{b}$ için tek çözüm.

## Başka tabanda koordinat

Taban vektörleri $B$'nin sütunları ise $\mathbf{x}$'in koordinatları $\mathbf{c}$:

$$
B\mathbf{c} = \mathbf{x} \quad \Rightarrow \quad \mathbf{c} = B^{-1}\mathbf{x}
$$

## Pratik ipuçları

- Bağımlılık gözle görünmeyebilir; üç vektörün ikişer ikişer paralel olmaması yetmez.
- Rank için elemeyi yap ve pivotları say.
- Çekirdeği bulmak: basamak biçiminde serbest değişkenlere $s, t, \dots$ ver, her birinin katsayı vektörü çekirdeğin bir taban vektörü.
- Sütunlar yerine satırlarla çalışmak da aynı rankı verir; hangisi kolaysa.
