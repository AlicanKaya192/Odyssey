Veri eğitime girmeden önce iki tür denetimden geçer:

| Denetim | Neye bakar | Yakaladığı | Örnek |
|---|---|---|---|
| Eksik değer | Tek değer | Boş ya da hiç olmayan sütun | `usage_hours: missing` |
| İzin verilen değerler | Tek değer | Yazım farkı, yeni kategori | `plan: 'PRO' is not allowed` |
| Tür | Tek değer | Sayı yerine metin | `monthly_fee: '29.90' is not a number` |
| Aralık | Tek değer | Birim değişimi, imkânsız değer | `tenure: -3 is out of range` |
| Profil karşılaştırması | Sütunun bütünü | Her değer geçerli ama dağılım yanlış | `support_calls 0.68 CHECK` |

## Denetim sırası

`check_row` her sütunda dört soruyu bu sırayla sorar ve ilk düşen
soruda durur:

1. Değer var mı? (`None` ya da sütun yok)
2. İzin verilen değerlerden biri mi? (`allowed` kuralı olan sütunda)
3. Sayı mı? (`isinstance(value, (int, float))`)
4. Aralıkta mı? (`min <= value <= max`)

Sıra önemli: boş bir değeri aralıkla karşılaştırmaya çalışmak hata
verir, metni sayıyla karşılaştırmak da.

## Karantina mı, ret mi?

| Durum | Karar | Neden |
|---|---|---|
| Birkaç bozuk satır | Karantina | Arada bir yanlış girilmiş satırlar; sağlam satırlarla devam |
| Bozuk satırların payı sınırı geçti | Ret | Sistemli bir bozulma; kuralların görmediği hatalar da olabilir |
| Kurallar temiz, profil "CHECK" | Bir insan bakar | Müşteriler gerçekten değişmiş de olabilir |

Ret, hata fırlatmak (`raise`) demektir: eğitim betiği hata koduyla
biter ve hat kırmızıya döner.

## Profil

- Eğitim verisinden her sayısal sütunun **ortalaması** ve **standart
  sapması** çıkarılır.
- Kayma = `|yeni ortalama - eski ortalama| / eski standart sapma`.
  Standart sapma cinsinden yazınca bütün sütunlar aynı ölçekte.
- Sınır (bu bölümde 0,5) bir uyarı eşiğidir; kesin hüküm değil.

## Terimler

- **Veri doğrulama** (data validation): veriyi eğitimden ya da
  tahminden önce kurallara göre denetlemek.
- **Şema** (schema), **veri sözleşmesi** (data contract): her sütunun
  kuralları; veriyi gönderenle alan arasındaki anlaşma.
- **Parti** (batch): bir kerede gelen veri, örneğin bir ayın müşterileri.
- **Karantina** (quarantine): bozuk satırları ayırıp incelemek için
  saklamak.
- **Kapı** (gate): geçilmezse hattı durduran adım.
- **Profil** (profile): bir sütunun özet istatistikleri.
