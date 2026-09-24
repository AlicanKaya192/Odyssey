Dersteki her şeyin kısa hâli. Bir soruda takıldığında buraya dön.

## Küme gösterimleri

| Gösterim | Anlamı |
|---|---|
| $x \in A$ / $x \notin A$ | eleman / eleman değil |
| $\emptyset$ | boş küme |
| $s(A)$ | eleman sayısı |
| $A \subseteq B$ | alt küme |
| $A \cup B$ | birleşim (veya) |
| $A \cap B$ | kesişim (ve) |
| $A \setminus B$ | fark |
| $A'$ | tümleyen |

## Sayma kuralları

$$
s(A \cup B) = s(A) + s(B) - s(A \cap B)
$$

$$
s(A') = s(U) - s(A), \qquad s(A \setminus B) = s(A) - s(A \cap B)
$$

$n$ elemanlı bir kümenin $2^n$ alt kümesi var ($\emptyset$ ve kendisi dahil).

## Doğruluk tablosu

| $p$ | $q$ | $p \wedge q$ | $p \vee q$ | $p \Rightarrow q$ |
|---|---|---|---|---|
| $1$ | $1$ | $1$ | $1$ | $1$ |
| $1$ | $0$ | $0$ | $1$ | $0$ |
| $0$ | $1$ | $0$ | $1$ | $1$ |
| $0$ | $0$ | $0$ | $0$ | $1$ |

## De Morgan

| Mantık | Küme |
|---|---|
| $\neg(p \wedge q) = \neg p \vee \neg q$ | $(A \cap B)' = A' \cup B'$ |
| $\neg(p \vee q) = \neg p \wedge \neg q$ | $(A \cup B)' = A' \cap B'$ |

## Pratik ipuçları

- Venn şemasını **içten dışa** doldur: önce kesişim, sonra "yalnız" bölgeler, en son hiçbiri.
- "En az biri" birleşim, "ikisi de" kesişim, "hiçbiri" birleşimin tümleyeni.
- $p \Rightarrow q$'nun eşdeğeri $\neg q \Rightarrow \neg p$ (karşıt ters); tersi ($q \Rightarrow p$) eşdeğer değil.
- pandas'ta `&`, `|`, `~` kullan; her koşulu paranteze al.
