**Fikir:** Önce dört turda işlenen toplam örnek sayısını, sonra her turun yığın yapısını düşünelim. Bu yol, adım sayısının neden örnek sayısından doğrudan bölünerek bulunamayacağını gösteriyor.

**Adım 1 — Bir turun yapısı.** $64 \cdot 390 = 24\,960$ örnek tam yığınlarda, kalan $25\,000 - 24\,960 = 40$ örnek son yığında. $40 < 64$ olduğu için $390$ tam yığın doğru.

**Adım 2 — Neden $100\,000 \div 64$ değil?** Dört turda toplam $4 \cdot 25\,000 = 100\,000$ örnek işleniyor. $100\,000 = 64 \cdot 1\,562 + 32$; bu hesap $1\,563$ adım verirdi. Ama her tur **kendi** son eksik yığınıyla bitiyor: turlar arasında yığınlar birleşmiyor.

**Adım 3 — Doğru sayım.** Her tur $391$ adım (390 tam + 1 eksik):

$$
4 \cdot 391 = 1\,564
$$

**Sonucu yorumla:** İki sayım arasındaki fark tam olarak şu: her tur sonunda kısa bir yığın var. Kütüphanelerde bu son yığını atmak için bir seçenek bile bulunur ("drop last"); atılırsa bir tur $390$ adım olur.

**Cevap:** $390$, $40$ ve $1\,564$.
