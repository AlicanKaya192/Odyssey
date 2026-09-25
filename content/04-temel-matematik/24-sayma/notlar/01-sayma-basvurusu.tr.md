Dersteki her şeyin kısa hâli. Bir soruda takıldığında buraya dön.

## İki ilke

| İlke | Ne zaman | İşlem |
|---|---|---|
| toplama | ayrı gruplardan **biri** ("ya o ya bu") | topla |
| çarpma | **adım adım** seçim ("önce o, sonra bu") | çarp |

## Formüller

| Ad | Formül | Anlamı |
|---|---|---|
| faktöriyel | $n! = n(n - 1) \cdots 1$, $0! = 1$ | $n$ nesnenin dizilişleri |
| permütasyon | $P(n, k) = \dfrac{n!}{(n - k)!}$ | $k$ tanesini sıralı seçmek |
| kombinasyon | $\binom{n}{k} = \dfrac{n!}{k!(n - k)!}$ | $k$ tanesini sırasız seçmek |
| tekrarlı sıralı | $n^k$ | PIN, şifre |
| tekrarlı sırasız | $\binom{n + k - 1}{k}$ | aynı çeşitten birden çok |
| aynı nesneli diziliş | $\dfrac{n!}{a! \, b! \cdots}$ | "KAYAK": $\frac{5!}{2!2!}$ |

$P(n, k) = \binom{n}{k} \cdot k!$

## Kombinasyon özellikleri

- $\binom{n}{0} = \binom{n}{n} = 1$, $\binom{n}{1} = n$
- $\binom{n}{k} = \binom{n}{n - k}$
- Pascal: $\binom{n}{k} = \binom{n - 1}{k - 1} + \binom{n - 1}{k}$
- $\binom{n}{0} + \binom{n}{1} + \dots + \binom{n}{n} = 2^n$
- $\binom{n}{2} = \frac{n(n - 1)}{2}$: çift sayısı

## Hangi formül?

1. Sıra önemli mi? Seçilenlerin yerini değiştir; sonuç değişiyorsa evet.
2. Tekrar var mı? Aynı nesne iki kez seçilebiliyor mu?
3. Aynı nesneler var mı? Varsa kendi aralarındaki dizilişlere böl.

## Olasılık

Eşit olasılıklı sonuçlarda $P = \dfrac{\text{uyan sonuç}}{\text{bütün sonuç}}$.

## Pratik ipuçları

- "En az bir" için tümleyen: hepsinden "hiç yok"u çıkar.
- Koşullu gruplarda (2 erkek, 2 kadın) her grubu ayrı seç, sonra çarp.
- Emin değilsen küçük bir örneği elle say ve formülle karşılaştır.
