Dersteki yöntemlerin her biri için adım adım çözülmüş bir örnek. Önce soruyu kendin çözmeye çalış, sonra çözümü oku.

## 1. Koşulun iki yönü

**Soru:** $40$ kişilik sınıfta $25$ kız var; kızların $10$'u, erkeklerin
$6$'sı gözlüklü. $P(\text{gözlüklü} \mid \text{kız})$ ve
$P(\text{kız} \mid \text{gözlüklü})$ nedir?

$\frac{10}{25} = 0{,}4$. Gözlüklüler $16$ kişi, $10$'u kız:
$\frac{10}{16} = 0{,}625$. Paydalar farklı gruplar.

## 2. Çarpım kuralı

**Soru:** $2$ bozuk, $8$ sağlam ampulden geri koymadan iki tane alınıyor.
İlkinin bozuk, ikincinin sağlam olma olasılığı?

$\frac{2}{10} \cdot \frac{8}{9} = \frac{16}{90} = \frac{8}{45}$. İkinci
çarpan koşullu: ilki bozuk çıktıktan sonra $9$ ampulün $8$'i sağlam.

## 3. Toplam olasılık

**Soru:** Günlerin yüzde $30$'u yağmurlu. Yağmurlu günde otobüs yüzde $40$,
kuru günde yüzde $10$ olasılıkla gecikiyor. Rastgele bir gün gecikme
olasılığı?

$0{,}3 \cdot 0{,}4 + 0{,}7 \cdot 0{,}1 = 0{,}12 + 0{,}07 = 0{,}19$.

## 4. Bayes

**Soru:** Aynı soruda otobüs gecikti. O günün yağmurlu olma olasılığı?

$\frac{0{,}12}{0{,}19} \approx 0{,}632$. Gecikme, yağmura inancı
$0{,}3$'ten $0{,}63$'e çıkardı.

## 5. Test sorusu

**Soru:** Hastalık yüzde $2$; duyarlılık yüzde $90$; yanlış pozitif oranı
yüzde $10$. Pozitif bir sonuçtan sonra hasta olma olasılığı?

$P(+) = 0{,}9 \cdot 0{,}02 + 0{,}1 \cdot 0{,}98 = 0{,}018 + 0{,}098 = 0{,}116$.
$P(H \mid +) = \frac{0{,}018}{0{,}116} \approx 0{,}155$.

## 6. Doğal sıklıklarla

**Soru:** Aynı soruyu $1000$ kişiyle düşün.

$20$ hasta, $18$'i pozitif. $980$ sağlıklı, $98$'i pozitif. Pozitiflerin
$\frac{18}{116} \approx 0{,}155$'i hasta.

## 7. İkinci test

**Soru:** Aynı kişi bağımsız ikinci testte de pozitif. Şimdi?

Önsel $0{,}155$: $\frac{0{,}9 \cdot 0{,}155}{0{,}9 \cdot 0{,}155 + 0{,}1 \cdot
0{,}845} \approx 0{,}623$.

## 8. Oran biçimi

**Soru:** Beşinci örneği oranlarla çöz.

Önsel oran $2 : 98 = 1 : 49$. Olabilirlik oranı $\frac{0{,}9}{0{,}1} = 9$.
Sonsal oran $9 : 49$; olasılık $\frac{9}{58} \approx 0{,}155$.

## 9. İki kutu

**Soru:** Birinci kutuda $3$ kırmızı $2$ mavi, ikincide $1$ kırmızı $4$
mavi top var. Rastgele bir kutu seçilip bir top çekiliyor; top kırmızı.
Birinci kutudan gelmiş olma olasılığı?

$\frac{0{,}5 \cdot 0{,}6}{0{,}5 \cdot 0{,}6 + 0{,}5 \cdot 0{,}2} = \frac{0{,}3}{0{,}4}
= 0{,}75$.

## 10. Naive Bayes

**Soru:** $P(A) = 0{,}6$, $P(B) = 0{,}4$ iki sınıf. Bir örneğin iki
özelliği için $P(x_1 \mid A) = 0{,}2$, $P(x_2 \mid A) = 0{,}5$,
$P(x_1 \mid B) = 0{,}6$, $P(x_2 \mid B) = 0{,}3$. Hangi sınıf seçilir?

$A$: $0{,}6 \cdot 0{,}2 \cdot 0{,}5 = 0{,}06$. $B$: $0{,}4 \cdot 0{,}6 \cdot
0{,}3 = 0{,}072$. $B$ seçilir; $P(B \mid x) = \frac{0{,}072}{0{,}132} \approx
0{,}545$.
