Dersteki yöntemlerin her biri için adım adım çözülmüş bir örnek. Önce soruyu kendin çözmeye çalış, sonra çözümü oku.

## 1. Ortalama için güven aralığı

**Soru:** $n = 49$, $\bar{x} = 120$, $\sigma = 14$. Yüzde $95$ güven
aralığı?

$\text{SE} = \frac{14}{7} = 2$; hata payı $1{,}96 \cdot 2 = 3{,}92$.
Aralık $[116{,}08; \ 123{,}92]$.

## 2. Farklı güven düzeyi

**Soru:** Aynı veriyle yüzde $99$ güven aralığı?

$2{,}576 \cdot 2 = 5{,}152$; aralık $[114{,}85; \ 125{,}15]$. Daha geniş.

## 3. Gereken örneklem

**Soru:** $\sigma = 12$; yüzde $95$ güvenle hata payı en fazla $2$ olsun.
Kaç gözlem?

$\left(\frac{1{,}96 \cdot 12}{2}\right)^2 = 11{,}76^2 = 138{,}3$; yukarı
yuvarla: $139$.

## 4. Oran için aralık

**Soru:** $400$ kişinin $120$'si "evet" dedi. Yüzde $95$ güven aralığı?

$\hat{p} = 0{,}3$; $\text{SE} = \sqrt{\frac{0{,}3 \cdot 0{,}7}{400}} \approx
0{,}0229$; hata payı $\approx 0{,}045$. Aralık yaklaşık
$[0{,}255; \ 0{,}345]$.

## 5. İki yönlü test

**Soru:** $H_0: \mu = 80$, $\sigma = 10$, $n = 25$, $\bar{x} = 83{,}5$.
$\alpha = 0{,}05$ ile karar?

$\text{SE} = 2$, $z = 1{,}75$. $P(Z \geq 1{,}75) \approx 0{,}040$; iki
yönlü p $\approx 0{,}080 > 0{,}05$: $H_0$ reddedilemez.

## 6. Tek yönlü test

**Soru:** Aynı veriyle, veriye bakmadan önce $H_1: \mu > 80$ seçilmiş
olsaydı?

Tek kuyruk: p $\approx 0{,}040 < 0{,}05$: reddedilir. Yön önceden
seçilmediyse bu hesap geçersizdir.

## 7. Aralık ile test

**Soru:** Yüzde $95$ güven aralığı $[4{,}1; \ 7{,}3]$. $H_0: \mu = 4$,
$\alpha = 0{,}05$ ile iki yönlü test ne der?

$4$ aralığın dışında: $H_0$ reddedilir.

## 8. İki oranın farkı

**Soru:** A grubunda $1000$ kişiden $150$'si, B grubunda $1000$ kişiden
$180$'i tıkladı. Farkın standart hatası ve $z$?

$\text{SE}_{\text{fark}} = \sqrt{\frac{0{,}15 \cdot 0{,}85}{1000} +
\frac{0{,}18 \cdot 0{,}82}{1000}} = \sqrt{0{,}0002751} \approx 0{,}0166$;
$z = \frac{0{,}03}{0{,}0166} \approx 1{,}81$. İki yönlü p $\approx 0{,}07$:
yüzde 5 düzeyinde anlamlı değil.

## 9. Çoklu karşılaştırma

**Soru:** $10$ bağımsız test, hepsinde $H_0$ doğru, $\alpha = 0{,}05$. En
az bir yanlış alarm olasılığı? Bonferroni eşiği?

$1 - 0{,}95^{10} \approx 0{,}40$. Eşik $\frac{0{,}05}{10} = 0{,}005$.

## 10. Hata türleri

**Soru:** Bir spam filtresinde $H_0$: "e-posta normal". Önemli bir iş
e-postasının spama düşmesi hangi tür hatadır?

$H_0$ doğruyken reddedilmiş: I. tür hata.
