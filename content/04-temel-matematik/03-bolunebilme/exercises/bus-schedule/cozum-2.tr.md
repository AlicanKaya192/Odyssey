**Fikir:** Formül kullanmadan iki hattın kalkış dakikalarını yan yana yaz ve ortakları bul. Küçük sayılarda bu yol EKOK'un ne demek olduğunu açıkça gösteriyor.

**Adım 1 — İki liste.**

$$
\begin{aligned}
\text{A} &: 0, 12, 24, 36, 48, 60, 72, \dots \\
\text{B} &: 0, 18, 36, 54, 72, \dots
\end{aligned}
$$

**Adım 2 — İlk ortak.** $0$'dan sonra iki listede de bulunan ilk sayı $36$. Bu, EKOK'un tanımı: sıfırdan büyük en küçük ortak kat.

**Adım 3 — Örüntü.** Ortaklar $0, 36, 72, \dots$ diye $36$'şar artıyor: bir kez aynı anda kalktıklarında her şey baştan başlıyor.

**Adım 4 — Saatlere çevir.** $08{:}00$, $08{:}36$, $09{:}12$, $09{:}48$, $10{:}24$, $11{:}00$, $11{:}36$. Bir sonraki $12{:}12$, sınırın dışında. Toplam $7$ kalkış.

**Neden aynı sonuç?** Listeleri yazmak, EKOK'u "ortak katların en küçüğü" tanımıyla doğrudan bulmak demek. Asal çarpan yolu aynı sayıya kısa yoldan varıyor; sayılar büyüdükçe listeler uzar, çarpan yolu tercih edilir.

**Cevap:** $36$ ve $7$.
