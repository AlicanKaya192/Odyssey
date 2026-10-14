# Genel Tekrar

Prompt Mühendisliği ve LLM Uygulamaları modülünün sonuna geldin. Bir
prompt'un bir mesaj listesi olduğunu görmekle başladık; talimatı netleştirdik,
örnek verdik, adım adım düşündürdük, cevabı katı ayrıştırıp doğruladık.
Sonra uygulamaya geçtik: sistem mesajı, şablonlar, zincirler, araçlar,
ajan döngüsü ve bellek. En sonda ölçtük ve korunduk: değerlendirme,
injection savunması, hatalar ve maliyet, sistemli iyileştirme ve hepsini
birleştiren bir destek asistanı. Bu bölüm yolu bir kez daha yürüyor.

<figure class="fig">
  <div class="flow">
    <span class="node">Temeller<br><small>00–04</small></span><span class="arrow">→</span>
    <span class="node">Uygulama<br><small>05–07</small></span><span class="arrow">→</span>
    <span class="node">Araç ve ajan<br><small>08–10</small></span><span class="arrow">→</span>
    <span class="node">Ölç ve koru<br><small>11–13</small></span><span class="arrow">→</span>
    <span class="node acc">Sistem ve proje<br><small>14–15</small></span>
  </div>
  <figcaption>Modülün yolu: prompt'u kur, uygulamayı kur, araç ve bellek ekle, ölç ve koru, hepsini birleştir.</figcaption>
</figure>

## 1. Prompt'un temelleri (Bölüm 0–4)

- Prompt bir **mesaj listesidir**: sistem, kullanıcı, asistan. Kısa
  mesajlarda gönderilen token'ların %73–78'i sabit kısım; cevap **katı
  ayrıştırılır**, örnek yanıtların yarısı (6'da 3) kabul edildi (00).
- **Net talimat** ölçülebilir kurallardır; aynı kural sözlüğünden hem
  prompt hem denetleyici üretilir. Veri bir **ayraçla** ayrılır ve
  kaçırılır (01).
- **Az örnekli prompt:** örnek sayısı token'ı büyütür (0 örnek 56, 10
  örnek 287 token); örnekler kategorileri kapsayacak şekilde seçilir,
  rastgele 5 örnek bin çekilişin 932'sinde bir kategoriyi kaçırdı (02).
- **Adım adım düşündürmek** hesap hatasını görünür kılar ama doğrulamaz;
  hesabı kod yapar. Adımlı cevap 10 kat token (03).
- **Yapılı çıktı:** ayrıştır, şemayla doğrula, gerekirse bir kez onar
  (onarımda giren token 16'dan 114'e) (04).

## 2. Uygulamayı kurmak (Bölüm 5–7)

- **Sistem mesajı** ayarlardan kurulur, sürüm özetiyle izlenir; cevap
  kurallara göre denetlenir (05).
- **Şablonlar:** `str.format` JSON örneğinde bozulur, `safe_substitute`
  eksiği sessizce bırakır; değişkenler doğrulanır, uzun metin ortadan
  kesilir (06).
- **Zincirler:** her adım küçük ve denetlenebilir; tek prompt 412 token,
  zincir 215; düşen adım zinciri durdurur (07).

## 3. Araçlar, ajanlar ve bellek (Bölüm 8–10)

- **Araç çağırma:** model çağrıyı önerir, program doğrular ve çalıştırır;
  geri alınamaz işte onay; cevap aracın sonucuna dayandırılır (08).
- **Ajan döngüsü:** tur ve token sınırı şart; aynı çağrıyı tekrarlayan ajan
  5 turda 516 token harcayıp sonuç vermedi (09).
- **Bellek:** bütün geçmiş 1565 token; son 4 mesaj sipariş numarasını
  kaybetti; önemli bilgiler ayrı bir bellekte tutulur (10).

## 4. Ölçmek ve korumak (Bölüm 11–13)

- **Değerlendirme:** biçim ve doğruluk ayrı sayılır; `v2` 40 mesajda
  36 doğru, `v1` 31; farkın aralığı 0 ile 0,25 arası (11).
- **Prompt injection:** kesin çözüm yok; dedektör (kesinlik 0,8,
  duyarlılık 0,57), en az yetki, onay ve çıktı denetimi birlikte (12).
- **Hatalar ve maliyet:** geçici hata jitter'lı üstel beklemeyle denenir,
  kalıcı hata denenmez; kesilen cevap prompt'u yeniden ödetir; önbellek
  100 isteğin 55'ini modele göndermedi (13).

## 5. Sistemli çalışmak ve proje (Bölüm 14–15)

- **Sistemli iyileştirme:** geliştirme kümesinde karar ver, teste en
  sonda bak; ezberleyen `v3` geliştirmede 1,00, testte `v2` ile aynı
  (0,75) (14).
- **Destek asistanı:** girdi süzgeci → sınıflandır → sipariş verisi →
  cevap → çıktı denetimi; on senaryoda 9/10, tek değişiklikle 10/10 (15).

## Hepsi birlikte: token nereye gidiyor?

Bitirme projesindeki asistan her mesajda iki çağrı yapıyor. 40 destek
mesajının hepsini asistandan geçirseydik token'ların ne kadarı sabit
sistem mesajlarına, ne kadarı müşterinin yazdığına giderdi?

```python
from llm_client import count_message_tokens
from shop_data import LABELS, TICKETS

CLASSIFY = "Answer with one word: " + ", ".join(LABELS) + "."
SYSTEM = ("You are the support assistant of an outdoor shop. Answer in at most "
          "two sentences, only from the order data you are given. Never promise "
          "a refund, a delivery date or a discount.")

fixed = total = 0
for ticket in TICKETS:
    answer_prompt = "Order data: none\n\nCustomer: " + ticket["text"]
    for system, user in [(CLASSIFY, ticket["text"]), (SYSTEM, answer_prompt)]:
        total += count_message_tokens([{"role": "system", "content": system},
                                       {"role": "user", "content": user}])
        fixed += count_message_tokens([{"role": "system", "content": system}])
print(f"{len(TICKETS)} messages, {2 * len(TICKETS)} calls, {total} input tokens")
print(f"fixed system part {fixed} ({fixed / total:.0%})")
```

```text
40 messages, 80 calls, 5054 input tokens
fixed system part 3400 (67%)
```

40 mesaj, mesaj başına iki çağrıyla 80 çağrı ve 5054 giren token; bunun
3400'ü (%67) her çağrıda aynen tekrar eden sistem mesajları. Müşterinin
yazdığı kısım üçte birin biraz üstünde. Bu sayı modülün birkaç dersini bir
araya getiriyor: sistem mesajındaki her gereksiz cümle her çağrıda yeniden
ödenir (Bir Promptun Anatomisi), sabit başlangıç bazı servislerin ön ek
önbelleğine uygundur (Hatalar, Yeniden Deneme ve Maliyet) ve bir ekleme
başarı getirmiyorsa yalnızca maliyettir (Promptu Sistemli İyileştirmek).
Sayaç basitleştirilmiş; çıkan token'lar ve sipariş verisi bu hesapta
yok.

## Sonra

Bu modülde her şeyi kayıtlı yanıtlarla ve oyuncak modelle kurduk; program
her bilgisayarda aynı sonucu verdi. Gerçek bir modelle çalışmaya
başladığında değişen tek şey cevapların kaynağı olacak: mesaj listesi,
ayrıştırıcı, araç doğrulaması, değerlendirme kümesi, injection savunması
ve yeniden deneme aynen kalır. Değişmeyen kural ise şu: **prompt'un etkisi
senin modelinde, senin kümende ölçülür.**
