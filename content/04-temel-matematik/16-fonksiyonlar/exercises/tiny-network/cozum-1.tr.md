**Ne soruluyor?** İki fonksiyonun bileşkesi olan küçük bir ağın çıktısı.

**Fikir:** Ağ bir bileşke: $y = g(\text{ReLU}(f(x)))$, burada $f(x) = 2x - 3$ ve $g(h) = 3h + 1$. İçten dışa hesaplarız; ReLU yalnızca negatifleri sıfırlar.

**Adım 1 — $x = 4$, iç katman.** $2 \cdot 4 - 3 = 5$; $\text{ReLU}(5) = 5$, yani $h = 5$.

**Adım 2 — Dış katman.** $y = 3 \cdot 5 + 1 = 16$.

**Adım 3 — $x = 1$, iç katman.** $2 \cdot 1 - 3 = -1$; $\text{ReLU}(-1) = 0$, yani $h = 0$.

**Adım 4 — Dış katman.** $y = 3 \cdot 0 + 1 = 1$.

**Sonucu yorumla:** $2x - 3 < 0$, yani $x < 1{,}5$ olan her girdi için ağ aynı çıktıyı ($1$) veriyor: ReLU o bölgeyi "kapatıyor". $x \ge 1{,}5$'te ise $y = 3(2x - 3) + 1 = 6x - 8$, bir doğru. Ağın grafiği $x = 1{,}5$'te kırılan bir çizgi.

**Dikkat:** ReLU'yu atlayıp $y = 3(2 \cdot 1 - 3) + 1 = -2$ bulmak, iç katmanın negatif çıktısını sıfırlamayı unutmak demek.

**Cevap:** $16$ ve $1$.
