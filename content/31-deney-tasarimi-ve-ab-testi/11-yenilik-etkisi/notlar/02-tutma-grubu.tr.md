Test bitip değişiklik herkese açıldığında soru kapanmış sayılır. Ama kısa
testin göremediği şeyler vardır: yeniliğin sönmesi, mevsim, kullanıcıların
zamanla davranış değiştirmesi. **Tutma grubu** (holdout) bunlar için
kurulur.

## Nasıl kurulur?

- Değişiklik açılırken kullanıcıların küçük bir payı (ör. %1–5) eski hâlde
  bırakılır.
- Bu grup rastgele seçilir, tıpkı testteki gibi; Rastgele Atama
  bölümündeki tuzlu karma yöntemi burada da kullanılır.
- Aylar sonra tutma grubu ile geri kalan karşılaştırılır: kalıcı etki budur.

## Bedeli

- Tutma grubundaki kullanıcılar daha iyi olduğu düşünülen ürünü görmez.
  Pay küçük tutulur.
- Küçük grup gürültülüdür; sonucu okumak için yeterli süre gerekir.
- Birçok değişiklik üst üste açılıyorsa tutma grubu hepsinin **toplam**
  etkisini ölçer; tek tek etkiler ayrılamaz.

## Ne zaman gerekir?

- Etkinin aylar içinde değişmesi bekleniyorsa (alışkanlık, yenilik).
- Kararın parası büyükse ve kısa testin tahmini yatırımın temeliyse.
- Metrik geç tepki veriyorsa (ör. abonelik iptali, geri dönen kullanıcı).

## Unutmayın

Tutma grubu testin yerini almaz. Önce kısa test zararlı bir değişikliği
yakalar; tutma grubu yalnızca kalıcı etkinin büyüklüğünü düzeltir.
