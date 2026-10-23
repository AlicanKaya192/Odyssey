Kullanıcıdan adını al ve `fpdf2` ile bir tişört sertifikası, `shirtificate.pdf` oluştur (Odyssey'de kurulu, `from fpdf import FPDF`). Şartlar:

- Sayfa **dikey A4** (210 × 297 mm), tek sayfa.
- Sayfanın üstünde, yatayda ortalı `CS50 Shirtificate` yazısı.
- Klasördeki `shirtificate.png` tişört resmi yatayda ortada (`pdf.image`).
- Tişörtün üstünde **beyaz** yazıyla `Ad took CS50` (`Harry took CS50`).

Çerçeve, renk ve çizgiler serbest; uzun adların satıra sığması gerekmiyor. Odyssey PDF'in sayfasını, metinlerini, yazı rengini ve resmin ortada olup olmadığını denetliyor; görünüşü birebir karşılaştırmıyor.

## Nasıl denenir

- Girdi `Harry` → yazılan dosya `shirtificate.pdf`
- Girdi `Ada Lovelace` → yazılan dosya `shirtificate.pdf`
