**Ne soruluyor?** Naive Bayes ile iki farklı e-postanın spam olasılığı.

**Fikir:** Her sınıf için önsel ile özelliklerin koşullu olasılıklarını çarp (koşullu bağımsızlık); puanları toplama bölüp olasılığa çevir.

**Adım 1 — İki kelime, spam puanı.** $0{,}4 \cdot 0{,}5 \cdot 0{,}2 = 0{,}04$.

**Adım 2 — Olasılık.** Spam değil puanı $0{,}6 \cdot 0{,}1 \cdot 0{,}25 = 0{,}015$.

$$
\frac{0{,}04}{0{,}04 + 0{,}015} = \frac{0{,}04}{0{,}055} = \frac{8}{11} \approx 0{,}727
$$

**Adım 3 — Yalnız ikinci kelime.** Spam: $0{,}4 \cdot 0{,}5 \cdot 0{,}2 = 0{,}04$ (birincinin yokluğu $1 - 0{,}5$). Spam değil: $0{,}6 \cdot 0{,}9 \cdot 0{,}25 = 0{,}135$. Olasılık $\frac{0{,}04}{0{,}175} = \frac{8}{35} \approx 0{,}229$.

**Sağlama:** İkinci kelime tek başına spamlerde daha **az** geçiyor ($0{,}2 < 0{,}25$); birinci kelimenin yokluğu da spam aleyhine. Olasılığın önselin ($0{,}4$) altına düşmesi mantıklı ✓.

**Dikkat:** Kelimenin geçmemesini "bilgi yok" sayıp çarpmamak; Naive Bayes'in bu biçiminde yokluk da kanıt.

**Cevap:** $0{,}04$; $\frac{8}{11}$; $\frac{8}{35}$.
