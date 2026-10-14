Örnekleri prompt'a koymanın iki yaygın biçimi var.

**1. Mesaj çiftleri.** Her örnek bir `user` mesajı ve onun `assistant`
cevabı; yeni girdi en sonda:

```text
system:    Put the message into one category: shipping, returns, ...
user:      My parcel should have arrived on Monday.
assistant: shipping
user:      Can I return boots I only tried on at home?
assistant: returns
user:      <yeni mesaj>
```

**2. Tek metin.** Örnekler aynı talimat metninin içinde, sabit bir
kalıpla:

```text
Put the message into one category: shipping, returns, ...

Message: My parcel should have arrived on Monday.
Category: shipping

Message: Can I return boots I only tried on at home?
Category: returns

Message: <yeni mesaj>
Category:
```

| | Mesaj çiftleri | Tek metin |
|---|---|---|
| Biçimi gösterme | Cevap mesajın tamamı | Cevap `Category:` satırından sonra |
| Ayrıştırma | Cevap doğrudan etiket | Fazladan satırlar gelirse ilk satırı al |
| Ne zaman? | Sohbet modelleri | Tek metin bekleyen modeller ya da şablonlar |

**Seçim sırası:**

1. Havuzu ve test kümesini ayır; test mesajı örnek olmasın.
2. Her kategoriden en az bir örnek al (dengeli), karışık sırayla ver.
3. Zor örnekleri (iki kategori arasındakiler) tercih et.
4. Örnek sayısını artırmadan önce token bedelini ölç; artışın değip
   değmediğini değerlendirme kümesiyle ölç.

**Sık hatalar:**

- **Örnekleri kategoriye göre sıralı vermek.** Son örneğin kategorisi hep
  aynı olur.
- **Örnek cevaplarda farklı biçim.** Biri "shipping", öteki
  "Shipping." ise model ikisini de üretebilir.
- **Test mesajını örnek yapmak.** Ölçülen başarı ezber olur.
