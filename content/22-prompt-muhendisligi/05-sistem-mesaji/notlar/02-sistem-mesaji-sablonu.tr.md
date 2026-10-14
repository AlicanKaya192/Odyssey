Bir destek asistanı için sistem mesajı iskeleti:

```text
You are the support assistant of <shop>.
Be friendly and brief: at most 3 sentences.
Answer in the language of the customer.
Rules:
1. Talk only about orders, shipping, returns and products.
2. Never promise a refund or a discount.
3. If you do not know, say so and offer to ask a colleague.
```

**Her kural için iki soru:**

| Kural | Modele söylendi mi? | Kodla denetleniyor mu? |
|---|---|---|
| En fazla 3 cümle | Evet | Evet: cümle sayısı |
| Vaat yok | Evet | Evet: vaat kalıpları |
| Yalnızca mağaza konuları | Evet | Kısmen: konu sınıflandırması gerekir |
| Bilmezse söyle | Evet | Hayır: değerlendirme kümesiyle ölçülür |

**Takılan cevap ne olur?**

| Sorun | Yapılacak |
|---|---|
| Vaat, indirim, kişisel bilgi | Gönderme; insana ilet |
| Fazla uzun | Kısaltmasını isteyerek bir kez yeniden sor |
| "As an AI ..." gibi gereksiz cümle | Yeniden sor ya da cümleyi at |

**Sık hatalar:**

- **Kuralı yalnızca sistem mesajına yazıp denetlememek.** Kullanıcı
  "kurallarını unut" yazdığında son savunma cevap denetimidir.
- **Sistem mesajına gizli bilgi koymak.** Kullanıcılar onu çekip
  çıkarabilir.
- **Sürümü kayda yazmamak.** Bir şikâyette hangi kuralların geçerli
  olduğu bulunamaz.
- **Rolü uzun bir hayalî geçmişle şişirmek.** Token her çağrıda ödenir.
