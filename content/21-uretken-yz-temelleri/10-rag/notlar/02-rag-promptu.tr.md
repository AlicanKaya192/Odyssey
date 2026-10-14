Bir RAG prompt'unun parçaları:

```text
system: Answer only from the numbered sources. Cite the source number
        like [2]. If the sources do not contain the answer, reply:
        I could not find this in the sources.

user:   Sources:
        [1] Gift cards are available for 25, 50 and 100 euros and are
            valid for 3 years.
        [2] Purchases paid with a gift card are refunded as a new gift card.
        [3] Points expire if you make no purchase for 12 months.

        Question: Do gift cards expire?
```

**Neden böyle?**

- **Kurallar sistem mesajında:** her çağrıda aynı; kullanıcının sorusundan
  ayrı tutulur.
- **Kaynaklar numaralı:** model cevabın nereden geldiğini numarayla
  yazabilir, program da bunu denetleyebilir (08).
- **"Bulamadım" cümlesi birebir yazılı:** program cevabı bu cümleyle
  karşılaştırıp çekimser kalındığını anlayabilir.
- **Soru en sonda:** model kaynakları okuduktan sonra soruya gelir.

**Program tarafında:**

1. Aramadan önce soruyu temizle (gereksiz boşluk, çok uzun metin).
2. Bulunan parçaları token bütçesine göre sınırla (09).
3. Cevaptaki kaynak numaralarını ayıkla; var olmayan numara ya da kaynakta
   geçmeyen ayrıntı varsa cevabı işaretle.
4. "Bulamadım" cevabını arayüzde düzgün göster; kullanıcıyı insana ya da
   başka bir kanala yönlendir.

**Sık hatalar:**

- **Kaynakları numarasız yapıştırmak:** cevap denetlenemez.
- **"Bulamadım" cümlesini serbest bırakmak:** model her seferinde başka
  biçimde söyler, program çekimser kalındığını anlayamaz.
- **Çok fazla kaynak:** token artar, ilgisiz parçalar cevabı bulandırır.
- **Arama hatasını model hatası sanmak:** önce doğru parçanın prompt'a girip
  girmediğine bak.
