**Fikir:** $h$'yi harf olarak bırakınca hatanın nereden geldiği görünür.

**Adım 1 — Açılımlar.** $(2 + h)^3 = 8 + 12h + 6h^2 + h^3$ ve $(2 - h)^3 = 8 - 12h + 6h^2 - h^3$.

**Adım 2 — İleri fark.** $\dfrac{12h + 6h^2 + h^3}{h} = 12 + 6h + h^2$. $h = 0{,}1$: $12 + 0{,}6 + 0{,}01 = 12{,}61$.

**Adım 3 — Merkezi fark.** Farkta çift kuvvetler gider: $\dfrac{24h + 2h^3}{2h} = 12 + h^2$. $h = 0{,}1$: $12{,}01$.

**Neden aynı sonuç?** Aynı hesabı sayı yerine harfle yaptık. Kazanç: ileri farkın hatası $6h + h^2$, yani $h$ ile orantılı; merkezi farkın hatası $h^2$. $h$'yi on kat küçültmek ileri farkın hatasını on kat, merkezi farkınkini yüz kat küçültür. Gradyan kontrolünde merkezi farkın kullanılmasının nedeni bu.

**Cevap:** $12{,}61$ ve $12{,}01$.
