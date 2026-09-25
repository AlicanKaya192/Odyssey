Dersteki yöntemlerin her biri için adım adım çözülmüş bir örnek. Önce soruyu kendin çözmeye çalış, sonra çözümü oku.

## 1. Parametre mi, istatistik mi?

**Soru:** Bir ankette $500$ kişinin yüzde $42$'si "evet" dedi. Ülke
genelindeki "evet" oranı nedir, $0{,}42$ nedir?

Ülke genelindeki oran $p$ bilinmeyen parametre; $\hat{p} = 0{,}42$ onu
tahmin eden istatistik.

## 2. Standart hata

**Soru:** $\sigma = 20$, $n = 100$. Örneklem ortalamasının standart hatası?

$\frac{20}{10} = 2$.

## 3. Gereken örneklem

**Soru:** $\sigma = 15$ ise standart hatanın en fazla $1{,}5$ olması için
kaç gözlem gerekir?

$\frac{15}{\sqrt{n}} \leq 1{,}5$, $\sqrt{n} \geq 10$, $n \geq 100$.

## 4. Ortalamanın olasılığı

**Soru:** $\mu = 50$, $\sigma = 10$, $n = 25$. $P(\bar{X} < 47)$?

$\text{SE} = 2$, $z = -1{,}5$: $1 - 0{,}933 = 0{,}067$.

## 5. Ortalamanın aralığı

**Soru:** Aynı durumda $P(48 \leq \bar{X} \leq 52)$?

$z = \pm 1$: yaklaşık $0{,}682$.

## 6. Toplamın dağılımı

**Soru:** Paket ağırlıkları $\mu = 500$ g, $\sigma = 20$ g. $40$ paketlik bir
kolinin toplam ağırlığının ortalaması ve standart sapması?

Ortalama $40 \cdot 500 = 20\,000$ g. Standart sapma $20\sqrt{40} \approx
126{,}5$ g. Toplamın yayılımı büyür, ama ortalamaya göre görece küçülür.

## 7. Oranın standart hatası

**Soru:** Gerçek oran $0{,}3$, $n = 100$. $\hat{p}$'nin standart hatası?

$\sqrt{\frac{0{,}3 \cdot 0{,}7}{100}} = \sqrt{0{,}0021} \approx 0{,}046$.

## 8. Test doğruluğunun belirsizliği

**Soru:** Bir model $500$ test örneğinde yüzde $85$ doğruluk aldı. Standart
hata?

$\sqrt{\frac{0{,}85 \cdot 0{,}15}{500}} \approx 0{,}016$, yani yaklaşık
$\pm 1{,}6$ puan.

## 9. Yanlı örneklem

**Soru:** Bir uygulamanın memnuniyet anketi yalnızca uygulamayı hâlâ
kullananlara gönderildi; $10\,000$ cevap geldi. Sonuç bütün kullanıcıları
temsil eder mi?

Hayır: bırakıp gidenler örneklemde yok. $10\,000$ cevap yanlılığı
düzeltmez, yalnızca yanlı tahmini daha kesin gösterir.

## 10. Bootstrap

**Soru:** Örneklem $\{2, 4, 9\}$. Bir bootstrap yeniden örneklemi nasıl
çekilir?

Üç kez, iadeli olarak rastgele çek: örneğin $\{4, 4, 9\}$, ortalaması
$\approx 5{,}67$. Bunu yüzlerce kez tekrarlayınca ortalamaların dağılımı,
örneklem dağılımının tahmini olur.
