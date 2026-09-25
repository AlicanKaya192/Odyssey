Dersteki yöntemlerin her biri için adım adım çözülmüş bir örnek. Önce soruyu kendin çözmeye çalış, sonra çözümü oku.

## 1. Bilgi

**Soru:** Olasılığı $\frac{1}{16}$ olan bir sonuç kaç bit bilgi taşır?

$-\log_2\frac{1}{16} = 4$ bit.

## 2. Zarın entropisi

**Soru:** Adil bir zarın entropisi?

Altı eşit olasılıklı sonuç: $\log_2 6 \approx 2{,}585$ bit.

## 3. Olasılığı sıfır olan sonuç

**Soru:** $P = (0{,}5; \ 0{,}5; \ 0)$. $H(P)$?

$0 \log 0 = 0$: $H = 1$ bit, iki sonuçlu adil para gibi.

## 4. Eşit olmayan dağılım

**Soru:** $P = (0{,}7; \ 0{,}2; \ 0{,}1)$. $H(P)$?

$0{,}7 \cdot 0{,}515 + 0{,}2 \cdot 2{,}322 + 0{,}1 \cdot 3{,}322 \approx 0{,}360
+ 0{,}464 + 0{,}332 = 1{,}157$ bit. Üç sonuçta en fazla $1{,}585$ olabilirdi.

## 5. Bitten nata

**Soru:** $2$ bit kaç nattır?

$2 \cdot \ln 2 \approx 1{,}386$ nat.

## 6. Çapraz entropi

**Soru:** $P = (0{,}5; \ 0{,}5)$, $Q = (0{,}8; \ 0{,}2)$. $H(P, Q)$?

$-0{,}5\log_2 0{,}8 - 0{,}5\log_2 0{,}2 \approx 0{,}161 + 1{,}161 = 1{,}322$
bit.

## 7. KL ıraksaması

**Soru:** Aynı dağılımlarla $D_{\mathrm{KL}}(P \parallel Q)$?

$H(P, Q) - H(P) = 1{,}322 - 1 = 0{,}322$ bit.

## 8. Sınıflandırma kaybı

**Soru:** Dört sınıflı bir modelde doğru sınıfın olasılığı $0{,}25$.
Çapraz entropi (nat)?

$-\ln 0{,}25 \approx 1{,}386$ nat: model tahminden öteye geçmemiş, düzgün
dağılım kadar kararsız.

## 9. Bilgi kazancı

**Soru:** $4$ pozitif $4$ negatif örnek. Bölme A: $(4, 0)$ ve $(0, 4)$.
Bölme B: $(2, 2)$ ve $(2, 2)$. Kazançlar?

Ebeveyn $H = 1$. A: çocuklar saf, entropileri $0$; kazanç $1$ bit. B:
çocuklar ebeveyn kadar karışık; kazanç $0$.

## 10. Şaşkınlık

**Soru:** Bir dil modelinin kelime başına çapraz entropisi $3$ bit.
Şaşkınlığı?

$2^3 = 8$: model her kelimede sanki $8$ eşit seçenek arasında kararsız.
