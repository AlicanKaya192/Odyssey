**Ne soruluyor?** Momentumlu ve momentumsuz gradyan inişinin ilk üç adımı.

**Fikir:** Momentumda önce hız $v$ güncellenir (eski hızın $0{,}9$'u artı yeni gradyan), sonra $w$ hız kadar ilerler.

**Adım 1 — Momentum.**

| $k$ | $w_k$ | $L'(w_k)$ | $v_{k+1}$ | $w_{k+1}$ |
|---|---|---|---|---|
| $0$ | $1$ | $2$ | $2$ | $0{,}8$ |
| $1$ | $0{,}8$ | $1{,}6$ | $3{,}4$ | $0{,}46$ |
| $2$ | $0{,}46$ | $0{,}92$ | $3{,}98$ | $0{,}062$ |

**Adım 2 — Momentumsuz.** $w \leftarrow w - 0{,}2w = 0{,}8w$: $0{,}8$, $0{,}64$, $0{,}512$.

**Sağlama:** Üç adımda momentum $0{,}062$'ye, düz iniş $0{,}512$'ye geldi: birikmiş hız inişi çok hızlandırdı ✓.

**Dikkat:** Momentum aynı zamanda aşmaya da yatkın: birkaç adım daha atılırsa $w$ sıfırın öbür yanına geçer ve salınarak döner. $\beta$ büyüdükçe bu salınım uzar.

**Cevap:** $0{,}46$, $0{,}062$ ve $0{,}512$.
